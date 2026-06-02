from __future__ import annotations

import os
from typing import Any

import requests

from tools._shared import TIMEOUT, err


def get_crypto_price(
    symbols: list[str] | None = None,
    base_currency: str = "USD",
    limit: int = 5,
) -> dict[str, Any]:
    """Fetch realtime crypto prices via RapidAPI crypto-news51."""
    key  = os.getenv("RAPIDAPI_KEY")
    host = os.getenv("RAPIDAPI_CRYPTO_HOST", "crypto-news51.p.rapidapi.com")
    if not key:
        return err("crypto_price", RuntimeError("Missing RAPIDAPI_KEY env var"))

    page_size = max(1, min(int(limit), 20))
    try:
        resp = requests.get(
            f"https://{host}/api/v1/mini-crypto/prices",
            params={"base_currency": base_currency, "page": "1", "page_size": str(page_size)},
            headers={"x-rapidapi-key": key, "x-rapidapi-host": host, "Content-Type": "application/json"},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        return err("crypto_price", exc)

    results = data.get("results", [])

    # Filter by symbols if provided
    if symbols:
        upper = {s.upper() for s in symbols}
        results = [r for r in results if r.get("symbol", "").upper() in upper]

    items = []
    for r in results:
        price      = r.get("price", 0)
        change     = r.get("change_24h_percent", 0)
        market_cap = r.get("market_cap", 0)
        symbol     = r.get("symbol", "")
        name       = r.get("name", "")
        arrow      = "▲" if change >= 0 else "▼"
        title      = f"{symbol} ({name}): ${price:,.2f}  {arrow}{abs(change):.2f}%"
        items.append({
            "title":      title,
            "symbol":     symbol,
            "name":       name,
            "price":      round(price, 4),
            "change_24h": round(change, 4),
            "market_cap": round(market_cap, 2),
            "currency":   base_currency,
            "url":        f"https://coinmarketcap.com/currencies/{r.get('slug', symbol.lower())}/",
            "source":     "crypto-news51",
        })

    return {
        "tool":          "crypto_price",
        "base_currency": base_currency,
        "items":         items,
    }
