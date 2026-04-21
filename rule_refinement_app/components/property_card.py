"""Five-property display for the selected data element."""

from __future__ import annotations

import streamlit as st


def _field_card(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="dq-card dq-animate-in">
            <div class="dq-label">{_escape_html(label)}</div>
            <div class="dq-value">{_escape_html(value)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_readonly_properties(element: dict[str, str]) -> None:
    """Render CDE Name, Definition, Rule Title, and Rule Dimension as stacked cards."""
    _field_card("CDE Name", element["cde_name"])
    _field_card("CDE Definition", element["cde_definition"])
    _field_card("Rule Title", element["rule_title"])
    _field_card("Rule Dimension", element["rule_dimension"])


def render_rule_text_area(default_text: str, key: str) -> str:
    """Editable business rule text; returns current widget value."""
    return st.text_area(
        "Rule Text (Editable)",
        value=default_text,
        height=220,
        key=key,
        label_visibility="visible",
    )
