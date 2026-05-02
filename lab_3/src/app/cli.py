from __future__ import annotations

import argparse
import os
import re
import shutil

from app import lab_io
from app.groq_client import chat_completion, get_model_name, validate_environment
from app.output_guard import guard_output
from app.prompt_builder import build_messages
from app.report_writer import save_check_outputs
from app.trace_store import make_trace


def command_doctor() -> int:
    lab_io.load_dotenv()
    errors: list[str] = []

    sources = lab_io.load_sources()
    if not sources:
        errors.append("No sources found in sources/")

    try:
        cases = lab_io.load_cases()
        rules = lab_io.load_rules()
        lab_io.load_contract()
    except Exception as error:  # noqa: BLE001
        errors.append(str(error))
        cases = []
        rules = {}

    allowed_statuses = rules.get("allowed_statuses", [])
    allowed_next_actions = rules.get("allowed_next_actions", [])
    allowed_risk_flags = rules.get("allowed_risk_flags", [])
    case_ids = set()
    for case in cases:
        case_id = case.get("id")
        if not case_id:
            errors.append("Case without id")
            continue
        if case_id in case_ids:
            errors.append(f"Duplicate case id: {case_id}")
        case_ids.add(case_id)
        for source_id in case.get("context_source_ids", []):
            if source_id not in sources:
                errors.append(f"Case {case_id} references missing source {source_id}")
        if allowed_statuses and case.get("expected_status") not in allowed_statuses:
            errors.append(f"Case {case_id} has invalid expected_status {case.get('expected_status')!r}")
        if allowed_next_actions and case.get("expected_next_action") not in allowed_next_actions:
            errors.append(f"Case {case_id} has invalid expected_next_action {case.get('expected_next_action')!r}")
        for flag in case.get("expected_risk_flags", []):
            if allowed_risk_flags and flag not in allowed_risk_flags:
                errors.append(f"Case {case_id} has invalid expected_risk_flag {flag!r}")

    has_api_key = bool(os.environ.get("GROQ_API_KEY"))

    print("Lab 3 doctor")
    print("\nLocal setup:")
    print(f"- sources: {len(sources)}")
    print(f"- cases: {len(cases)}")
    print(f"- model: {get_model_name()}")
    print(f"- GROQ_API_KEY: {'present' if has_api_key else 'missing'}")

    if errors:
        print("- local files: failed")
        print("\nStructural problems:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("- local files: ok")

    print("\nLive Groq check:")
    if not has_api_key:
        print("- skipped: GROQ_API_KEY missing")
        return 0

    try:
        validate_environment()
        output = chat_completion(
            [
                {"role": "system", "content": "Odpowiedz wylacznie slowem ok."},
                {"role": "user", "content": "Test polaczenia."},
            ]
        )
    except Exception as error:  # noqa: BLE001
        print(f"- failed ({error})")
        return 1
    print(f"- ok ({output.strip()[:80]})")

    return 0


def command_ask(case_id: str) -> int:
    lab_io.load_dotenv()
    validate_environment()
    sources = lab_io.load_sources()
    case = lab_io.find_case(case_id)
    output_contract = lab_io.load_contract()
    messages, context_sources = build_messages(case, sources, output_contract)
    raw_output = chat_completion(messages)
    trace = make_trace(case, messages, context_sources, raw_output, output_contract)
    lab_io.write_json(lab_io.trace_path(case_id), trace)
    parsed_state = "parsed" if trace.get("parsed_output") is not None else f"parse_error={trace.get('parse_error')}"
    print(f"Wrote trace: {lab_io.trace_path(case_id).relative_to(lab_io.ROOT)}")
    print(f"Model output: {parsed_state}")
    return 0


def command_check(case_id: str) -> int:
    lab_io.load_dotenv()
    path = lab_io.trace_path(case_id)
    if not path.exists():
        print(f"Missing trace: {path.relative_to(lab_io.ROOT)}")
        print(f"Run first: make ask CASE_ID={case_id}")
        return 1

    trace = lab_io.read_json(path)
    result = guard_output(trace, lab_io.load_rules(), lab_io.load_sources())
    save_check_outputs(trace, result)
    print(f"Wrote check JSON: {lab_io.check_json_path(case_id).relative_to(lab_io.ROOT)}")
    print(f"Wrote check report: {lab_io.check_report_path(case_id).relative_to(lab_io.ROOT)}")
    print(f"Guard result: {'PASS' if result['overall_passed'] else 'ATTENTION'}")
    return 0


def command_run_all() -> int:
    lab_io.load_dotenv()
    validate_environment()
    for case in lab_io.load_cases():
        print(f"\n== {case['id']} ==")
        command_ask(case["id"])
        command_check(case["id"])
    return 0


def command_snapshot(case_id: str, label: str) -> int:
    if not re.fullmatch(r"[A-Za-z0-9_-]+", label):
        raise RuntimeError("Snapshot label may contain only letters, digits, '_' and '-'")

    artifacts = [
        (lab_io.trace_path(case_id), lab_io.TRACES_DIR / f"{case_id}_{label}.json"),
        (lab_io.check_json_path(case_id), lab_io.CHECKS_DIR / f"{case_id}_{label}.json"),
        (lab_io.check_report_path(case_id), lab_io.CHECKS_DIR / f"{case_id}_{label}.md"),
    ]
    missing = [source.relative_to(lab_io.ROOT) for source, _ in artifacts if not source.exists()]
    if missing:
        print("Missing artifact(s):")
        for path in missing:
            print(f"- {path}")
        print(f"Run first: make ask CASE_ID={case_id} && make check CASE_ID={case_id}")
        return 1

    for source, target in artifacts:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        print(f"Wrote snapshot: {target.relative_to(lab_io.ROOT)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Lab 3 execution harness")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("doctor", help="check local setup and Groq connection when configured")

    ask_parser = subparsers.add_parser("ask", help="call Groq for one case")
    ask_parser.add_argument("--case", required=True, help="case id from cases.json")

    check_parser = subparsers.add_parser("check", help="check one existing trace")
    check_parser.add_argument("--case", required=True, help="case id from cases.json")

    snapshot_parser = subparsers.add_parser("snapshot", help="copy current trace and check outputs with a label")
    snapshot_parser.add_argument("--case", required=True, help="case id from cases.json")
    snapshot_parser.add_argument("--label", required=True, help="suffix such as before_intervention or after_intervention_1")

    subparsers.add_parser("run-all", help="ask and check all cases")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "doctor":
            return command_doctor()
        if args.command == "ask":
            return command_ask(args.case)
        if args.command == "check":
            return command_check(args.case)
        if args.command == "snapshot":
            return command_snapshot(args.case, args.label)
        if args.command == "run-all":
            return command_run_all()
    except RuntimeError as error:
        print(f"Error: {error}")
        return 1
    except KeyboardInterrupt:
        print("Interrupted")
        return 130

    return 2
