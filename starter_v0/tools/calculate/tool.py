from __future__ import annotations

import math
import re
from typing import Any

from tools._shared import err


SAFE_GLOBALS = {
    "abs": abs, "round": round, "min": min, "max": max,
    "sum": sum, "pow": pow, "int": int, "float": float,
    "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "log": math.log, "log10": math.log10, "log2": math.log2,
    "exp": math.exp, "floor": math.floor, "ceil": math.ceil,
    "pi": math.pi, "e": math.e, "degrees": math.degrees, "radians": math.radians,
    "factorial": math.factorial,
}


def calculate(expression: str = "") -> dict[str, Any]:
    try:
        if not expression:
            raise ValueError("Missing expression")
        expr = expression.strip()
        expr = expr.replace("×", "*").replace("X", "*").replace("x", "*")
        expr = expr.replace("÷", "/").replace(":", "/")
        expr = re.sub(r"\s+", "", expr)
        cleaned = re.sub(r"[^0-9+\-*/.%() ,a-z^!]", "", expr)
        result = eval(cleaned, {"__builtins__": {}}, SAFE_GLOBALS)
        return {
            "tool": "calculate",
            "expression": expression,
            "result": result,
            "result_str": f"{result:,.4f}" if isinstance(result, float) else str(result),
        }
    except Exception as exc:
        return err("calculate", exc)
