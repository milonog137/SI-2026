from __future__ import annotations

from typing import Any

from app import lab_io


def save_review(review_data: dict[str, Any]) -> None:
    lab_io.write_text(lab_io.review_path(review_data["case_id"]), review_markdown(review_data))


def review_markdown(review_data: dict[str, Any]) -> str:
    return f"""# Karta przeglądu: {review_data.get("case_id")}

Model: `{review_data.get("model")}`

## Przypadek

Kategoria sytuacji:

```text
{review_data.get("slice")}
```

Wiadomość studenta:

```text
{review_data.get("user_prompt")}
```

Zachowanie oczekiwane:

```text
{review_data.get("expected_behavior")}
```

Zachowanie niedopuszczalne:

```text
{review_data.get("forbidden_behavior")}
```

Kryterium obserwacji:

```text
{review_data.get("observe")}
```

Naruszenie kontraktu, które ten przypadek ma ujawnić:

```text
{review_data.get("failure_to_catch")}
```

## Odpowiedź modelu

```text
{review_data.get("raw_assistant_answer")}
```

## Miejsce na ręczną analizę

Ocena: `pass / partial / fail / severe_fail`

Dowód z odpowiedzi modelu:

```text

```

Krótki wniosek:

```text

```
"""
