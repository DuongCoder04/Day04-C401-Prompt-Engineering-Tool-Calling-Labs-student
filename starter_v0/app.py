"""
Research Agent — Streamlit UI
Run: streamlit run app.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st

# ── path setup ───────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from env_loader import load_lab_env
load_lab_env(ROOT)

from providers import make_provider
from providers.base import ToolCall
from tools import TOOL_FUNCTIONS, load_tool_declarations, to_openai_tools

# ── constants ─────────────────────────────────────────────────────────────────
ARTIFACTS_DIR      = ROOT / "artifacts"
SYSTEM_PROMPT_PATH = ARTIFACTS_DIR / "system_prompt.md"
TOOLS_YAML_PATH    = ARTIFACTS_DIR / "tools.yaml"
VERSION            = "v3"
PROVIDER_NAME      = "openrouter"
MAX_TOOL_ROUNDS    = 4

TOOL_ICONS = {
    "clarify":       "❓",
    "timeline":      "🐦",
    "social_search": "🔍",
    "lookup":        "🌐",
    "fetch":         "🔗",
    "format":        "📋",
    "send":          "📨",
    "policy":        "📜",
    "papers":        "📄",
    "paper_text":    "📖",
}

SUGGESTIONS = [
    "Tin tức AI nổi bật hôm nay",
    "Tweet mới nhất của Sam Altman",
    "Tìm paper arXiv về LLM agents",
    "Tin crypto tuần này",
]

# ── page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS: dark theme + chat_message overrides + tool badge ─────────────────────
st.markdown("""
<style>
/* ── Base dark theme ── */
[data-testid="stAppViewContainer"]      { background: #0f1117; }
[data-testid="stSidebar"]               { background: #1a1d27; border-right: 1px solid #2e3250; }
[data-testid="stChatMessageContainer"]  { background: transparent; }

/* ── User bubble ── */
[data-testid="stChatMessage"][data-testid*="user"] .stMarkdown,
div[data-testid="stChatMessageContent"] {
    color: #e8eaf6;
}

/* User message bg */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: rgba(108, 99, 255, 0.12);
    border: 1px solid rgba(108, 99, 255, 0.25);
    border-radius: 12px;
    padding: 8px 12px;
    margin: 4px 0;
}

/* Assistant message bg */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: #1e2235;
    border: 1px solid #2e3250;
    border-radius: 12px;
    padding: 8px 12px;
    margin: 4px 0;
}

/* ── Tool badge ── */
.tool-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #12151f;
    border: 1px solid #2e3250;
    border-radius: 8px;
    padding: 5px 10px;
    font-size: 0.8rem;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    color: #7b82a8;
    margin: 3px 0;
}
.tool-badge .tn { color: #00d4aa; font-weight: 700; }
.tool-badge .ta { color: #ffd166; }
.tool-badge .tv { color: #e8eaf6; }

/* ── Suggestion chips ── */
.chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }
.chip {
    padding: 6px 14px;
    background: #22263a;
    border: 1px solid #2e3250;
    border-radius: 20px;
    font-size: 0.82rem;
    color: #7b82a8;
    cursor: pointer;
    transition: all 0.18s;
    white-space: nowrap;
}
.chip:hover { border-color: #6c63ff; color: #e8eaf6; background: rgba(108,99,255,0.1); }

/* ── Empty state ── */
.empty-state {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 60px 20px; text-align: center; gap: 12px;
    color: #7b82a8;
}
.empty-state .es-icon  { font-size: 52px; margin-bottom: 4px; }
.empty-state .es-title { font-size: 1.25rem; font-weight: 700; color: #e8eaf6; }
.empty-state .es-sub   { font-size: 0.9rem; max-width: 360px; line-height: 1.6; }

/* ── Sidebar labels ── */
.sec-label {
    font-size: 0.7rem; letter-spacing: 1px;
    text-transform: uppercase; color: #7b82a8;
    margin-bottom: 6px; margin-top: 2px;
}

/* ── Streamlit chat input dark ── */
[data-testid="stChatInput"] textarea {
    background: #1a1d27 !important;
    color: #e8eaf6 !important;
    border: 1px solid #2e3250 !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #7b82a8 !important; }
[data-testid="stChatInput"] button { background: #6c63ff !important; border-radius: 8px !important; }

/* ── Status dot ── */
.sdot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.sdot.on  { background: #06d6a0; }
.sdot.off { background: #2e3250; }
</style>
""", unsafe_allow_html=True)


# ── session state ─────────────────────────────────────────────────────────────
def _init():
    defaults = {
        "messages":         [],   # {role, content, tool_events}
        "history":          [],   # OpenAI-format context window
        "tool_stats":       {},   # tool_name → call count
        "awaiting_clarify": False,
        "clarify_type":     "text",
        "pending_input":    None, # chip click sets this
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()


# ── cached resources ──────────────────────────────────────────────────────────
@st.cache_resource
def _load():
    p  = make_provider(PROVIDER_NAME)
    td = load_tool_declarations(TOOLS_YAML_PATH)
    ot = to_openai_tools(td)
    sp = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    return p, ot, sp

provider, openai_tools, system_prompt = _load()


# ── helpers ───────────────────────────────────────────────────────────────────
def _exec_tool(call: ToolCall) -> dict:
    fn = TOOL_FUNCTIONS.get(call.name)
    if not fn:
        return {"tool": call.name, "error": "unknown_tool"}
    try:
        return {"tool": call.name, "args": call.args, "result": fn(**call.args)}
    except Exception as exc:
        return {"tool": call.name, "args": call.args, "error": str(exc)}


def _badge_html(name: str, args: dict) -> str:
    icon = TOOL_ICONS.get(name, "🔧")
    parts = []
    for k, v in list(args.items())[:4]:
        val = str(v)[:35] + ("…" if len(str(v)) > 35 else "")
        parts.append(f'<span class="ta">{k}</span>=<span class="tv">{val}</span>')
    args_html = " &nbsp; ".join(parts)
    return f'<div class="tool-badge">{icon} <span class="tn">{name}</span> &nbsp; {args_html}</div>'


def _render_tool_events(events: list[dict]):
    for ev in events:
        name   = ev.get("tool", "?")
        args   = ev.get("args", {})
        result = ev.get("result", {})
        error  = ev.get("error")

        st.markdown(_badge_html(name, args), unsafe_allow_html=True)

        if error:
            st.caption(f"⚠️ {error}")
        elif isinstance(result, dict) and not result.get("awaiting_user"):
            items = result.get("items", [])
            if items:
                with st.expander(f"↳ {name} — {len(items)} results", expanded=False):
                    for it in items[:5]:
                        title = it.get("title", "")[:100]
                        url   = it.get("url", "")
                        st.markdown(f"- [{title}]({url})" if url else f"- {title}")
            elif result.get("status") == "sent":
                st.caption("✅ Đã gửi Telegram")


def run_agent(user_text: str):
    """Run agent turn, append result to session state."""
    st.session_state.messages.append(
        {"role": "user", "content": user_text, "tool_events": []}
    )
    st.session_state.history.append({"role": "user", "content": user_text})
    if len(st.session_state.history) > 20:
        st.session_state.history = st.session_state.history[-20:]

    msgs = [
        {"role": "system", "content": system_prompt},
        *st.session_state.history[:-1],
        {"role": "user", "content": user_text},
    ]

    all_events: list[dict] = []
    agent_text = ""

    for _ in range(MAX_TOOL_ROUNDS):
        try:
            resp = provider.complete(msgs, openai_tools, temperature=0.0)
        except Exception as exc:
            agent_text = f"⚠️ Provider error: {exc}"
            break

        calls = resp.tool_calls
        if not calls:
            agent_text = resp.text or ""
            break

        waiting = False
        for call in calls:
            ev = _exec_tool(call)
            all_events.append(ev)
            st.session_state.tool_stats[call.name] = \
                st.session_state.tool_stats.get(call.name, 0) + 1

            res = ev.get("result", {})
            if isinstance(res, dict) and res.get("awaiting_user"):
                agent_text = res.get("question", "Bạn muốn làm gì tiếp theo?")
                st.session_state.awaiting_clarify = True
                st.session_state.clarify_type = call.args.get("response_type", "text")
                waiting = True
                break

        if waiting:
            break

        tool_dump = json.dumps(
            [e.get("result", {}) for e in all_events],
            ensure_ascii=False, default=str
        )[:8000]
        msgs.append({"role": "user", "content": f"TOOL_RESULTS_JSON:\n{tool_dump}"})

    st.session_state.messages.append(
        {"role": "assistant", "content": agent_text, "tool_events": all_events}
    )
    st.session_state.history.append({"role": "assistant", "content": agent_text})


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Research Agent")
    st.caption(f"Model: `openai/gpt-oss-120b:free` · v`{VERSION}`")
    st.divider()

    st.markdown('<div class="sec-label">Tool Activity</div>', unsafe_allow_html=True)
    for tool in TOOL_FUNCTIONS:
        count = st.session_state.tool_stats.get(tool, 0)
        icon  = TOOL_ICONS.get(tool, "🔧")
        dot   = '<span class="sdot on"></span>' if count else '<span class="sdot off"></span>'
        badge = f'`×{count}`' if count else ""
        st.markdown(
            f'{dot} {icon} **{tool}** {badge}',
            unsafe_allow_html=True,
        )

    st.divider()
    col1, col2 = st.columns(2)
    col1.metric("Turns",      len([m for m in st.session_state.messages if m["role"] == "user"]))
    col2.metric("Tool calls", sum(st.session_state.tool_stats.values()))
    st.divider()

    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages         = []
        st.session_state.history          = []
        st.session_state.tool_stats       = {}
        st.session_state.awaiting_clarify = False
        st.session_state.pending_input    = None
        st.rerun()


# ── MAIN ──────────────────────────────────────────────────────────────────────

# Empty state
if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <div class="es-icon">🔍</div>
        <div class="es-title">Research Agent</div>
        <div class="es-sub">
            Tôi có thể tìm tin tức, đọc URL, tìm tweet, tra cứu paper khoa học,
            và gửi digest lên Telegram. Hãy thử một trong các gợi ý bên dưới!
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Suggestion chips via buttons in columns
    cols = st.columns(len(SUGGESTIONS))
    for col, suggestion in zip(cols, SUGGESTIONS):
        with col:
            if st.button(suggestion, use_container_width=True):
                st.session_state.pending_input = suggestion
                st.rerun()

# Render chat history
for msg in st.session_state.messages:
    role = msg["role"]
    with st.chat_message(role, avatar="👤" if role == "user" else "🤖"):
        _render_tool_events(msg.get("tool_events", []))
        if msg["content"]:
            st.markdown(msg["content"])

# Clarify yes/no buttons
if st.session_state.awaiting_clarify and st.session_state.clarify_type == "yes_no":
    st.info("⏳ Agent đang chờ xác nhận:")
    c1, c2, _ = st.columns([1, 1, 4])
    with c1:
        if st.button("✅ Có", use_container_width=True, type="primary"):
            st.session_state.awaiting_clarify = False
            with st.spinner("Đang xử lý..."):
                run_agent("Có")
            st.rerun()
    with c2:
        if st.button("❌ Không", use_container_width=True):
            st.session_state.awaiting_clarify = False
            with st.spinner("Đang xử lý..."):
                run_agent("Không")
            st.rerun()

# Process chip click (set before rerun)
if st.session_state.pending_input:
    text = st.session_state.pending_input
    st.session_state.pending_input = None
    with st.spinner("Agent đang xử lý..."):
        run_agent(text)
    st.rerun()

# Sticky chat input
user_input = st.chat_input(
    "Nhập yêu cầu của bạn...",
    disabled=st.session_state.awaiting_clarify and st.session_state.clarify_type == "yes_no",
)
if user_input:
    with st.spinner("Agent đang xử lý..."):
        run_agent(user_input)
    st.rerun()
