---
name: get_crypto_prices
track: bonus
kind: live_api
provider: RapidAPI crypto-news51
requires_env: [RAPIDAPI_KEY, RAPIDAPI_CRYPTO_HOST]
inputs: [symbols, base_currency, limit]
outputs: [items]
side_effect: false
---
# get_crypto_prices

Lấy giá crypto realtime từ RapidAPI crypto-news51. Trả về danh sách coin với giá, thay đổi 24h, và market cap.

- `symbols`: danh sách ký hiệu coin (ví dụ: ["BTC", "ETH"]). Nếu để trống sẽ trả về top coins theo rank.
- `base_currency`: tiền tệ cơ sở (mặc định USD).
- `limit`: số coin cần lấy (mặc định 5, tối đa 20).

## Ví dụ

```
crypto_price(symbols=["BTC", "ETH"])
crypto_price(limit=10)
crypto_price(symbols=["BTC"], base_currency="USD")
```
