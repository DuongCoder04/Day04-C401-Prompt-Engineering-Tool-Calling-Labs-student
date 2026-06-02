---
name: summarize
track: bonus
kind: local_formatter
provider: LLM provider (reuses existing provider)
requires_env: []
inputs: [text, style, max_words]
outputs: [summary]
side_effect: false
---
# summarize

Tóm tắt một đoạn văn bản dài bằng LLM. Dùng khi đã có nội dung từ fetch/paper_text và muốn rút gọn.

- `text`: văn bản cần tóm tắt.
- `style`: kiểu tóm tắt — `bullet` (danh sách gạch đầu dòng), `paragraph` (đoạn văn), `tldr` (1-2 câu).
- `max_words`: giới hạn số từ đầu ra (mặc định 150).

## Ví dụ

```
summarize(text="...", style="bullet", max_words=100)
summarize(text="...", style="tldr")
```
