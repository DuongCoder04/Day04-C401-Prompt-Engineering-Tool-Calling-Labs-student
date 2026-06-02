from __future__ import annotations

import os
from pathlib import Path


def load_dotenv(path: Path, *, override: bool = True) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key and (override or key not in os.environ):
            os.environ[key] = value


def _load_streamlit_secrets() -> bool:
    """Bridge st.secrets → os.environ so existing os.getenv() calls work on Streamlit Cloud."""
    try:
        import streamlit as st  # noqa: PLC0415
        secrets = st.secrets  # type: ignore[attr-defined]
        for key, value in secrets.items():
            if isinstance(value, str) and key not in os.environ:
                os.environ[key] = value
        return True
    except Exception:
        return False


def load_lab_env(root: Path) -> None:
    # 1. Streamlit Cloud secrets take priority when running on Cloud
    if _load_streamlit_secrets():
        return
    # 2. Explicit env file override
    external_path = os.getenv("DAY04_ENV_FILE")
    if external_path:
        load_dotenv(Path(external_path).expanduser())
        return
    # 3. Local .env file
    load_dotenv(root / ".env")
