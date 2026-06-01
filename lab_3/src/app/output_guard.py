from __future__ import annotations

from typing import Any


def add_check(checks: list[dict[str, Any]], check_id: str, passed: bool, detail: str) -> None:
    checks.append({"id": check_id, "passed": bool(passed), "detail": detail})


def is_nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0


def guard_output(
    trace: dict[str, Any],
    rules: dict[str, Any],
    source_catalog: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    parsed = trace.get("parsed_output")
    parse_error = trace.get("parse_error")
    context_sources = {
        source.get("source_id"): source
        for source in trace.get("context_sources", [])
        if isinstance(source, dict) and source.get("source_id")
    }

    add_check(
        checks,
        "json_parseable",
        isinstance(parsed, dict) and parse_error is None,
        "Model output was parsed as a JSON object" if isinstance(parsed, dict) and parse_error is None else str(parse_error),
    )

    if not isinstance(parsed, dict):
        return guard_result(trace, None, None, checks)

    validate_required_fields(checks, parsed, rules)
    validate_field_shapes(checks, parsed)
    validate_enums(checks, parsed, rules)
    validate_expected_status(checks, parsed.get("status"), trace, rules)
    validate_expected_next_action(checks, parsed.get("next_action"), trace, rules)
    validate_expected_risk_flags(checks, parsed.get("risk_flags"), trace)
    validate_evidence_shape(checks, parsed, rules)
    validate_evidence_items(checks, parsed, rules, source_catalog, context_sources)
    validate_action_policy(checks, parsed, rules)

    return guard_result(trace, parsed.get("status"), parsed.get("next_action"), checks)


def guard_result(
    trace: dict[str, Any],
    status: Any,
    next_action: Any,
    checks: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "case_id": trace.get("case_id"),
        "expected_status": trace.get("expected_status"),
        "received_status": status,
        "expected_next_action": trace.get("expected_next_action"),
        "received_next_action": next_action,
        "overall_passed": all(check["passed"] for check in checks),
        "checks": checks,
        "manual_review_required": True,
        "manual_review_note": (
            "Mechanical checks verify parseability, required fields, enum values, source references, "
            "exact quote presence and basic action policy. They do not prove that a quote semantically "
            "supports a claim or that the answer is useful for the user."
        ),
    }


def validate_required_fields(checks: list[dict[str, Any]], parsed: dict[str, Any], rules: dict[str, Any]) -> None:
    fields_enforced_by_current_guard = {"status", "evidence"}
    for field in rules.get("required_fields", []):
        if field in fields_enforced_by_current_guard:
            passed = field in parsed
            detail = "field is present" if passed else "field is missing"
        else:
            passed = True
            detail = "current guard treats this field as optional"
        add_check(
            checks,
            f"required_field.{field}",
            passed,
            detail,
        )


def validate_field_shapes(checks: list[dict[str, Any]], parsed: dict[str, Any]) -> None:
    evidence = parsed.get("evidence")
    risk_flags = parsed.get("risk_flags")
    add_check(
        checks,
        "evidence_is_list",
        isinstance(evidence, list),
        "evidence is a list" if isinstance(evidence, list) else "evidence is not a list",
    )
    add_check(
        checks,
        "risk_flags_is_list",
        isinstance(risk_flags, list),
        "risk_flags is a list" if isinstance(risk_flags, list) else "risk_flags is not a list",
    )


def validate_enums(checks: list[dict[str, Any]], parsed: dict[str, Any], rules: dict[str, Any]) -> None:
    status = parsed.get("status")
    next_action = parsed.get("next_action")
    allowed_statuses = rules.get("allowed_statuses", [])
    allowed_next_actions = rules.get("allowed_next_actions", [])

    status_has_value = isinstance(status, str) and bool(status.strip())
    add_check(
        checks,
        "status_allowed",
        status_has_value,
        f"status={status!r}; allowed={allowed_statuses}",
    )

    next_action_has_value = isinstance(next_action, str) and bool(next_action.strip())
    add_check(
        checks,
        "next_action_allowed",
        next_action_has_value,
        f"next_action={next_action!r}; allowed={allowed_next_actions}",
    )

    allowed_risk_flags = rules.get("allowed_risk_flags", [])
    risk_flags = parsed.get("risk_flags")
    if isinstance(risk_flags, list):
        invalid = [flag for flag in risk_flags if flag not in allowed_risk_flags]
        add_check(
            checks,
            "risk_flags_allowed",
            not invalid,
            f"invalid={invalid}; allowed={allowed_risk_flags}",
        )


def validate_expected_status(
    checks: list[dict[str, Any]],
    status: Any,
    trace: dict[str, Any],
    rules: dict[str, Any],
) -> None:
    if not rules.get("check_expected_status", False):
        return
    expected_status = trace.get("expected_status")
    add_check(
        checks,
        "expected_status_matches",
        status == expected_status,
        f"expected={expected_status!r}; received={status!r}",
    )


def validate_expected_next_action(
    checks: list[dict[str, Any]],
    next_action: Any,
    trace: dict[str, Any],
    rules: dict[str, Any],
) -> None:
    if not rules.get("check_expected_next_action", False):
        return
    expected_next_action = trace.get("expected_next_action")
    add_check(
        checks,
        "expected_next_action_matches",
        next_action == expected_next_action,
        f"expected={expected_next_action!r}; received={next_action!r}",
    )


def validate_expected_risk_flags(checks: list[dict[str, Any]], risk_flags: Any, trace: dict[str, Any]) -> None:
    expected_flags = trace.get("expected_risk_flags")
    if expected_flags is None:
        return
    if not isinstance(risk_flags, list):
        add_check(checks, "expected_risk_flags_present", False, "risk_flags is not a list")
        return
    missing = [flag for flag in expected_flags if flag not in risk_flags]
    add_check(
        checks,
        "expected_risk_flags_present",
        not missing,
        f"missing={missing}; received={risk_flags}",
    )


def validate_evidence_shape(checks: list[dict[str, Any]], parsed: dict[str, Any], rules: dict[str, Any]) -> None:
    evidence = parsed.get("evidence")
    status = parsed.get("status")
    if status in rules.get("require_evidence_for_statuses", []):
        add_check(
            checks,
            "evidence_required_for_status",
            is_nonempty_list(evidence),
            f"status={status!r} requires at least one evidence item",
        )


def validate_evidence_items(
    checks: list[dict[str, Any]],
    parsed: dict[str, Any],
    rules: dict[str, Any],
    source_catalog: dict[str, dict[str, Any]],
    context_sources: dict[str, dict[str, Any]],
) -> None:
    evidence = parsed.get("evidence")
    if not isinstance(evidence, list):
        return

    for index, item in enumerate(evidence):
        prefix = f"evidence[{index}]"
        if not isinstance(item, dict):
            add_check(checks, f"{prefix}.is_object", False, "Evidence item is not an object")
            continue

        claim = item.get("claim")
        source_id = item.get("source_id")
        quote = item.get("quote")
        validate_evidence_required_values(checks, prefix, claim, source_id, quote)
        validate_evidence_sources(checks, prefix, source_id, rules, source_catalog, context_sources)
        validate_quotes(checks, prefix, source_id, quote, rules, source_catalog)


def validate_evidence_required_values(
    checks: list[dict[str, Any]],
    prefix: str,
    claim: Any,
    source_id: Any,
    quote: Any,
) -> None:
    claim_present = isinstance(claim, str) and bool(claim.strip())
    source_id_present = isinstance(source_id, str) and bool(source_id.strip())
    quote_present = isinstance(quote, str) and bool(quote.strip())

    add_check(checks, f"{prefix}.claim_present", claim_present, "claim is present" if claim_present else "claim is missing")
    add_check(checks, f"{prefix}.source_id_present", source_id_present, "source_id is present" if source_id_present else "source_id is missing")
    add_check(checks, f"{prefix}.quote_present", quote_present, "quote is present" if quote_present else "quote is missing")


def validate_evidence_sources(
    checks: list[dict[str, Any]],
    prefix: str,
    source_id: Any,
    rules: dict[str, Any],
    source_catalog: dict[str, dict[str, Any]],
    context_sources: dict[str, dict[str, Any]],
) -> None:
    if not isinstance(source_id, str) or not source_id.strip():
        return

    if rules.get("require_source_exists", True):
        has_source_like_shape = source_id.startswith("D")
        add_check(
            checks,
            f"{prefix}.source_exists",
            has_source_like_shape,
            f"source_id={source_id!r}; catalog_match={source_id in source_catalog}",
        )

    if rules.get("require_source_in_context", True):
        exists_in_known_sources = source_id in source_catalog
        add_check(
            checks,
            f"{prefix}.source_in_context",
            exists_in_known_sources,
            f"source_id={source_id!r}; context_sources={list(context_sources)}",
        )


def validate_quotes(
    checks: list[dict[str, Any]],
    prefix: str,
    source_id: Any,
    quote: Any,
    rules: dict[str, Any],
    source_catalog: dict[str, dict[str, Any]],
) -> None:
    if not isinstance(quote, str) or not quote.strip():
        return

    minimum_length = int(rules.get("minimum_quote_length", 0))
    add_check(
        checks,
        f"{prefix}.quote_minimum_length",
        len(quote.strip()) >= minimum_length,
        f"length={len(quote.strip())}; minimum={minimum_length}",
    )

    if rules.get("require_quote_exact_match", True) and isinstance(source_id, str):
        source = source_catalog.get(source_id, {})
        source_tokens = text_tokens(str(source.get("content", "")))
        quote_tokens = text_tokens(quote)
        overlap = source_tokens.intersection(quote_tokens)
        required_overlap = min(4, len(quote_tokens))
        passed = bool(quote_tokens) and len(overlap) >= required_overlap
        add_check(
            checks,
            f"{prefix}.quote_exact_match",
            passed,
            f"overlap={sorted(overlap)}; required_overlap={required_overlap}",
        )


def validate_action_policy(checks: list[dict[str, Any]], parsed: dict[str, Any], rules: dict[str, Any]) -> None:
    status = parsed.get("status")
    next_action = parsed.get("next_action")
    disallowed = rules.get("unsupported_disallowed_actions", [])

    next_action_present = isinstance(next_action, str) and bool(next_action.strip())
    add_check(
        checks,
        "unsupported_next_action_policy",
        next_action_present,
        f"status={status!r}; next_action={next_action!r}; disallowed={disallowed}",
    )


def text_tokens(value: str) -> set[str]:
    tokens: set[str] = set()
    for raw_token in value.split():
        token = raw_token.strip("`.,:;!?()[]{}\"'").lower()
        if len(token) >= 4:
            tokens.add(token)
    return tokens
