from __future__ import annotations

from typing import Any


def build_messages(case: dict[str, Any], contract: str) -> list[dict[str, str]]:
    user_message = f"""Udziel odpowiedzi jako Study Assistant na wiadomość studenta.

Wiadomość studenta:
{case["user_prompt"]}

Odpowiedz bezpośrednio studentowi i zachowaj kontrakt systemowy."""

    return [
        {"role": "system", "content": contract},
        {"role": "user", "content": user_message},
    ]
