from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from providers.base import Provider, ToolCall
from tools import TOOL_FUNCTIONS


@dataclass
class AgentRun:
    text: str | None
    tool_calls: list[ToolCall] = field(default_factory=list)
    tool_results: list[dict[str, Any]] = field(default_factory=list)


class ResearchAgent:
    def __init__(
        self,
        provider: Provider,
        *,
        system_prompt: str,
        tools: list[dict[str, Any]] | None = None,
        model: str | None = None,
    ) -> None:
        self.provider = provider
        self.system_prompt = system_prompt
        self.tools = tools or []
        self.model = model

    def run(self, user_messages: list[dict[str, str]], *, tool_choice: Any | None = None) -> AgentRun:
        messages = [{"role": "system", "content": self.system_prompt}, *user_messages]
        response = self.provider.complete(
            messages,
            self.tools,
            model=self.model,
            temperature=0.0,
            tool_choice=tool_choice,
        )
        results: list[dict[str, Any]] = []
        all_tool_calls: list[ToolCall] = []
        for call in response.tool_calls:
            func = TOOL_FUNCTIONS.get(call.name)
            if not func:
                results.append({"tool_call_id": call.id, "tool": call.name, "error": "unknown_tool"})
                continue
            try:
                result = func(**call.args)
            except Exception as exc:  # keep eval robust; failures are evidence
                result = {"error": type(exc).__name__, "message": str(exc)}
            results.append({"tool_call_id": call.id, "tool": call.name, "args": call.args, "result": result})
            all_tool_calls.append(call)

        text = response.text
        if results:
            messages.append({"role": "assistant", "content": response.text or "", "tool_calls": [{"id": c.id, "type": "function", "function": {"name": c.name, "arguments": json.dumps(c.args, ensure_ascii=False)}} for c in all_tool_calls]})
            for tr in results:
                messages.append({"role": "tool", "tool_call_id": tr["tool_call_id"], "content": json.dumps(tr.get("result", {"error": tr.get("error", "unknown")}), ensure_ascii=False)})
            response2 = self.provider.complete(
                messages,
                self.tools,
                model=self.model,
                temperature=0.0,
            )
            text = response2.text

        return AgentRun(text=text, tool_calls=all_tool_calls, tool_results=results)
