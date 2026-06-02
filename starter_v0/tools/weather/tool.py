from __future__ import annotations

from typing import Any

import requests

from tools._shared import TIMEOUT, err

# Open-Meteo geocoding + forecast — no API key required
_GEO_URL     = "https://geocoding-api.open-meteo.com/v1/search"
_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

_WMO_CODES: dict[int, str] = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Icy fog",
    51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
    61: "Light rain", 63: "Rain", 65: "Heavy rain",
    71: "Light snow", 73: "Snow", 75: "Heavy snow",
    80: "Rain showers", 81: "Rain showers", 82: "Violent rain showers",
    95: "Thunderstorm", 96: "Thunderstorm + hail", 99: "Thunderstorm + heavy hail",
}


def get_weather(city: str = "Hanoi", unit: str = "celsius") -> dict[str, Any]:
    """Fetch current weather for a city using Open-Meteo (no API key)."""
    temp_unit = "fahrenheit" if unit.lower().startswith("f") else "celsius"

    # Step 1: Geocode city name
    try:
        geo = requests.get(
            _GEO_URL,
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=TIMEOUT,
        ).json()
    except Exception as exc:
        return err("weather", exc)

    results = geo.get("results", [])
    if not results:
        return {"tool": "weather", "error": f"City not found: {city}", "items": []}

    loc        = results[0]
    lat, lon   = loc["latitude"], loc["longitude"]
    city_label = f"{loc.get('name', city)}, {loc.get('country', '')}"

    # Step 2: Fetch current weather
    try:
        wx = requests.get(
            _WEATHER_URL,
            params={
                "latitude":              lat,
                "longitude":             lon,
                "current":               "temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weathercode",
                "temperature_unit":      temp_unit,
                "wind_speed_unit":       "kmh",
                "timezone":              "auto",
                "forecast_days":         1,
            },
            timeout=TIMEOUT,
        ).json()
    except Exception as exc:
        return err("weather", exc)

    cur  = wx.get("current", {})
    code = cur.get("weathercode", 0)
    desc = _WMO_CODES.get(code, "Unknown")
    temp = cur.get("temperature_2m", "?")
    feel = cur.get("apparent_temperature", "?")
    hum  = cur.get("relative_humidity_2m", "?")
    wind = cur.get("wind_speed_10m", "?")
    u    = "°F" if temp_unit == "fahrenheit" else "°C"

    summary = (
        f"{city_label}: {desc}, {temp}{u} (feels {feel}{u}), "
        f"humidity {hum}%, wind {wind} km/h"
    )
    items = [{
        "title":       summary,
        "city":        city_label,
        "description": desc,
        "temperature": temp,
        "feels_like":  feel,
        "humidity":    hum,
        "wind_kmh":    wind,
        "unit":        temp_unit,
        "source":      "open-meteo.com",
        "url":         f"https://open-meteo.com/",
    }]
    return {"tool": "weather", "city": city_label, "items": items}
