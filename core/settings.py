from __future__ import annotations

import os

import streamlit as st


def get_setting(name: str, default: str = "") -> str:
    """Read config from environment first, then Streamlit secrets."""
    value = os.getenv(name)
    if value is not None:
        return value.strip()

    try:
        secret_value = st.secrets.get(name, default)
    except Exception:
        secret_value = default

    return str(secret_value).strip()
