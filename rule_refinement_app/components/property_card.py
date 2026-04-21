"""Data element property display — compact 2×2 grid + editable rule text area."""

from __future__ import annotations

import streamlit as st


def _escape(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _field_card(label: str, value: str) -> None:
    """Single property cell rendered via its own st.markdown call."""
    st.markdown(
        f'<div class="dq-prop-cell dq-animate-in">'
        f'<div class="dq-label">{_escape(label)}</div>'
        f'<div class="dq-value" style="font-size:0.82rem;line-height:1.4;">{_escape(value)}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_readonly_properties(element: dict[str, str]) -> None:
    """Render the 4 read-only fields as a native 2×2 Streamlit column grid."""
    col_left, col_right = st.columns(2, gap="small")

    with col_left:
        _field_card("CDE Name", element["cde_name"])
        _field_card("Rule Title", element["rule_title"])

    with col_right:
        _field_card("Rule Dimension", element["rule_dimension"])
        _field_card("CDE Definition", element["cde_definition"])


def render_rule_text_area(default_text: str, key: str) -> str:
    """Editable business rule text; returns the current widget value."""
    return st.text_area(
        "Rule Text (Editable)",
        value=default_text,
        height=155,
        key=key,
        label_visibility="visible",
    )
