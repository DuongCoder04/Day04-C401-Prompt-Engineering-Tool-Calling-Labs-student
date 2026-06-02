---
name: check_weather
track: bonus
kind: live_api
provider: Open-Meteo (no API key required)
requires_env: []
inputs: [city, unit]
outputs: [items]
side_effect: false
---
# check_weather

Lấy thông tin thời tiết hiện tại của một thành phố. Dùng Open-Meteo API (miễn phí, không cần API key).

- `city`: tên thành phố (ví dụ: "Hanoi", "Ho Chi Minh City", "New York").
- `unit`: đơn vị nhiệt độ — `celsius` hoặc `fahrenheit` (mặc định celsius).

## Ví dụ

```
weather(city="Hanoi")
weather(city="New York", unit="fahrenheit")
```
