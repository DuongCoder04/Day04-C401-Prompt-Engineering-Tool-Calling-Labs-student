from __future__ import annotations

from typing import Any

import requests

from tools._shared import TIMEOUT, domain, err


def search(query: str = "", max_results: int = 5) -> dict[str, Any]:
    try:
        if not query:
            raise ValueError("Missing query")
        url = "https://api.duckduckgo.com/"
        params = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}
        response = requests.get(url, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        items = []

        abstract = data.get("AbstractText", "")
        abstract_src = data.get("AbstractSource", "")
        abstract_url = data.get("AbstractURL", "")
        if abstract:
            items.append({
                "title": abstract_src or "Abstract",
                "url": abstract_url,
                "source": domain(abstract_url),
                "summary": abstract[:500],
            })

        for topic in data.get("RelatedTopics", []):
            if "Topics" in topic:
                for sub in topic["Topics"][:max_results]:
                    items.append({
                        "title": sub.get("Text", "").split(" - ")[0],
                        "url": sub.get("FirstURL", ""),
                        "source": domain(sub.get("FirstURL", "")),
                        "summary": sub.get("Text", "")[:300],
                    })
            else:
                items.append({
                    "title": topic.get("Text", "").split(" - ")[0],
                    "url": topic.get("FirstURL", ""),
                    "source": domain(topic.get("FirstURL", "")),
                    "summary": topic.get("Text", "")[:300],
                })
            if len(items) >= max_results:
                break

        if not items:
            items.append({
                "title": query,
                "url": f"https://duckduckgo.com/?q={query}",
                "source": "duckduckgo.com",
                "summary": f"Xem kết quả tìm kiếm tại DuckDuckGo cho: {query}",
            })

        return {"tool": "search", "query": query, "items": items[:max_results]}
    except Exception as exc:
        return err("search", exc)
