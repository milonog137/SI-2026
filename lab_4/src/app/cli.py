from __future__ import annotations

import argparse
import os
from pathlib import Path

from app import lab_io
from app.groq_client import chat_completion, get_model_name, validate_environment
from app.prompt_builder import build_messages
from app.review_writer import save_review


def command_doctor() -> int:
    lab_io.load_dotenv()
    errors: list[str] = []
    warnings: list[str] = []

    try:
        contract = lab_io.load_contract()
        if not contract:
            errors.append("study_assistant_contract.md is empty")
    except Exception as error:  # noqa: BLE001
        errors.append(str(error))

    all_cases = []
    try:
        all_cases = lab_io.load_all_cases()
    except Exception as error:  # noqa: BLE001
        errors.append(str(error))

    seen_ids: set[str] = set()
    for case in all_cases:
        case_id = case.get("id", "<missing>")
        if case_id in seen_ids:
            errors.append(f"powtórzony identyfikator przypadku: {case_id}")
        if isinstance(case_id, str):
            seen_ids.add(case_id)
        for error in lab_io.validate_case(case):
            errors.append(f"{case.get('_case_file')}: {case_id}: {error}")
        if case.get("_case_file") == str(Path("cases") / "my_cases.json") and lab_io.contains_todo(case):
            warnings.append(f"cases/my_cases.json: {case_id} nadal zawiera tekst TODO")

    print("Laboratorium 4: sprawdzenie środowiska")
    print("\nSprawdzenie lokalne:")
    print(f"- kontrakt: {'ok' if not errors else 'sprawdzony'}")
    print(f"- przypadki: {len(all_cases)}")
    print(f"- model: {get_model_name()}")
    print(f"- GROQ_API_KEY: {'obecny' if os.environ.get('GROQ_API_KEY') else 'brak'}")

    if warnings:
        print("\nOstrzeżenia:")
        for warning in warnings:
            print(f"- {warning}")

    if errors:
        print("\nProblemy:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("- pliki lokalne: ok")

    if not os.environ.get("GROQ_API_KEY"):
        print("\nSprawdzenie połączenia z Groq:")
        print("- pominięto: brak GROQ_API_KEY")
        return 0

    print("\nSprawdzenie połączenia z Groq:")
    try:
        validate_environment()
        output = chat_completion(
            [
                {"role": "system", "content": "Odpowiedz wyłącznie słowem ok."},
                {"role": "user", "content": "Test połączenia."},
            ]
        )
    except Exception as error:  # noqa: BLE001
        print(f"- niepowodzenie ({error})")
        return 1

    print(f"- ok ({output.strip()[:80]})")
    return 0


def command_list() -> int:
    for case in lab_io.load_all_cases():
        print(f"{case['id']}  [{case.get('_case_file')}]")
    return 0


def command_ask(case_id: str) -> int:
    lab_io.load_dotenv()
    case = lab_io.find_case(case_id)
    for error in lab_io.validate_case(case):
        raise RuntimeError(f"{case_id}: {error}")
    if lab_io.contains_todo(case):
        raise RuntimeError(f"{case_id} nadal zawiera tekst TODO")

    validate_environment()
    contract = lab_io.load_contract()
    messages = build_messages(case, contract)
    raw_answer = chat_completion(messages)
    save_review(make_review_data(case, raw_answer))
    print(f"Zapisano kartę przeglądu: {lab_io.review_path(case_id).relative_to(lab_io.ROOT)}")
    return 0


def make_review_data(case: dict, raw_answer: str) -> dict:
    return {
        "case_id": case["id"],
        "model": get_model_name(),
        "slice": case.get("slice"),
        "user_prompt": case.get("user_prompt"),
        "expected_behavior": case.get("expected_behavior"),
        "forbidden_behavior": case.get("forbidden_behavior"),
        "observe": case.get("observe"),
        "failure_to_catch": case.get("failure_to_catch"),
        "raw_assistant_answer": raw_answer,
    }


def command_run_student() -> int:
    lab_io.load_dotenv()
    cases = lab_io.load_student_cases()
    for case in cases:
        case_id = case["id"]
        for error in lab_io.validate_case(case):
            raise RuntimeError(f"{case_id}: {error}")
        if lab_io.contains_todo(case):
            raise RuntimeError(f"{case_id} nadal zawiera tekst TODO")

    validate_environment()
    for case in cases:
        case_id = case["id"]
        print(f"\n== {case_id} ==")
        command_ask(case_id)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Skrypt uruchomieniowy dla Laboratorium 4")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("doctor", help="sprawdź pliki lokalne i połączenie z Groq, jeśli jest skonfigurowane")
    subparsers.add_parser("list", help="wypisz dostępne przypadki")

    ask_parser = subparsers.add_parser("ask", help="wywołaj model dla jednego przypadku")
    ask_parser.add_argument("--case", required=True, help="identyfikator przypadku z cases/example_cases.json albo cases/my_cases.json")

    subparsers.add_parser("run-student", help="uruchom wszystkie przypadki z cases/my_cases.json i zapisz karty przeglądu")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "doctor":
            return command_doctor()
        if args.command == "list":
            return command_list()
        if args.command == "ask":
            return command_ask(args.case)
        if args.command == "run-student":
            return command_run_student()
    except RuntimeError as error:
        print(f"Błąd: {error}")
        return 1
    except KeyboardInterrupt:
        print("Przerwano")
        return 130

    return 2
