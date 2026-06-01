from __future__ import annotations

from typing import Any

from app import lab_io
from app.groq_client import get_model_name
from app.output_parser import parse_model_output


def make_trace(
    case: dict[str, Any],
    messages: list[dict[str, str]],
    context_sources: list[dict[str, Any]],
    raw_output: str,
    output_contract: str,
) -> dict[str, Any]:
    parsed_output, parse_error = parse_model_output(raw_output)
    return {
        "created_at": lab_io.now_iso(),
        "model": get_model_name(),
        "case_id": case["id"],
        "case_title": case.get("title", ""),
        "question": case["question"],
        "expected_status": case.get("expected_status"),
        "expected_next_action": case.get("expected_next_action"),
        "expected_risk_flags": case.get("expected_risk_flags"),
        "focus": case.get("focus", []),
        "context_source_ids": case.get("context_source_ids", []),
        "context_sources": context_sources,
        "output_contract": output_contract,
        "full_model_input": {"messages": messages},
        "raw_model_output": raw_output,
        "parsed_output": parsed_output,
        "parse_error": parse_error,
    }
