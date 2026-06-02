from __future__ import annotations

import os
from typing import Any

import requests

from tools._shared import err

_STYLE_INSTRUCTIONS = {
    "bullet":    "Summarize in concise bullet points (•). Each point on a new line.",
    "paragraph": "Summarize in one or two clear paragraphs.",
    "tldr":      "Write a TL;DR in 1–2 sentences maximum.",
}


def summarize_text(
    text: str = "",
    style: str = "bullet",
    max_words: int = 150,
) -> dict[str, Any]:
    """Summarize a long text using the OpenRouter LLM provider."""
    if not text.strip():
        return {"tool": "summarize", "error": "empty input", "summary": ""}

    api_key  = os.getenv("OPENROUTER_API_KEY")
    model    = os.getenv("OPENROUTER_DEFAULT_MODEL", "openai/gpt-oss-20b:free")
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

    if not api_key:
        return err("summarize", RuntimeError("Missing OPENROUTER_API_KEY env var"))

    style_key  = style.lower() if style.lower() in _STYLE_INSTRUCTIONS else "bullet"
    style_inst = _STYLE_INSTRUCTIONS[style_key]
    prompt = (
        f"{style_inst} Keep the summary under {max_words} words.\n\n"
        f"TEXT TO SUMMARIZE:\n{text[:6000]}"
    )

    try:
        resp = requests.post(
            f"{base_url}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model":       model,
                "messages":    [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens":  400,
            },
            timeout=30,
        )
        resp.raise_for_status()
        data    = resp.json()
        summary = data["choices"][0]["message"]["content"].strip()
    except Exception as exc:
        return err("summarize", exc)

    return {
        "tool":    "summarize",
        "style":   style_key,
        "summary": summary,
        "items":   [{"title": summary[:120], "summary": summary, "source": "LLM summarizer"}],
    }
