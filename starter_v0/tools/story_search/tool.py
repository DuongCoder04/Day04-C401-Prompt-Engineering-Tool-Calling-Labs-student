from __future__ import annotations

from typing import Any

import requests

from tools._shared import TIMEOUT, err


def story_search(query: str = "", max_results: int = 5) -> dict[str, Any]:
    try:
        if not query:
            raise ValueError("Missing query")
        url = "https://openlibrary.org/search.json"
        params = {
            "q": query,
            "limit": min(int(max_results or 5), 50),
            "sort": "rating",
        }
        response = requests.get(url, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        items = []
        for doc in data.get("docs", []):
            cover_id = doc.get("cover_i")
            items.append({
                "title": doc.get("title", ""),
                "author": ", ".join(doc.get("author_name", [])),
                "year": doc.get("first_publish_year"),
                "isbn": (doc.get("isbn") or [None])[0],
                "pages": doc.get("number_of_pages_median"),
                "subjects": (doc.get("subject") or [])[:3],
                "url": f"https://openlibrary.org{doc.get('key', '')}" if doc.get("key") else "",
                "cover_url": f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else "",
            })
        return {"tool": "story_search", "query": query, "items": items}
    except Exception as exc:
        return err("story_search", exc)
