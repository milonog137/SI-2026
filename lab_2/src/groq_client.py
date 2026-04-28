from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request


GROQ_CHAT_COMPLETIONS_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "llama-3.3-70b-versatile"


def get_model_name() -> str:
    return os.environ.get("GROQ_MODEL", DEFAULT_MODEL)


def mask_secret(value: str | None) -> str:
    if not value:
        return "<missing>"
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}...{value[-4:]}"


def validate_environment() -> None:
    if not os.environ.get("GROQ_API_KEY"):
        raise RuntimeError("Missing GROQ_API_KEY. Fill src/.env from src/.env.example.")


def retry_delay(body: str, attempt: int) -> float:
    match = re.search(r"try again in ([0-9.]+)s", body, flags=re.IGNORECASE)
    if match:
        return float(match.group(1)) + 0.5
    return min(8.0, 1.0 + attempt * 1.5)


def chat_completion(messages: list[dict[str, str]], temperature: float = 0.0, max_tokens: int = 500) -> str:
    validate_environment()
    payload = {
        "model": get_model_name(),
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    for attempt in range(5):
        request = urllib.request.Request(
            GROQ_CHAT_COMPLETIONS_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "course-generation-lab2/1.0",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                data = json.loads(response.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")
            if error.code == 429 and attempt < 4:
                time.sleep(retry_delay(body, attempt))
                continue
            raise RuntimeError(f"Groq HTTP {error.code}: {body}") from error
        except urllib.error.URLError as error:
            raise RuntimeError(f"Groq request failed: {error.reason}") from error
    raise RuntimeError("Groq request failed after retries")
