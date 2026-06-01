from __future__ import annotations

from typing import Any


def render_source_block(source: dict[str, Any]) -> str:
    metadata = source["metadata"]
    header = (
        f'<SOURCE source_id="{source["source_id"]}" '
        f'title="{metadata.get("title", "")}" '
        f'date="{metadata.get("date", "")}" '
        f'status="{metadata.get("status", "")}" '
        f'authority="{metadata.get("authority", "")}" '
        f'source_type="{metadata.get("source_type", "")}">'
    )
    return f"{header}\n{source['content']}\n</SOURCE>"


def build_messages(
    case: dict[str, Any],
    sources: dict[str, dict[str, Any]],
    output_contract: str,
) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    context_sources = []
    missing_sources = []

    for source_id in case.get("context_source_ids", []):
        source = sources.get(source_id)
        if source is None:
            missing_sources.append(source_id)
            continue
        context_sources.append(source)

    if missing_sources:
        raise RuntimeError(f"Case {case.get('id')} references missing sources: {', '.join(missing_sources)}")

    context = "\n\n".join(render_source_block(source) for source in context_sources)
    user_message = f"""Pytanie uzytkownika:
{case["question"]}

Kontekst przekazany modelowi:
{context}

Zwroc output zgodny z kontraktem systemowym."""

    return [
        {"role": "system", "content": output_contract},
        {"role": "user", "content": user_message},
    ], context_sources
