# Day 04 Lab v2 Report — Research Agent

## Team

- Team: Zone 10 team 4
- Members: (sinh vien dien ten)
- Provider/model: openrouter / openai/gpt-4o-mini

## Final Metrics

- Final version: v3
- Final artifact_version: v3+p662cb2bcab8a+t73d9565a6dbf
- Best base run file: runs/v3_B_base_openrouter_20260602T130435117316.json
- Base case accuracy: 1.0 (20/20)
- Base tool routing accuracy: 1.0
- Base argument accuracy: 1.0
- Group eval run file: runs/v3_B_group_openrouter_20260602T130719439241.json
- Group eval accuracy: 0.7 (7/10)
- Chat transcript file: transcripts/v3_openrouter_20260602T130749786506.transcript.json

## Version Evidence

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Do hanh vi chua toi uu | - | 0.65 | runs/v0_B_base_openrouter_20260602T125116420428.json |
| v1 | system_prompt.md + tools.yaml | Prompt bao "dung hoi, cu doan" gay fail. Sua thanh "hoi lai khi thieu" + mo ta tool ro rang | 0.65 | 0.85 | runs/v1_B_base_openrouter_20260602T130009216701.json |
| v2 | system_prompt.md | Them rule "chi goi tool can thiet", "send yes_no", "bo Twitter thi dung goi social_search" | 0.85 | 0.90 | runs/v2_B_base_openrouter_20260602T130144098459.json |
| v3 | system_prompt.md | Rewrite gon hon, routing rules cu the cho tung tool, them vi du | 0.90 | 1.0 | runs/v3_B_base_openrouter_20260602T130435117316.json |

## Failure Analysis

### Baseline (v0) - 7 failures

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R03 | wrong_tool | lookup(query="AI news") | query sai "AI news" thay vi "AI", thieu topic | Mo ta tool: query la exact topic, khong them "news" |
| R08 | out_of_scope | send(text="nguyen ham...") | Goi send cho toan thay vi tu choi | Them rule: toan/lap trinh/van -> khong goi tool |
| R10 | missing_info | timeline(screenname="sama") | Doan bua handle thay vi clarify | Them rule: thieu handle/URL -> clarify, khong doan |
| R11 | missing_info | fetch(url="https://example.com") | Doan bua URL thay vi clarify | Them rule: khong co URL -> clarify |
| R12 | wrong_boundary | send(text=...) | Tu dong gui khong xac nhan | Them rule: send can confirm truoc |
| R13 | wrong_tool | lookup(query="AI news", thieu topic) | query sai + thieu topic | Mo ta tool: topic=news, query exact topic |
| R14 | out_of_scope | send(text="fibonacci code") | Goi send cho code thay vi tu choi | Them rule: coding -> khong goi tool |

### v1 -> v2 improvements (3 failures)

| Case ID | Failure Type | What Failed | Fix |
|---|---|---|---|
| R07 | wrong_arg_value | Goi them lookup khong can thiet | Rule: chi goi tool can thiet |
| R12 | wrong_boundary | clarify response_type="text" thay vi "yes_no" | Rule: send confirm phai dung yes_no |
| M06 | wrong_tool | Van goi social_search duoc bao "bo Twitter" | Rule: bo Twitter thi khong goi social_search |

### v2 -> v3 final (2 failures)

| Case ID | Failure Type | What Failed | Fix |
|---|---|---|---|
| R10 | missing_info | Goi social_search(query="tom tat") thay vi clarify | Rewrite prompt gon hon, routing rules tung tool |
| M06 | wrong_tool | Van goi social_search cung voi lookup | Them vi du cu the trong prompt |

## Team Eval Cases

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_papers_routing | Tim paper -> papers tool | papers(query="reinforcement learning") | PASS |
| G02_policy_routing | Hoi noi bo -> policy tool | policy(query="AI research", policy_area="ai_research") | PASS |
| G03_clarify_search_type | Chi noi "tweet ve AI" khong ro -> hoi lai | clarify(response_type="text") | FAIL |
| G04_lookup_and_papers | Can ca tin tuc + bai bao -> song song | lookup + papers | PASS |
| G05_out_of_scope_history | Lich su ngoai pham vi -> khong goi tool | no_tool | PASS |
| G06_multiturn_clarify_policy | 3 turns: lam ro policy_area | policy(area="tool_usage") | FAIL |
| G07_multiturn_paper_text | Tim paper -> doc text -> gioi han trang | paper_text | PASS |
| G08_multiturn_timeline_format | Lay tweet -> format bullet -> template brief | format(template="brief") | FAIL |
| G09_multiturn_two_accounts | 1 account thanh 2 account, moi account limit rieng | timeline(sama,5) + timeline(karpathy,7) | PASS |
| G10_multiturn_switch_from_offtopic | Turn 1 out-of-scope, turn 2 chuyen sang research | lookup(query="AI", topic="news", timeframe="day") | PASS |

## Live Chat Evidence

| Turn | User Request | Tool Calls | Outcome |
|---|---|---|---|
| 1 | Tim cho toi tin AI hom nay | lookup(query="AI", topic="news", timeframe="day") | Agent goi lookup dung, nhung API tra ve loi do thieu TAVILY_API_KEY |

## Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| arXiv/company policy | data/eval_group.json (G01, G02, G06, G07) | papers, policy, paper_text tools duoc routing dung trong eval | Policy Area can duoc lam ro qua nhieu turn |

## Reflection

- **system_prompt.md fixes**: Tat ca cac fix chinh deu thuoc prompt: routing rules, clarify khi thieu thong tin, refuse out-of-scope, send confirmation, multi-turn context.
- **tools.yaml fixes**: Mo ta tool ro rang hon, them vi du cu the, dat required fields chinh xac (lookup: query+topic, send: text+confirmed).
- **Manual review**: Group eval can xem xet thu cong vi agent co the chon tool dung nhung args sai tinh te (VD: response_type, policy_area).
- **What to improve next**: Them more specific examples cho tung tool, fine-tune prompt de group eval dat > 90%.
