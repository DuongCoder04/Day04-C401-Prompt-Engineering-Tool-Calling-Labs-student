"""
Bridge script: receives a user message via CLI arg or stdin,
runs the ResearchAgent, and outputs JSON result to stdout.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def _resolve_root() -> Path:
    env = os.environ.get("PROJECT_ROOT")
    if env:
        return Path(env).resolve()
    here = Path(__file__).resolve().parent
    for candidate in [here.parent, here.parent.parent]:
        if (candidate / "chat.py").exists():
            return candidate
    return here.parent


ROOT = _resolve_root()
sys.path.insert(0, str(ROOT))

from env_loader import load_lab_env
load_lab_env(ROOT)

from agent import ResearchAgent
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools


def _get_message() -> str:
    if "--message" in sys.argv:
        idx = sys.argv.index("--message")
        return sys.argv[idx + 1] if idx + 1 < len(sys.argv) else ""
    return sys.stdin.read().strip()


def main() -> None:
    message = _get_message()
    if not message:
        print(json.dumps({"error": "No message provided"}, ensure_ascii=False))
        sys.exit(1)

    artifacts_dir = ROOT / "artifacts"
    system_prompt = (artifacts_dir / "system_prompt.md").read_text(encoding="utf-8")
    tool_declarations = load_tool_declarations(artifacts_dir / "tools.yaml")
    openai_tools = to_openai_tools(tool_declarations)

    provider_name = "openrouter"
    provider = make_provider(provider_name)
    agent = ResearchAgent(
        provider=provider,
        system_prompt=system_prompt,
        tools=openai_tools,
        model=None,
    )

    try:
        run = agent.run([{"role": "user", "content": message}], tool_choice=None)
    except Exception as exc:
        print(json.dumps({
            "error": f"{type(exc).__name__}: {str(exc)}",
        }, ensure_ascii=False))
        sys.exit(1)

    result = {
        "assistant_text": run.text or "",
        "tool_calls": [
            {"name": call.name, "args": call.args} for call in run.tool_calls
        ],
        "tool_results": run.tool_results,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
