from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request


API_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "llama-3.3-70b-versatile"
USER_AGENT = "si-2026-lab4-study-assistant/0.1"


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Brak wymaganej zmiennej środowiskowej: {name}")
    return value


def get_model_name() -> str:
    return os.environ.get("GROQ_MODEL", DEFAULT_MODEL)


def validate_environment() -> None:
    _require_env("GROQ_API_KEY")


def chat_completion(messages: list[dict[str, str]]) -> str:
    api_key = _require_env("GROQ_API_KEY")
    payload = {
        "model": get_model_name(),
        "messages": messages,
        "temperature": 0.2,
    }
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )

    last_error: RuntimeError | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                response_body = response.read().decode("utf-8")
            break
        except urllib.error.HTTPError as error:
            error_body = error.read().decode("utf-8", errors="replace")
            if error.code == 429 and attempt < 2:
                time.sleep(2 * (attempt + 1))
                continue
            raise RuntimeError(f"Błąd HTTP Groq {error.code}: {error_body}") from error
        except urllib.error.URLError as error:
            last_error = RuntimeError(f"Zapytanie do Groq nie powiodło się: {error.reason}")
            raise last_error from error
    else:
        raise last_error or RuntimeError("Zapytanie do Groq nie powiodło się bez szczegółów")

    data = json.loads(response_body)
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError(f"Nieoczekiwany kształt odpowiedzi Groq: {response_body}") from error
