from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCES_DIR = ROOT / "sources"
SYSTEM_DIR = ROOT / "system"
CASES_PATH = ROOT / "cases.json"
CONTRACT_PATH = SYSTEM_DIR / "output_contract.md"
RULES_PATH = SYSTEM_DIR / "output_guard_rules.json"
OUTPUTS_DIR = ROOT / "outputs"
TRACES_DIR = OUTPUTS_DIR / "traces"
CHECKS_DIR = OUTPUTS_DIR / "checks"


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


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def parse_source(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    metadata: dict[str, str] = {}
    content_lines: list[str] = []
    in_metadata = True

    for line in text.splitlines():
        if in_metadata and not line.strip():
            in_metadata = False
            continue
        if in_metadata and ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()
            continue
        in_metadata = False
        content_lines.append(line)

    source_id = metadata.get("source_id") or path.stem
    return {
        "source_id": source_id,
        "path": str(path.relative_to(ROOT)),
        "metadata": metadata,
        "content": "\n".join(content_lines).strip(),
    }


def load_sources() -> dict[str, dict[str, Any]]:
    return {
        source["source_id"]: source
        for source in (parse_source(path) for path in sorted(SOURCES_DIR.glob("*.md")))
    }


def load_cases() -> list[dict[str, Any]]:
    data = read_json(CASES_PATH)
    cases = data.get("cases")
    if not isinstance(cases, list):
        raise RuntimeError("cases.json must contain a top-level 'cases' list")
    return cases


def find_case(case_id: str) -> dict[str, Any]:
    for case in load_cases():
        if case.get("id") == case_id:
            return case
    raise RuntimeError(f"Unknown case id: {case_id}")


def load_contract() -> str:
    return CONTRACT_PATH.read_text(encoding="utf-8").strip()


def load_rules() -> dict[str, Any]:
    rules = read_json(RULES_PATH)
    if not isinstance(rules, dict):
        raise RuntimeError("output_guard_rules.json must contain an object")
    return rules


def trace_path(case_id: str) -> Path:
    return TRACES_DIR / f"{case_id}.json"


def check_json_path(case_id: str) -> Path:
    return CHECKS_DIR / f"{case_id}.json"


def check_report_path(case_id: str) -> Path:
    return CHECKS_DIR / f"{case_id}.md"
