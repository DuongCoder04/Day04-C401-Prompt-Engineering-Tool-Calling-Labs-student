# 🔍 Research Agent — Group 42 Showcase

> **VinUni AI20k — Day 04 Lab: Prompt Engineering & Tool Calling**

---

## 🎯 Dự án là gì?

Chúng tôi build một **Research Agent** — một trợ lý AI có khả năng tự chọn công cụ phù hợp để trả lời yêu cầu của người dùng, thay vì chỉ trả lời bằng kiến thức có sẵn.

**Điểm khác biệt với chatbot thông thường:**

| Chatbot thường | Research Agent của chúng tôi |
|---|---|
| Chỉ trả lời từ kiến thức có sẵn | Gọi API thực để lấy dữ liệu thật |
| Không biết hôm nay là thứ mấy | Lấy tin tức thật thời gian thực |
| Không thể gửi tin nhắn | Gửi được lên Telegram |
| Trả lời mọi câu hỏi dù thiếu thông tin | Hỏi lại khi thiếu thông tin cần thiết |

---

## 🏗️ Kiến trúc hệ thống

```
Người dùng
    │
    ▼
┌─────────────────┐
│   Streamlit UI  │  ← Giao diện web (localhost:8501)
└────────┬────────┘
         │
    ▼
┌─────────────────┐
│  Research Agent │  ← Não của hệ thống
│  (gpt-oss-120b) │    Quyết định dùng tool nào
└────────┬────────┘
         │
    ┌────┴────────────────────────────────┐
    │         13 Tools (Công cụ)          │
    ├─────────────────────────────────────┤
    │ 🌐 lookup        → Tìm web (Tavily) │
    │ 🐦 timeline      → Tweet 1 người   │
    │ 🔍 social_search → Tweet theo chủ đề│
    │ 🔗 fetch         → Đọc URL (Firecrawl)│
    │ 📋 format        → Tạo digest       │
    │ ❓ clarify       → Hỏi lại user     │
    │ 📨 send          → Gửi Telegram     │
    │ 📜 policy        → Tra policy nội bộ│
    │ 📄 papers        → Tìm paper arXiv  │
    │ 📖 paper_text    → Đọc PDF arXiv    │
    │ 💰 get_crypto_prices → Giá coin thật│
    │ 🌤️ check_weather → Thời tiết thật   │
    │ ✍️ summarize     → Tóm tắt bằng AI  │
    └─────────────────────────────────────┘
```

---

## ✨ Tính năng nổi bật

### 1. Tool Calling thông minh
Agent tự quyết định dùng tool nào, không cần user chỉ định:

```
User: "Tin AI hôm nay có gì?"
→ Agent tự gọi: lookup(query="AI", topic="news", timeframe="day")
→ Trả về 5 bài báo AI thật từ Tavily
```

### 2. Clarify khi thiếu thông tin
Agent không đoán bừa — hỏi lại khi cần:

```
User: "Tóm tắt 5 tweet mới nhất"
→ Agent: "Bạn muốn xem tweet của ai?"  ← hỏi lại
User: "Của Elon Musk"
→ Agent gọi: timeline(screenname="elonmusk", limit=5)
```

### 3. Confirmation guard trước khi hành động
Agent không tự ý gửi tin — luôn xin phép trước:

```
User: "Đăng tin này lên Telegram"
→ Agent: "Bạn có muốn gửi không?" [Có] [Không]
User: nhấn [Có]
→ Agent gọi: send(confirmed=True, text=...)
→ Tin nhắn đến Telegram ✅
```

### 4. Multi-turn context
Agent nhớ context qua nhiều lượt hội thoại:

```
Turn 1: "Tìm tweet về AI"  → social_search(query="AI")
Turn 2: "Bỏ Twitter, tìm web đi"
Turn 3: "Vẫn về AI nhé"   → lookup(query="AI")  ← switch tool, giữ query
```

---

## 📊 Kết quả đo lường (Evidence-Based)

Chúng tôi chạy **eval tự động** trên 20 test cases chuẩn, đo 4 chỉ số:

```
Baseline (v0) — prompt xấu cố ý:
  Case accuracy:    57.9%
  Routing accuracy: 78.9%
  Argument accuracy:57.9%
  Multiturn:        60.0%

Final (v3-final) — sau 5 vòng tối ưu:
  Case accuracy:    94.7%  ← +36.8%
  Routing accuracy: 94.7%  ← +15.8%
  Argument accuracy:94.7%  ← +36.8%
  Multiturn:       100.0%  ← +40.0% 🎯
```

### Quá trình tối ưu (5 vòng có hypothesis)

```
v0 ──── 57.9% ──── Baseline (prompt xấu cố ý)
  └─ Vấn đề: agent đoán bừa khi thiếu info
v1 ──── 66.7% ──── Fix clarify rules (+8.8%)
  └─ Vấn đề: gửi Telegram không confirm + over-clarify
v2 ──── 57.9% ──── Thêm send rule → regression
  └─ Vấn đề: query bloat + handle mapping sai
v3 ──── 88.2% ──── Fix tools.yaml descriptions (+30.3%)
  └─ Vấn đề: send confirmed=True chưa đúng
v3-final 94.7% ── Final polish (+6.5%) ✅
```

---

## 🛠️ Stack kỹ thuật

| Layer | Technology |
|---|---|
| **LLM** | OpenRouter → `openai/gpt-oss-120b:free` |
| **Web search** | Tavily API |
| **URL scraping** | Firecrawl API |
| **Twitter** | RapidAPI Twitter API45 |
| **Crypto prices** | RapidAPI crypto-news51 |
| **Weather** | Open-Meteo (free, no key) |
| **Telegram** | Telegram Bot API |
| **arXiv papers** | arXiv API + pypdf |
| **UI** | Streamlit |
| **Eval framework** | Custom `run_eval.py` |

---

## 🖥️ Giao diện Streamlit

```
┌─────────────────────────────────────────────────────────┐
│ Sidebar                │  Chat Area                      │
│ ─────────────────────  │  ──────────────────────────     │
│ 🟢 clarify  ×2         │  [Tin tức AI nổi bật hôm nay]  │
│ 🟢 lookup   ×3         │                                 │
│ ⚫ timeline             │  🌐 lookup  query=AI  topic=news│
│ ⚫ send                 │  ↳ 5 results (expand)           │
│                        │                                 │
│ Turns:  8              │  🤖 Đây là 5 tin AI nổi bật...  │
│ Calls: 12              │                                 │
│                        │  👤 Gửi lên Telegram nhé        │
│ [🗑 Clear chat]        │                                 │
│                        │  ❓ clarify  response_type=yes_no│
│                        │                                 │
│                        │  ⏳ Agent đang chờ xác nhận:    │
│                        │  [✅ Có]  [❌ Không]             │
│                        │                                 │
│                        │  [Nhập yêu cầu...       Send]   │
└────────────────────────┴─────────────────────────────────┘
```

**Features của UI:**
- 🌑 Dark theme (#0f1117)
- 📌 Input sticky bottom (`st.chat_input`)
- 🏷️ Tool call badges inline (`🌐 lookup  query=AI`)
- 📂 Expandable tool results
- 🔘 Yes/No buttons thay vì text khi agent hỏi confirm
- 💡 Suggestion chips khi chat trống
- 📊 Tool activity tracker trong sidebar

---

## 📁 Cấu trúc dự án

```
starter_v0/
├── app.py                  ← Streamlit UI
├── agent.py                ← Core agent (one-shot)
├── chat.py                 ← Interactive chat + transcript
├── run_eval.py             ← Automated evaluation
├── artifacts/
│   ├── system_prompt.md    ← Prompt đã tối ưu 5 vòng
│   ├── tools.yaml          ← Tool declarations (13 tools)
│   ├── version_log.csv     ← Lịch sử tối ưu v0→v3-final
│   └── REPORT.md           ← Báo cáo đầy đủ
├── tools/                  ← 13 tool implementations
│   ├── lookup/             ← Tavily web search
│   ├── timeline/           ← Twitter timeline
│   ├── social_search/      ← Twitter search
│   ├── fetch/              ← Firecrawl URL reader
│   ├── format/             ← Markdown digest renderer
│   ├── clarify/            ← User clarification
│   ├── send/               ← Telegram sender
│   ├── policy/             ← Company policy KB
│   ├── papers/             ← arXiv search
│   ├── paper_text/         ← arXiv PDF reader
│   ├── get_crypto_prices/  ← NEW: Crypto prices
│   ├── check_weather/      ← NEW: Weather (no key)
│   └── summarize/          ← NEW: LLM summarizer
├── data/
│   ├── eval_base.json      ← 20 test cases chuẩn
│   └── eval_group.json     ← 15 team test cases
├── runs/                   ← Eval results (JSON)
└── transcripts/            ← Live chat logs (JSON)
```

---

## 🎬 Demo Scenarios

### Scenario A — Tin tức + Gửi Telegram
```
You: Tìm tin AI hôm nay
→ 🌐 lookup(AI, news, day) → 5 bài báo thật

You: Gửi tóm tắt lên Telegram
→ ❓ clarify(yes_no): "Bạn có muốn gửi không?"

You: Có
→ 📨 send(confirmed=True, text=...) → ✅ Đến Telegram
```

### Scenario B — Twitter Research
```
You: Lấy 3 tweet của Elon Musk về AI
→ 🐦 timeline(elonmusk, limit=3) → Real tweets
→ Kết quả: không có tweet về AI → Agent thông báo thật
```

### Scenario C — Crypto + Weather (New Tools)
```
You: Giá BTC hôm nay là bao nhiêu?
→ 💰 get_crypto_prices(symbols=["BTC"]) → $89,386 ▲0.18%

You: Thời tiết Hà Nội hôm nay?
→ 🌤️ check_weather(city="Hanoi") → 35°C, Thunderstorm
```

---

## 👥 Team

| Thành viên | Role |
|---|---|
| Nguyen Van Duong | Lead developer, agent architecture |
| Nguyen Tuan Dung | Prompt engineering, eval analysis |
| Nguyen Nhat Quang | Tool implementation, testing |
| Phung Huu Uy | UI/UX, Streamlit frontend |
| Nguyen Quang Minh | Eval cases design, documentation |

---

*Group 42 — VinUni AI20k C401 — Day 04 Lab — June 2026*
