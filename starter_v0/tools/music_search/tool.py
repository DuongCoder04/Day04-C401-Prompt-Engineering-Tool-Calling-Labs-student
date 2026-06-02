from __future__ import annotations

from typing import Any

import requests

from tools._shared import TIMEOUT, err


def music_search(query: str = "", max_results: int = 5) -> dict[str, Any]:
    try:
        if not query:
            raise ValueError("Missing query")
        url = "https://itunes.apple.com/search"
        params = {
            "term": query,
            "limit": min(int(max_results or 5), 50),
            "media": "music",
            "entity": "song,album",
        }
        response = requests.get(url, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        items = []
        for item in data.get("results", []):
            kind = item.get("kind", "song")
            items.append({
                "title": item.get("trackName") or item.get("collectionName", ""),
                "artist": item.get("artistName", ""),
                "album": item.get("collectionName", ""),
                "type": "song" if kind == "song" else "album",
                "url": item.get("trackViewUrl") or item.get("collectionViewUrl", ""),
                "genre": item.get("primaryGenreName", ""),
                "release_date": item.get("releaseDate", "")[:10] if item.get("releaseDate") else "",
                "preview_url": item.get("previewUrl", ""),
            })
        return {"tool": "music_search", "query": query, "items": items}
    except Exception as exc:
        return err("music_search", exc)
