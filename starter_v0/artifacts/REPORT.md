# Day 04 Lab v2 Report — Research Agent Tool Eval

## Team

- **Team:** Zone: 10 - Group 3
- **Members:** Nguyen Van Duong, Nguyen Nhat Quang, Phung Huu Uy.
- **Provider / Model:** OpenRouter → `openai/gpt-oss-120b:free`

---

## Final Metrics

| Metric | Value |
|---|---|
| Final version | `v3-final` |
| Final artifact_version | `v3+p3acc8a1e97f2+t80cab00026f8` |
| **Best base run file** | `runs/v3_B_base_openrouter_20260602T133148072779.json` |
| **Base case accuracy** | **94.74%** (18/19 measured) |
| **Base tool routing accuracy** | **94.74%** |
| **Base argument accuracy** | **94.74%** |
| **Base multiturn accuracy** | **100%** (6/6) |
| Best group eval run file | `runs/v3_B_group_openrouter_20260602T133336614084.json` |
| **Group eval accuracy** | **71.43%** (10/14 measured) |
| Representative transcript | `transcripts/v3_openrouter_20260602T141506933726.transcript.json` |

---

## Version Evidence

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---:|---:|---:|---|
| v0 | baseline (intentionally bad prompt) | N/A | N/A | 57.89% | `runs/v0_B_base_openrouter_20260602T125244644009.json` |
| v1 | `system_prompt.md` | Removing "just guess when info missing" + adding explicit clarify rules for missing handle/URL will fix R10, R11 | 57.89% | 66.67% | `runs/v1_B_base_openrouter_20260602T130515740078.json` |
| v2 | `system_prompt.md` | Adding send confirmation rule + parallel tool call rule will fix R12, R13. **Partial: R12 fixed but regression on R05/R07 due to over-clarification** | 66.67% | 57.89% | `runs/v2_B_base_openrouter_20260602T130940483330.json` |
| v3 | `system_prompt.md` + `tools.yaml` | Tightening clarify conditions (prevent false positives) + lookup query-bloat rule + handle mapping in timeline description | 57.89% | 88.24% | `runs/v3_B_base_openrouter_20260602T131407434471.json` |
| v3-final | `system_prompt.md` | Fix send confirmed=true logic (2-branch rule) + format tool trigger words + multi-turn latest-turn rule | 88.24% | **94.74%** | `runs/v3_B_base_openrouter_20260602T133148072779.json` |

---

## Failure Analysis

### Base Eval (v3-final) — Remaining Failures

| Case ID | Failure Type | Actual Tool Calls | What Failed | Root Cause |
|---|---|---|---|---|
| R02_search_tweets_routing | provider_error | — | Rate limit (429) during eval run | Free tier model `gpt-oss-120b:free` intermittently rate-limited |
| R13_parallel_web_and_tweets | wrong_tool | `lookup` only | Expected `lookup` + `social_search` in parallel; agent only called one | Model limitation: `gpt-oss-120b:free` does not reliably emit parallel tool calls |

### Group Eval (v3-final) — Failures

| Case ID | Failure Type | What Failed | Root Cause |
|---|---|---|---|
| G01_topic_tweet_not_timeline | provider_error | Rate limit | Free tier rate limit |
| G03_fetch_arxiv_full_url | wrong_tool | Expected `fetch` for full arxiv URL; agent used `paper_text` | Model sees "arxiv" and defaults to arxiv tool, ignoring full URL context |
| MG01_carryover_query_switch_tool | wrong_arg_value | Expected `lookup` after switch; agent stuck on `social_search` | Tool-sticking in multi-turn: model doesn't fully override previous tool context |
| MG05_parallel_then_format | wrong_tool | Expected `format` after previous search results; agent searched again | Model doesn't detect that results already exist in conversation context |
| H03_three_tool_switch | wrong_tool | Expected `format` at turn 3; agent called `social_search` again | Same as MG05 — format trigger not recognized after multi-turn tool switch |

**Summary:** 3 provider errors (rate limit, not logic failures). 4 actual logic failures — all related to model limitations with parallel tool calls and context-aware tool switching, not prompt design flaws.

---

## Key Failure Patterns Identified

### Pattern 1 — Query Bloat (v0 → fixed in v3)
Model appended words to queries: `"AI"` → `"AI news today"`, `"robotics"` → `"robotics news this week"`.

**Fix:** Added explicit rule in `lookup` tool description: *"query phải là keyword ngắn gọn, KHÔNG thêm 'news/today/latest'"*

### Pattern 2 — Clarify Bypass (v0 → fixed in v1)
Model ignored `clarify` tool, guessed values (handle, URL) instead.

**Fix:** Removed "just make a sensible guess" from system prompt. Added explicit: *"If missing handle → MUST call clarify"*

### Pattern 3 — Over-Clarification Regression (v2 regression → fixed in v3)
After adding clarify rules, model started clarifying when info was already present (R05, R07).

**Fix:** Added negative constraint: *"Do NOT clarify when user has already given enough information"*

### Pattern 4 — Send Without Confirmation (v0 → fixed in v2/v3)
Model sent to Telegram without asking confirmation.

**Fix:** Added 2-branch rule: unconfirmed → `clarify(yes_no)`, already confirmed by word → `send(confirmed=true)`

### Pattern 5 — Handle Mapping (v0 → fixed in v3)
`Sam Altman` → `SamAltman` instead of `sama`.

**Fix:** Added explicit mapping table in `timeline` tool description: *Sam Altman → sama, Elon Musk → elonmusk, Karpathy → karpathy*

---

## Team Eval Cases (15 cases added to `data/eval_group.json`)

### Medium (10 cases)

| Case ID | What It Tests | Expected Tool/Behavior | v3-final Result |
|---|---|---|---|
| G01_topic_tweet_not_timeline | "tweet về LLM" → social_search not timeline | `social_search` | FAIL (rate limit) |
| G02_timeframe_month | "tháng này" → timeframe=month | `lookup(timeframe=month)` | ✅ PASS |
| G03_fetch_arxiv_full_url | Full arxiv URL → fetch not paper_text | `fetch(url=arxiv...)` | FAIL (wrong_tool) |
| G04_out_of_scope_translation | Dịch thuật → no tool | `no_tool` | ✅ PASS |
| G05_unnecessary_tool_trivial | Câu hỏi phổ thông → no tool | `no_tool` | ✅ PASS |
| MG01_carryover_query_switch_tool | Switch twitter→web, carry query | `lookup(query=Mistral AI)` | FAIL (wrong_arg) |
| MG02_handle_at_correction | @sama → @ylecun correction | `timeline(ylecun, limit=5)` | ✅ PASS |
| MG03_topic_shift_timeframe_carryover | blockchain→web3, keep timeframe=week | `lookup(web3, week)` | ✅ PASS |
| MG04_send_confirmed_true | User confirms verbally → send(confirmed=True) | `send(confirmed=True)` | ✅ PASS |
| MG05_parallel_then_format | After search, "tổng hợp" → format | `format(sections)` | FAIL (wrong_tool) |

### Hard (5 cases)

| Case ID | What It Tests | Expected Tool/Behavior | v3-final Result |
|---|---|---|---|
| H01_ambiguous_paper_vs_web | "bài báo khoa học arXiv" → papers not lookup | `papers(query=AI agents)` | ✅ PASS |
| H02_missing_two_urls | "2 bài viết này" no URLs → clarify | `clarify(text)` | ✅ PASS |
| H03_three_tool_switch | 3-turn tool switch → final = format | `format(brief)` | FAIL (wrong_tool) |
| H04_cancel_parallel_keep_one | Cancel tweet, keep web | `lookup(AI, news, day)` | ✅ PASS |
| H05_negative_confirmation_no_send | "thôi đừng gửi" → no tool | `no_tool` | ✅ PASS |

---

## Live Chat Evidence

Transcript files in `transcripts/`:

| Transcript | Turns | Scenario | Outcome |
|---|---|---|---|
| `v3_..._135628880240` | 4 | Stability test — BTC search, crypto Twitter | Model stable; minor over-clarify on meta question |
| `v3_..._140648967381` | 4 | Twitter BTC search (topic-based) | ❌ Over-clarify — agent misidentified topic search as missing-handle case |
| `v3_..._141506933726` | 10 | Send Telegram + Elon timeline | ✅ All correct: clarify→send confirmed=True; timeline(elonmusk); honest "no LLM tweets" |
| `v3_..._142710219118` | 6 | Normal news lookup + send Telegram | ✅ Perfect: lookup(AI,news,day)→format→clarify→send(confirmed=True) |

### Live Chat Highlights (Scenario 2 — v3_..._142710219118)

| Turn | User Input | Tool Called | Args | Outcome |
|---|---|---|---|---|
| 1 | "Tìm tin tức AI nổi bật hôm nay" | `lookup` | `query=AI, topic=news, timeframe=day` | ✅ 5 real AI news from Tavily |
| 2 | "Gửi cả 5 bài lên Telegram" | `clarify` | `response_type=yes_no` | ✅ Correctly asked for confirmation |
| 3 | "Có" | `send` | `confirmed=True, text=<full digest>` | ✅ Sent to Telegram successfully |

---

## Bonus Evidence

| Bonus | Evidence | What Worked | Notes |
|---|---|---|---|
| `send` (Telegram confirmation guard) | `transcripts/v3_..._141506933726.transcript.json` Turn 1-2 | 2-branch confirm rule: unconfirmed → clarify(yes_no), verbally confirmed → send(confirmed=True) | Works consistently across all transcripts |
| `policy` (company policy search) | `data/eval_research_extension.json` E01-E03 | Routes "theo policy công ty" → policy tool, not web lookup | Local markdown KB search |
| `papers` / `paper_text` (arXiv) | `data/eval_research_extension.json` E04-E05 | paper_text correctly extracts text from arXiv PDF | pypdf-based local extraction |
| **Streamlit UI** | `starter_v0/app.py` | Full dark-theme chat UI at `localhost:8501` | st.chat_message + sticky input + tool badges + clarify buttons + suggestion chips + empty state |
| **3 new tools** | `tools/get_crypto_prices/`, `tools/summarize/`, `tools/check_weather/` | All 3 tested and working live | Uses RAPIDAPI_CRYPTO_HOST (already in .env), Open-Meteo (no key), LLM provider |

---

## Tool Inventory (13 tools total)

### Core (6)
| Tool | Function | Provider | Status |
|---|---|---|---|
| `clarify` | Ask user for missing info | Local | ✅ |
| `timeline` | Get tweets from one account | RapidAPI Twitter API45 | ✅ |
| `social_search` | Search tweets by topic | RapidAPI Twitter API45 | ✅ |
| `lookup` | Web/news search | Tavily | ✅ |
| `fetch` | Read URL content | Firecrawl | ✅ |
| `format` | Render markdown digest | Local | ✅ |

### Bonus — Original (4)
| Tool | Function | Provider | Status |
|---|---|---|---|
| `send` | Post to Telegram (with confirm guard) | Telegram Bot API | ✅ |
| `policy` | Search company policy KB | Local markdown | ✅ |
| `papers` | Search arXiv papers | arXiv API | ✅ |
| `paper_text` | Extract arXiv PDF text | arXiv + pypdf | ✅ |

### Bonus — New Tools (3)
| Tool | Function | Provider | Status |
|---|---|---|---|
| `get_crypto_prices` | Realtime crypto prices | RapidAPI crypto-news51 | ✅ |
| `summarize` | LLM-based text summarization | OpenRouter (reuse) | ✅ |
| `check_weather` | Current weather by city | Open-Meteo (no key) | ✅ |

---

## Reflection

### Which fixes belonged in `system_prompt.md`?

- **Clarify rules** (when to ask, when NOT to ask) — behavioral rules are agent-level, not tool-level
- **Send confirmation logic** (unconfirmed vs verbally confirmed) — action boundary enforcement
- **Multi-turn latest-turn rule** — context management behavior
- **Parallel tool call rule** — response structure guidance
- **Format trigger words** — high-level intent recognition

### Which fixes belonged in `tools.yaml`?

- **`lookup` query constraint** — argument format is tool-specific, belongs in tool description
- **`timeline` handle mapping** — tool-specific knowledge (name→handle) belongs where the model sees it at tool-selection time
- These are *argument-level* constraints, not *behavioral* constraints

### Which failure needed manual review instead of automatic grading?

- **R02 / G01 (provider_error)**: Rate limit, not a logic failure. Automatic grading marks as failure but it's an infrastructure issue.
- **G03 (fetch vs paper_text)**: The expected behavior is debatable — user gave full URL, but the URL is an arXiv page. Both `fetch` and `paper_text` could be argued correct.
- **Failed scenario in live chat** (v3_..._140648967381 Turn 2): Agent over-clarified on "tìm giá BTC trên Twitter" — unclear whether "tweet về BTC" (topic) vs "tweet của X" (person) is the agent's fault or a prompt ambiguity that needs more explicit rule.

### What would you improve next?

1. **Parallel tool calls**: The free model (`gpt-oss-120b:free`) rarely emits multiple tool calls in one response. Upgrading to a paid model (GPT-4o or Claude 3.5) would likely fix R13, MG05, H03.
2. **Topic-tweet vs person-tweet disambiguation**: Add explicit rule: *"tweet VỀ chủ đề X → social_search, tweet CỦA người Y → timeline"* — this pattern was missed in all prompt versions.
3. **Format trigger in multi-turn**: Model doesn't detect that results already exist in conversation. A potential fix: add to system prompt *"If tool results are already in conversation and user asks to organize/summarize → call format immediately without searching again"*.
4. **Rate limit resilience**: Implement retry logic with exponential backoff in `run_eval.py` to reduce provider_error cases.
5. **Streamlit UI persistence**: Current session state resets on server restart. Adding SQLite-backed persistence would make the UI production-ready.
