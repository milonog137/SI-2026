from __future__ import annotations

import json
from typing import Any

from app import lab_io


def save_check_outputs(trace: dict[str, Any], result: dict[str, Any]) -> None:
    case_id = trace["case_id"]
    lab_io.write_json(lab_io.check_json_path(case_id), result)
    lab_io.write_text(lab_io.check_report_path(case_id), check_markdown(trace, result))


def check_markdown(trace: dict[str, Any], result: dict[str, Any]) -> str:
    status_line = "PASS" if result["overall_passed"] else "ATTENTION"
    checks_table = "\n".join(
        f"| `{markdown_cell(check['id'])}` | {'PASS' if check['passed'] else 'FAIL'} | {markdown_cell(check['detail'])} |"
        for check in result["checks"]
    )
    return f"""# Output Guard: {trace.get("case_id")}

Overall: **{status_line}**

Expected status: `{trace.get("expected_status")}`
Received status: `{result.get("received_status")}`

Expected next_action: `{trace.get("expected_next_action")}`
Received next_action: `{result.get("received_next_action")}`

Expected risk_flags: `{trace.get("expected_risk_flags")}`

## Mechanical Checks

| Check | Result | Detail |
| --- | --- | --- |
{checks_table}

## Manual Review Required

{result["manual_review_note"]}

Suggested manual question:

```text
claim -> source_id -> quote -> czy quote faktycznie wspiera stwierdzenie?
```

## Parsed Output

```json
{json.dumps(trace.get("parsed_output"), ensure_ascii=False, indent=2)}
```
"""


def markdown_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")
