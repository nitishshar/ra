"""DQ Rule Refinement Studio — main Streamlit application."""

from __future__ import annotations

import json
import time
from datetime import datetime
from typing import Any

import streamlit as st

from components.checkpoint_results import render_checkpoint_results
from components.property_card import render_readonly_properties, render_rule_text_area
from components.refinement_results import render_refinement_results
from data.mock_elements import MOCK_DATA_ELEMENTS
from mock_llm import mock_checkpoint_evaluation, mock_rule_refinement
from styles import APP_CSS

# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="DQ Rule Refinement Studio",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(f"<style>{APP_CSS}</style>", unsafe_allow_html=True)

# ── Session state defaults ────────────────────────────────────────────────────

DEFAULTS: dict[str, Any] = {
    "selected_element": None,
    "edited_business_text": "",
    "text_last_modified": None,
    "checkpoint_results": None,
    "refinement_results": None,
    "flow_stage": "selection",
    "session_history": [],
}
for k, v in DEFAULTS.items():
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


def _reset_results() -> None:
    st.session_state.checkpoint_results = None
    st.session_state.refinement_results = None
    st.session_state.flow_stage = "selection"


def _animated_progress(
    placeholder: Any,
    steps: list[tuple[str, float]],
    progress_bar: Any,
) -> None:
    """Drive progress bar + status messages through a list of (message, fraction) steps."""
    for message, fraction in steps:
        with placeholder.container():
            st.markdown(
                f'<div style="color:#00D4FF;font-size:0.95rem;font-weight:500;'
                f'padding:0.3rem 0;">{message}</div>',
                unsafe_allow_html=True,
            )
        progress_bar.progress(fraction)
        time.sleep(0.8)


def _run_evaluation(element: dict[str, str], business_text: str) -> None:
    """Run checkpoint evaluation with animated loading UI."""
    st.session_state.flow_stage = "evaluating"

    status_box = st.empty()
    bar = st.progress(0.0)

    steps: list[tuple[str, float]] = [
        ("🔍 Sending rule to evaluation engine...", 0.1),
        ("⚙️ Running DQ Dimension Mapping check...", 0.35),
        ("📊 Analyzing dimension coverage...", 0.65),
        ("✅ Finalizing checkpoint results...", 0.9),
    ]

    with st.spinner("Evaluating against checkpoints..."):
        _animated_progress(status_box, steps, bar)
        try:
            result = mock_checkpoint_evaluation(
                cde_name=element["cde_name"],
                cde_definition=element["cde_definition"],
                rule_title=element["rule_title"],
                rule_dimension=element["rule_dimension"],
                business_text=business_text,
            )
        except Exception as exc:
            bar.empty()
            status_box.empty()
            _show_error("Checkpoint evaluation failed", str(exc))
            st.session_state.flow_stage = "selection"
            return

    bar.progress(1.0)
    time.sleep(0.3)
    bar.empty()
    status_box.empty()

    st.session_state.checkpoint_results = result
    st.session_state.flow_stage = "checkpoint_done"

    summary = result["checkpoint_evaluation"]["summary"]
    st.session_state.session_history.append(
        {
            "element": element["cde_name"],
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "passed": summary["passed"],
            "failed": summary["failed"],
            "total": summary["total_checkpoints"],
        }
    )


def _run_refinement(element: dict[str, str], business_text: str) -> None:
    """Run rule refinement with animated loading UI."""
    st.session_state.flow_stage = "refining"

    status_box = st.empty()
    bar = st.progress(0.0)

    refine_steps: list[tuple[str, float]] = [
        ("🧠 Generating rule refinements...", 0.3),
        ("✨ Applying improvements...", 0.75),
    ]

    with st.spinner("Refining rule..."):
        _animated_progress(status_box, refine_steps, bar)
        original_rule = {**element, "business_text": business_text}
        try:
            ref_result = mock_rule_refinement(
                original_rule=original_rule,
                checkpoint_results=st.session_state.checkpoint_results,
            )
        except Exception as exc:
            bar.empty()
            status_box.empty()
            _show_error("Rule refinement failed", str(exc))
            st.session_state.flow_stage = "checkpoint_done"
            return

    bar.progress(1.0)
    time.sleep(0.3)
    bar.empty()
    status_box.empty()

    st.session_state.refinement_results = ref_result
    st.session_state.flow_stage = "complete"


def _show_error(title: str, detail: str) -> None:
    st.markdown(
        f"""
        <div style="
          background:rgba(255,82,82,0.1); border:1px solid rgba(255,82,82,0.35);
          border-radius:12px; padding:1rem 1.25rem; margin:0.75rem 0;">
          <div style="color:#FF5252;font-weight:700;margin-bottom:0.35rem;">⚠ {_escape(title)}</div>
          <div style="color:rgba(230,241,255,0.7);font-size:0.88rem;">{_escape(detail)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _build_export_payload() -> str:
    element_name = st.session_state.selected_element or ""
    element = MOCK_DATA_ELEMENTS.get(element_name, {})
    payload = {
        "element": element_name,
        "cde_name": element.get("cde_name", ""),
        "rule_dimension": element.get("rule_dimension", ""),
        "edited_business_text": st.session_state.edited_business_text,
        "checkpoint_results": st.session_state.checkpoint_results,
        "refinement_results": st.session_state.refinement_results,
        "exported_at": datetime.now().isoformat(),
    }
    return json.dumps(payload, indent=2)


# ── Sidebar: Session History ──────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        '<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.12em;'
        'text-transform:uppercase;color:#00D4FF;border-left:3px solid #00D4FF;'
        'padding-left:0.6rem;margin-bottom:0.75rem;">Session History</div>',
        unsafe_allow_html=True,
    )

    history = st.session_state.session_history
    if not history:
        st.markdown(
            '<div style="color:rgba(230,241,255,0.45);font-size:0.85rem;">'
            'No evaluations yet.</div>',
            unsafe_allow_html=True,
        )
    else:
        for entry in reversed(history):
            pass_color = "#00E676" if entry["failed"] == 0 else "#FF5252"
            st.markdown(
                f"""
                <div style="
                  background:#112240; border:1px solid rgba(0,212,255,0.12);
                  border-radius:10px; padding:0.65rem 0.75rem; margin-bottom:0.5rem;">
                  <div style="font-weight:600;font-size:0.85rem;color:#E6F1FF;
                    white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                    {_escape(entry['element'])}
                  </div>
                  <div style="font-size:0.75rem;color:rgba(230,241,255,0.5);margin-top:0.1rem;">
                    {entry['timestamp']}
                  </div>
                  <div style="margin-top:0.35rem;display:flex;gap:0.4rem;flex-wrap:wrap;">
                    <span style="background:rgba(0,230,118,0.1);color:#00E676;
                      border-radius:4px;padding:0.1rem 0.4rem;font-size:0.72rem;font-weight:700;">
                      ✓ {entry['passed']}
                    </span>
                    <span style="background:{'rgba(255,82,82,0.1)' if entry['failed'] else 'rgba(255,255,255,0.05)'};
                      color:{pass_color};
                      border-radius:4px;padding:0.1rem 0.4rem;font-size:0.72rem;font-weight:700;">
                      ✗ {entry['failed']}
                    </span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<hr/>", unsafe_allow_html=True)

    if (
        st.session_state.checkpoint_results is not None
        or st.session_state.refinement_results is not None
    ):
        export_data = _build_export_payload()
        element_name = st.session_state.selected_element or "export"
        filename = f"dq_evaluation_{element_name.replace(' ', '_').lower()}.json"
        st.download_button(
            label="⬇ Export Evaluation (JSON)",
            data=export_data,
            file_name=filename,
            mime="application/json",
        )


# ── Main Header ───────────────────────────────────────────────────────────────

st.markdown(
    """
    <div style="display:flex;align-items:center;gap:0.85rem;margin-bottom:0.25rem;">
      <span style="font-size:2rem;">🔍</span>
      <div>
        <h1 style="margin:0;font-size:1.65rem;font-weight:800;color:#E6F1FF;
          letter-spacing:-0.01em;line-height:1.2;">
          DQ Rule Refinement Studio
        </h1>
        <div style="color:rgba(230,241,255,0.5);font-size:0.88rem;margin-top:0.1rem;">
          Evaluate & refine data quality rules using AI-assisted checkpoint analysis
        </div>
      </div>
    </div>
    <hr/>
    """,
    unsafe_allow_html=True,
)


# ── Section 1: Element Selection & Properties ─────────────────────────────────

st.markdown('<div class="dq-section-title">Data Element Selection</div>', unsafe_allow_html=True)

element_options = ["— Select a data element —"] + list(MOCK_DATA_ELEMENTS.keys())

selected_label = st.selectbox(
    "Select a Data Element",
    options=element_options,
    index=0,
    label_visibility="collapsed",
)

selected = selected_label if selected_label != element_options[0] else None

# Reset if user changes element
if selected != st.session_state.selected_element:
    st.session_state.selected_element = selected
    if selected:
        st.session_state.edited_business_text = MOCK_DATA_ELEMENTS[selected]["business_text"]
    _reset_results()
    st.session_state.text_last_modified = None

if not selected:
    st.markdown(
        '<div class="dq-hero dq-animate-in dq-instruction">'
        '← Select a data element above to begin the evaluation workflow.'
        '</div>',
        unsafe_allow_html=True,
    )
    st.stop()

element = MOCK_DATA_ELEMENTS[selected]

st.markdown('<div class="dq-section-title">Element Properties</div>', unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    render_readonly_properties(element)

with right_col:
    current_text = st.session_state.edited_business_text

    new_text = render_rule_text_area(
        default_text=current_text,
        key=f"rule_text_{selected}",
    )

    if new_text != current_text:
        st.session_state.edited_business_text = new_text
        st.session_state.text_last_modified = datetime.now().strftime("%H:%M:%S")

    if st.session_state.text_last_modified:
        st.markdown(
            f'<div style="color:rgba(0,212,255,0.6);font-size:0.78rem;margin-top:0.25rem;">'
            f'Last modified at {st.session_state.text_last_modified}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    run_eval = st.button(
        "▶ Run Checkpoint Evaluation",
        type="primary",
        key="run_eval_btn",
        use_container_width=True,
    )

st.markdown("<hr/>", unsafe_allow_html=True)


# ── Section 2: Checkpoint Evaluation ─────────────────────────────────────────

if run_eval:
    _reset_results()
    _run_evaluation(element, st.session_state.edited_business_text)
    # After evaluation completes, immediately trigger refinement inline
    if st.session_state.flow_stage == "checkpoint_done":
        render_checkpoint_results(st.session_state.checkpoint_results)
        st.markdown("<hr/>", unsafe_allow_html=True)
        _run_refinement(element, st.session_state.edited_business_text)

elif st.session_state.flow_stage in ("checkpoint_done", "refining", "complete"):
    if st.session_state.checkpoint_results:
        render_checkpoint_results(st.session_state.checkpoint_results)
        st.markdown("<hr/>", unsafe_allow_html=True)


# ── Section 3: Rule Refinement ────────────────────────────────────────────────

if st.session_state.flow_stage == "complete" and st.session_state.refinement_results:
    def on_reevaluate(improved_text: str) -> None:
        st.session_state.edited_business_text = improved_text
        st.session_state.text_last_modified = datetime.now().strftime("%H:%M:%S")
        _reset_results()
        st.rerun()

    render_refinement_results(
        results=st.session_state.refinement_results,
        original_text=element["business_text"],
        on_reevaluate=on_reevaluate,
    )
