from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SYSTEM_DIR = ROOT / "system"
CASES_DIR = ROOT / "cases"
EXAMPLE_CASES_PATH = CASES_DIR / "example_cases.json"
STUDENT_CASES_PATH = CASES_DIR / "my_cases.json"
CONTRACT_PATH = SYSTEM_DIR / "study_assistant_contract.md"
OUTPUTS_DIR = ROOT / "outputs"
REVIEWS_DIR = OUTPUTS_DIR / "reviews"

REQUIRED_CASE_FIELDS = [
    "id",
    "slice",
    "user_prompt",
    "expected_behavior",
    "forbidden_behavior",
    "observe",
    "failure_to_catch",
]


def load_dotenv(path: Path = ROOT / ".env") -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_contract() -> str:
    if not CONTRACT_PATH.exists():
        raise RuntimeError(f"Brak pliku kontraktu: {CONTRACT_PATH.relative_to(ROOT)}")
    return CONTRACT_PATH.read_text(encoding="utf-8").strip()


def case_files() -> list[Path]:
    return [EXAMPLE_CASES_PATH, STUDENT_CASES_PATH]


def load_cases_from_file(path: Path) -> list[dict[str, Any]]:
    data = read_json(path)
    cases = data.get("cases")
    if not isinstance(cases, list):
        raise RuntimeError(f"{path.relative_to(ROOT)} musi zawierać listę 'cases' na najwyższym poziomie")

    loaded: list[dict[str, Any]] = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise RuntimeError(f"{path.relative_to(ROOT)} przypadek #{index + 1} nie jest obiektem")
        copied = dict(case)
        copied["_case_file"] = str(path.relative_to(ROOT))
        loaded.append(copied)
    return loaded


def load_all_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for path in case_files():
        if not path.exists():
            raise RuntimeError(f"Brak pliku z przypadkami: {path.relative_to(ROOT)}")
        cases.extend(load_cases_from_file(path))
    return cases


def load_student_cases() -> list[dict[str, Any]]:
    return load_cases_from_file(STUDENT_CASES_PATH)


def find_case(case_id: str) -> dict[str, Any]:
    matches = [case for case in load_all_cases() if case.get("id") == case_id]
    if not matches:
        raise RuntimeError(f"Nieznany identyfikator przypadku: {case_id}")
    if len(matches) > 1:
        raise RuntimeError(f"Powtórzony identyfikator przypadku: {case_id}")
    return matches[0]


def validate_case(case: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_CASE_FIELDS:
        value = case.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"brakujące albo puste pole: {field}")

    case_id = case.get("id")
    if isinstance(case_id, str) and case_id.strip():
        if not re.fullmatch(r"[a-z0-9_]+", case_id):
            errors.append("id może zawierać tylko małe litery, cyfry i podkreślenia")

    return errors


def contains_todo(case: dict[str, Any]) -> bool:
    for field in REQUIRED_CASE_FIELDS:
        value = case.get(field)
        if isinstance(value, str) and "TODO" in value.upper():
            return True
    return False


def review_path(case_id: str) -> Path:
    return REVIEWS_DIR / f"{case_id}.md"
