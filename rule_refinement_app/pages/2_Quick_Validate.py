"""Quick Validate — element selector + icon validate button + result popup."""

from __future__ import annotations

import time
from datetime import datetime
from typing import Any

import streamlit as st

from components.property_card import render_readonly_properties, render_rule_text_area
from data.mock_elements import MOCK_DATA_ELEMENTS
from mock_llm import mock_checkpoint_evaluation, mock_rule_refinement
from styles import APP_CSS

# ── Extra CSS (defined first so page config block can reference it) ────────────

_EXTRA_CSS = """
/* Validate button — purple accent to distinguish from page 1 */
div[data-testid="stButton"] > button[kind="primary"] {
  background: linear-gradient(90deg,#6C3DE0,#9B6DFF) !important;
  color: #fff !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
  box-shadow: 0 0 22px rgba(108,61,224,0.45) !important;
}

/* Approve button */
.qv-approve > div[data-testid="stButton"] > button {
  background: linear-gradient(90deg,#00A86B,#00E676) !important;
  color: #0B1929 !important; font-weight: 800 !important;
  border: none !important; border-radius: 10px !important;
}
/* Reject button */
.qv-reject > div[data-testid="stButton"] > button {
  background: rgba(255,82,82,0.08) !important;
  color: #FF5252 !important;
  border: 1px solid rgba(255,82,82,0.35) !important;
  border-radius: 10px !important;
}
/* Status badge row */
.qv-status { display:flex; align-items:center; gap:0.6rem;
  font-size:0.8rem; color:rgba(230,241,255,0.45); margin:0.3rem 0 0.1rem; }
"""

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Quick Validate — DQ Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(f"<style>{APP_CSS}{_EXTRA_CSS}</style>", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────

_DEFAULTS: dict[str, Any] = {
    "qv_selected":         None,
    "qv_rule_text":        "",
    "qv_modal_result":     None,
    "qv_show_modal":       False,
    "qv_last_summary":     None,
    "qv_pending_override": None,
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Helpers ───────────────────────────────────────────────────────────────────

def _escape(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _rerun() -> None:
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()  # type: ignore[attr-defined]


def _run_validation(element: dict[str, str], rule_text: str) -> None:
    """Run eval + refinement with a combined animated progress bar."""
    status = st.empty()
    bar    = st.progress(0.0)

    steps = [
        ("🔍 Sending rule to evaluation engine...",   0.10),
        ("⚙️ Running DQ Dimension Mapping check...",  0.28),
        ("📊 Analyzing dimension coverage...",         0.50),
        ("🧠 Generating rule refinements...",          0.72),
        ("✨ Applying improvements...",                0.90),
    ]

    with st.spinner("Validating rule…"):
        for msg, frac in steps:
            with status.container():
                st.markdown(
                    f'<div style="color:#9B6DFF;font-size:0.88rem;font-weight:500;">'
                    f'{msg}</div>',
                    unsafe_allow_html=True,
                )
            bar.progress(frac)
            time.sleep(0.55)

        try:
            eval_result = mock_checkpoint_evaluation(
                cde_name=element["cde_name"],
                cde_definition=element["cde_definition"],
                rule_title=element["rule_title"],
                rule_dimension=element["rule_dimension"],
                business_text=rule_text,
            )
        except Exception as exc:
            bar.empty(); status.empty()
            st.error(f"Evaluation error: {exc}")
            return

        try:
            ref_result = mock_rule_refinement(
                original_rule={**element, "business_text": rule_text},
                checkpoint_results=eval_result,
            )
        except Exception as exc:
            bar.empty(); status.empty()
            st.error(f"Refinement error: {exc}")
            return

    bar.progress(1.0)
    time.sleep(0.2)
    bar.empty()
    status.empty()

    summary = eval_result["checkpoint_evaluation"]["summary"]
    st.session_state.qv_last_summary = {
        "passed":    summary["passed"],
        "failed":    summary["failed"],
        "total":     summary["total_checkpoints"],
        "timestamp": datetime.now().strftime("%H:%M:%S"),
    }
    st.session_state.qv_modal_result = ref_result
    st.session_state.qv_show_modal   = True


# ── Shared dialog body (used by both @st.dialog and inline fallback) ──────────

def _render_dialog_body() -> None:
    result = st.session_state.qv_modal_result
    if not result:
        return

    ref            = result["rule_refinement"]
    improved: str | None   = ref.get("improved_business_text")
    suggested: dict | None = ref.get("suggested_rule")
    key_changes: list[str] = ref.get("key_changes", [])
    is_suggested           = bool(suggested and not improved)
    rule_text              = improved or (suggested.get("business_text") if suggested else "")

    badge_bg    = "linear-gradient(90deg,#FFD740,#FFA726)" if is_suggested else "linear-gradient(90deg,#9B6DFF,#00D4FF)"
    badge_label = "AI SUGGESTED" if is_suggested else "REFINED"
    card_border = "rgba(255,215,64,0.35)" if is_suggested else "rgba(155,109,255,0.35)"
    card_bg     = ("linear-gradient(135deg,rgba(255,215,64,0.06),rgba(0,212,255,0.04))"
                   if is_suggested else
                   "linear-gradient(135deg,rgba(108,61,224,0.08),rgba(0,212,255,0.05))")
    heading     = "Generated Rule" if is_suggested else "Improved Business Rule Text"

    # ── Rule text card ────────────────────────────────────────────────────────
    st.markdown(
        f'<div style="background:{card_bg};border:1px solid {card_border};'
        f'border-radius:14px;padding:1.1rem 1.2rem;position:relative;margin-bottom:0.85rem;">'
        f'<span style="position:absolute;top:-0.52rem;left:1rem;'
        f'background:{badge_bg};color:#0B1929;font-size:0.65rem;font-weight:800;'
        f'letter-spacing:0.12em;border-radius:4px;padding:0.12rem 0.52rem;">{badge_label}</span>'
        f'<div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:0.08em;'
        f'color:rgba(155,109,255,0.85);margin-bottom:0.45rem;">{heading}</div>'
        f'<div style="font-family:\'Space Mono\',monospace;font-size:0.875rem;'
        f'color:#E6F1FF;line-height:1.6;">{_escape(rule_text)}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Dimension chip + warning note (suggested only) ────────────────────────
    if is_suggested and suggested:
        dim  = suggested.get("dimension", "")
        note = suggested.get("note", "")
        if dim:
            st.markdown(
                f'<span style="background:rgba(0,212,255,0.1);color:#00D4FF;'
                f'border:1px solid rgba(0,212,255,0.3);border-radius:20px;'
                f'padding:0.18rem 0.72rem;font-size:0.78rem;font-weight:600;">'
                f'{_escape(dim)}</span>',
                unsafe_allow_html=True,
            )
        if note:
            st.markdown(
                f'<div style="margin-top:0.55rem;display:flex;gap:0.45rem;'
                f'align-items:flex-start;">'
                f'<span style="color:#FFD740;font-size:0.9rem;flex-shrink:0;">⚠</span>'
                f'<div style="color:rgba(255,215,64,0.78);font-size:0.8rem;line-height:1.5;">'
                f'{_escape(note)}</div></div>',
                unsafe_allow_html=True,
            )

    # ── Key changes ───────────────────────────────────────────────────────────
    if key_changes:
        rows = "".join(
            f'<div style="display:flex;gap:0.5rem;align-items:flex-start;margin-bottom:0.38rem;">'
            f'<span style="color:#00E676;flex-shrink:0;font-size:0.95rem;">✓</span>'
            f'<span style="color:rgba(230,241,255,0.8);font-size:0.86rem;">{_escape(c)}</span>'
            f'</div>'
            for c in key_changes
        )
        st.markdown(
            f'<div style="background:rgba(0,230,118,0.05);border:1px solid rgba(0,230,118,0.15);'
            f'border-radius:10px;padding:0.7rem 1rem;margin-bottom:0.7rem;">'
            f'<div style="font-size:0.67rem;text-transform:uppercase;letter-spacing:0.08em;'
            f'color:rgba(0,230,118,0.65);margin-bottom:0.45rem;">Key Changes</div>'
            f'{rows}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<hr style='margin:0.6rem 0;'/>", unsafe_allow_html=True)

    # ── Action buttons ────────────────────────────────────────────────────────
    col_a, col_r = st.columns(2, gap="medium")

    with col_a:
        st.markdown('<div class="qv-approve">', unsafe_allow_html=True)
        approve = st.button("✓  Approve & Apply", key="qv_approve_btn",
                            use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="qv-reject">', unsafe_allow_html=True)
        reject = st.button("✗  Reject", key="qv_reject_btn",
                           use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if approve:
        st.session_state.qv_pending_override = rule_text
        st.session_state.qv_rule_text        = rule_text
        st.session_state.qv_show_modal       = False
        st.session_state.qv_modal_result     = None
        _rerun()

    if reject:
        st.session_state.qv_show_modal   = False
        st.session_state.qv_modal_result = None
        _rerun()


# ── @st.dialog decorator (Streamlit ≥ 1.36) ──────────────────────────────────

_HAS_DIALOG = hasattr(st, "dialog")

if _HAS_DIALOG:
    @st.dialog("✨ Validation Result", width="large")
    def _show_dialog() -> None:
        _render_dialog_body()


# ════════════════════════════════════════════════════════════════════════════════
# UI
# ════════════════════════════════════════════════════════════════════════════════

# ── Header ────────────────────────────────────────────────────────────────────

st.markdown(
    """
    <div style="display:flex;align-items:center;gap:0.7rem;
      padding:0.3rem 0 0.65rem 0;
      border-bottom:1px solid rgba(155,109,255,0.18);margin-bottom:0.75rem;">
      <span style="font-size:1.6rem;line-height:1;flex-shrink:0;">⚡</span>
      <div>
        <div style="font-size:1.2rem;font-weight:800;color:#E6F1FF;
          letter-spacing:-0.01em;line-height:1.15;">Quick Validate</div>
        <div style="font-size:0.76rem;color:rgba(230,241,255,0.45);margin-top:0.05rem;">
          Select · edit · validate — results appear in a popup
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Element dropdown ──────────────────────────────────────────────────────────

element_options = ["— Select a data element —"] + list(MOCK_DATA_ELEMENTS.keys())
selected_label  = st.selectbox(
    "Data Element",
    options=element_options,
    index=0,
    label_visibility="collapsed",
)
selected = selected_label if selected_label != element_options[0] else None

if selected != st.session_state.qv_selected:
    st.session_state.qv_selected         = selected
    st.session_state.qv_rule_text        = MOCK_DATA_ELEMENTS[selected]["business_text"] if selected else ""
    st.session_state.qv_show_modal       = False
    st.session_state.qv_modal_result     = None
    st.session_state.qv_last_summary     = None
    st.session_state.qv_pending_override = None

if not selected:
    st.markdown(
        '<div class="dq-hero dq-animate-in dq-instruction" style="margin-top:0.5rem;">'
        'Select a data element above to begin.'
        '</div>',
        unsafe_allow_html=True,
    )
    st.stop()

element = MOCK_DATA_ELEMENTS[selected]

st.markdown("<hr style='margin:0.5rem 0 0.75rem;'/>", unsafe_allow_html=True)

# ── Input panel ───────────────────────────────────────────────────────────────

prop_col, rule_col = st.columns([5, 7], gap="large")

with prop_col:
    st.markdown(
        '<div class="dq-section-title" style="margin-top:0;">Element Properties</div>',
        unsafe_allow_html=True,
    )
    render_readonly_properties(element)

with rule_col:
    # Apply pending override BEFORE widget instantiation
    widget_key = f"qv_text_{selected}"
    if st.session_state.qv_pending_override is not None:
        st.session_state[widget_key]         = st.session_state.qv_pending_override
        st.session_state.qv_pending_override = None

    current_text = st.session_state.qv_rule_text
    new_text = render_rule_text_area(default_text=current_text, key=widget_key)
    if new_text != current_text:
        st.session_state.qv_rule_text = new_text

    st.markdown("<div style='height:0.3rem;'></div>", unsafe_allow_html=True)

    validate_clicked = st.button(
        "⚡  Validate Rule",
        key="qv_validate_btn",
        type="primary",
        use_container_width=True,
    )

# ── Last validation status strip ──────────────────────────────────────────────

if st.session_state.qv_last_summary:
    s        = st.session_state.qv_last_summary
    fail_col = "#FF5252" if s["failed"] else "rgba(230,241,255,0.28)"
    fail_bg  = "rgba(255,82,82,0.1)" if s["failed"] else "rgba(255,255,255,0.04)"
    st.markdown(
        f'<div class="qv-status">'
        f'<span>Last validated {s["timestamp"]}</span>'
        f'<span style="background:rgba(0,230,118,0.1);color:#00E676;'
        f'border-radius:4px;padding:0.06rem 0.48rem;font-weight:700;">✓ {s["passed"]} passed</span>'
        f'<span style="background:{fail_bg};color:{fail_col};'
        f'border-radius:4px;padding:0.06rem 0.48rem;font-weight:700;">✗ {s["failed"]} failed</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

st.markdown("<hr style='margin:0.65rem 0;'/>", unsafe_allow_html=True)

# ── Run validation ────────────────────────────────────────────────────────────

if validate_clicked:
    st.session_state.qv_show_modal   = False
    st.session_state.qv_modal_result = None
    _run_validation(element, st.session_state.qv_rule_text)

# ── Show result popup ─────────────────────────────────────────────────────────

if st.session_state.qv_show_modal and st.session_state.qv_modal_result:
    if _HAS_DIALOG:
        _show_dialog()
    else:
        # Inline fallback for Streamlit < 1.36
        st.markdown(
            """
            <style>
            .qv-backdrop{position:fixed;top:0;left:0;width:100%;height:100%;
              background:rgba(0,0,0,0.62);z-index:998;}
            </style>
            <div class="qv-backdrop"></div>
            """,
            unsafe_allow_html=True,
        )
        _, modal_col, _ = st.columns([1, 4, 1])
        with modal_col:
            st.markdown(
                '<div style="background:#112240;border:1px solid rgba(155,109,255,0.35);'
                'border-radius:16px;padding:1.5rem 1.5rem 0.75rem;margin-top:1rem;">'
                '<div style="font-size:1rem;font-weight:700;color:#E6F1FF;'
                'margin-bottom:1rem;">✨ Validation Result</div>',
                unsafe_allow_html=True,
            )
            _render_dialog_body()
            st.markdown("</div>", unsafe_allow_html=True)
