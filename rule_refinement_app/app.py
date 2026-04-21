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

# ── Page config ───────────────────────────────────────────────────────────────

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
    "_pending_rule_override": None,
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
    bar: Any,
) -> None:
    for message, fraction in steps:
        with placeholder.container():
            st.markdown(
                f'<div style="color:#00D4FF;font-size:0.9rem;font-weight:500;">'
                f'{message}</div>',
                unsafe_allow_html=True,
            )
        bar.progress(fraction)
        time.sleep(0.75)


def _run_evaluation(element: dict[str, str], business_text: str) -> None:
    st.session_state.flow_stage = "evaluating"
    status_box = st.empty()
    bar = st.progress(0.0)

    with st.spinner("Evaluating against checkpoints..."):
        _animated_progress(status_box, [
            ("🔍 Sending rule to evaluation engine...", 0.10),
            ("⚙️ Running DQ Dimension Mapping check...", 0.35),
            ("📊 Analyzing dimension coverage...", 0.65),
            ("✅ Finalizing checkpoint results...", 0.90),
        ], bar)
        try:
            result = mock_checkpoint_evaluation(
                cde_name=element["cde_name"],
                cde_definition=element["cde_definition"],
                rule_title=element["rule_title"],
                rule_dimension=element["rule_dimension"],
                business_text=business_text,
            )
        except Exception as exc:
            bar.empty(); status_box.empty()
            _show_error("Checkpoint evaluation failed", str(exc))
            st.session_state.flow_stage = "selection"
            return

    bar.progress(1.0); time.sleep(0.25); bar.empty(); status_box.empty()
    st.session_state.checkpoint_results = result
    st.session_state.flow_stage = "checkpoint_done"

    summary = result["checkpoint_evaluation"]["summary"]
    st.session_state.session_history.append({
        "element": element["cde_name"],
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "passed": summary["passed"],
        "failed": summary["failed"],
        "total": summary["total_checkpoints"],
    })


def _run_refinement(element: dict[str, str], business_text: str) -> None:
    st.session_state.flow_stage = "refining"
    status_box = st.empty()
    bar = st.progress(0.0)

    with st.spinner("Refining rule..."):
        _animated_progress(status_box, [
            ("🧠 Generating rule refinements...", 0.30),
            ("✨ Applying improvements...", 0.75),
        ], bar)
        try:
            ref_result = mock_rule_refinement(
                original_rule={**element, "business_text": business_text},
                checkpoint_results=st.session_state.checkpoint_results,
            )
        except Exception as exc:
            bar.empty(); status_box.empty()
            _show_error("Rule refinement failed", str(exc))
            st.session_state.flow_stage = "checkpoint_done"
            return

    bar.progress(1.0); time.sleep(0.25); bar.empty(); status_box.empty()
    st.session_state.refinement_results = ref_result
    st.session_state.flow_stage = "complete"


def _rerun() -> None:
    """st.rerun() compat shim — falls back to experimental_rerun for older Streamlit."""
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()  # type: ignore[attr-defined]


def _show_error(title: str, detail: str) -> None:
    st.markdown(
        f"""
        <div style="background:rgba(255,82,82,0.1);border:1px solid rgba(255,82,82,0.35);
          border-radius:12px;padding:0.85rem 1.1rem;margin:0.5rem 0;">
          <div style="color:#FF5252;font-weight:700;margin-bottom:0.3rem;">⚠ {_escape(title)}</div>
          <div style="color:rgba(230,241,255,0.7);font-size:0.87rem;">{_escape(detail)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _build_export_payload() -> str:
    name = st.session_state.selected_element or ""
    el   = MOCK_DATA_ELEMENTS.get(name, {})
    return json.dumps({
        "element": name,
        "cde_name": el.get("cde_name", ""),
        "rule_dimension": el.get("rule_dimension", ""),
        "edited_business_text": st.session_state.edited_business_text,
        "checkpoint_results": st.session_state.checkpoint_results,
        "refinement_results": st.session_state.refinement_results,
        "exported_at": datetime.now().isoformat(),
    }, indent=2)


# ── Sidebar: Session History ──────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        '<div style="font-size:0.7rem;font-weight:700;letter-spacing:0.12em;'
        'text-transform:uppercase;color:#00D4FF;border-left:3px solid #00D4FF;'
        'padding-left:0.6rem;margin-bottom:0.6rem;">Session History</div>',
        unsafe_allow_html=True,
    )

    history = st.session_state.session_history
    if not history:
        st.markdown(
            '<div style="color:rgba(230,241,255,0.4);font-size:0.83rem;'
            'padding:0.2rem 0 0.5rem;">No evaluations yet.</div>',
            unsafe_allow_html=True,
        )
    else:
        if st.button("🗑 Clear History", key="clear_history_btn", type="secondary",
                     use_container_width=True):
            st.session_state.session_history = []
            _rerun()

        st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)

        for entry in reversed(history):
            fail_col = "#FF5252" if entry["failed"] else "rgba(230,241,255,0.3)"
            st.markdown(
                f"""
                <div style="background:#112240;border:1px solid rgba(0,212,255,0.12);
                  border-radius:9px;padding:0.55rem 0.7rem;margin-bottom:0.4rem;">
                  <div style="font-weight:600;font-size:0.83rem;color:#E6F1FF;
                    white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                    {_escape(entry['element'])}
                  </div>
                  <div style="font-size:0.72rem;color:rgba(230,241,255,0.45);
                    margin-top:0.05rem;">{entry['timestamp']}</div>
                  <div style="margin-top:0.3rem;display:flex;gap:0.35rem;">
                    <span style="background:rgba(0,230,118,0.1);color:#00E676;
                      border-radius:4px;padding:0.08rem 0.38rem;font-size:0.7rem;
                      font-weight:700;">✓ {entry['passed']}</span>
                    <span style="background:{'rgba(255,82,82,0.1)' if entry['failed'] else 'rgba(255,255,255,0.04)'};
                      color:{fail_col};border-radius:4px;padding:0.08rem 0.38rem;
                      font-size:0.7rem;font-weight:700;">✗ {entry['failed']}</span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<hr/>", unsafe_allow_html=True)

    if (st.session_state.checkpoint_results is not None
            or st.session_state.refinement_results is not None):
        name = st.session_state.selected_element or "export"
        st.download_button(
            label="⬇ Export Evaluation (JSON)",
            data=_build_export_payload(),
            file_name=f"dq_evaluation_{name.replace(' ','_').lower()}.json",
            mime="application/json",
        )


# ── Header bar (full-width compact) ──────────────────────────────────────────

st.markdown(
    """
    <div style="display:flex;align-items:center;gap:0.7rem;
      padding:0.3rem 0 0.65rem 0;
      border-bottom:1px solid rgba(0,212,255,0.12);margin-bottom:0.75rem;">
      <span style="font-size:1.6rem;line-height:1;flex-shrink:0;">🔍</span>
      <div>
        <div style="font-size:1.2rem;font-weight:800;color:#E6F1FF;
          letter-spacing:-0.01em;line-height:1.15;">DQ Rule Refinement Studio</div>
        <div style="font-size:0.76rem;color:rgba(230,241,255,0.45);margin-top:0.05rem;">
          AI-assisted checkpoint analysis &amp; rule refinement
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Element dropdown (full-width) ─────────────────────────────────────────────

element_options = ["— Select a data element —"] + list(MOCK_DATA_ELEMENTS.keys())
selected_label  = st.selectbox(
    "Select a Data Element",
    options=element_options,
    index=0,
    label_visibility="collapsed",
)

selected = selected_label if selected_label != element_options[0] else None

# Reset when element changes
if selected != st.session_state.selected_element:
    st.session_state.selected_element = selected
    if selected:
        st.session_state.edited_business_text = MOCK_DATA_ELEMENTS[selected]["business_text"]
    _reset_results()
    st.session_state.text_last_modified = None

if not selected:
    st.markdown(
        '<div class="dq-hero dq-animate-in dq-instruction" style="margin-top:0.5rem;">'
        'Select a data element above to begin the evaluation workflow.'
        '</div>',
        unsafe_allow_html=True,
    )
    st.stop()

element = MOCK_DATA_ELEMENTS[selected]

st.markdown("<hr style='margin:0.5rem 0 0.75rem;'/>", unsafe_allow_html=True)


# ── Input Panel ───────────────────────────────────────────────────────────────

prop_col, rule_col = st.columns([5, 7], gap="large")

with prop_col:
    st.markdown('<div class="dq-section-title" style="margin-top:0;">Element Properties</div>',
                unsafe_allow_html=True)
    render_readonly_properties(element)

with rule_col:
    # Apply pending re-evaluate override BEFORE the widget is instantiated
    widget_key = f"rule_text_{selected}"
    if st.session_state._pending_rule_override is not None:
        st.session_state[widget_key] = st.session_state._pending_rule_override
        st.session_state._pending_rule_override = None

    current_text = st.session_state.edited_business_text
    new_text = render_rule_text_area(default_text=current_text, key=widget_key)

    if new_text != current_text:
        st.session_state.edited_business_text = new_text
        st.session_state.text_last_modified = datetime.now().strftime("%H:%M:%S")

    mod_note = ""
    if st.session_state.text_last_modified:
        mod_note = (
            f'<div style="color:rgba(0,212,255,0.55);font-size:0.74rem;'
            f'margin-bottom:0.35rem;">Last modified at '
            f'{st.session_state.text_last_modified}</div>'
        )
    st.markdown(mod_note, unsafe_allow_html=True)

    run_eval = st.button(
        "▶ Run Checkpoint Evaluation",
        type="primary",
        key="run_eval_btn",
        use_container_width=True,
    )

st.markdown("<hr style='margin:0.75rem 0;'/>", unsafe_allow_html=True)


# ── Results Tabs ──────────────────────────────────────────────────────────────

stage = st.session_state.flow_stage

# Build dynamic tab labels
if stage in ("checkpoint_done", "complete") and st.session_state.checkpoint_results:
    s = st.session_state.checkpoint_results["checkpoint_evaluation"]["summary"]
    cp_label = f"📋 Checkpoint Results  ·  ✓{s['passed']} ✗{s['failed']}"
else:
    cp_label = "📋 Checkpoint Results"

ref_label = "✨ Rule Refinement" + ("  ·  Ready" if stage == "complete" else "")

tab_cp, tab_ref = st.tabs([cp_label, ref_label])

# ── Tab 1: Checkpoint Evaluation ─────────────────────────────────────────────

with tab_cp:
    if run_eval:
        _reset_results()
        _run_evaluation(element, st.session_state.edited_business_text)
        if st.session_state.flow_stage == "checkpoint_done":
            render_checkpoint_results(st.session_state.checkpoint_results)

    elif stage in ("checkpoint_done", "complete") and st.session_state.checkpoint_results:
        render_checkpoint_results(st.session_state.checkpoint_results)

    else:
        st.markdown(
            '<div class="dq-instruction dq-animate-in" style="padding:1.5rem 0.5rem;'
            'color:rgba(230,241,255,0.45);text-align:center;">'
            'Run checkpoint evaluation to see results here.'
            '</div>',
            unsafe_allow_html=True,
        )

# ── Tab 2: Rule Refinement ────────────────────────────────────────────────────

with tab_ref:
    if run_eval and st.session_state.flow_stage == "checkpoint_done":
        _run_refinement(element, st.session_state.edited_business_text)

    if st.session_state.flow_stage == "complete" and st.session_state.refinement_results:
        def on_reevaluate(improved_text: str) -> None:
            st.session_state._pending_rule_override = improved_text
            st.session_state.edited_business_text   = improved_text
            st.session_state.text_last_modified     = datetime.now().strftime("%H:%M:%S")
            _reset_results()
            _rerun()

        render_refinement_results(
            results=st.session_state.refinement_results,
            original_text=element["business_text"],
            on_reevaluate=on_reevaluate,
        )

    elif st.session_state.flow_stage not in ("complete",):
        st.markdown(
            '<div class="dq-instruction dq-animate-in" style="padding:1.5rem 0.5rem;'
            'color:rgba(230,241,255,0.45);text-align:center;">'
            'Refinement results appear here after checkpoint evaluation completes.'
            '</div>',
            unsafe_allow_html=True,
        )

# ── Auto-switch to Refinement tab when complete ───────────────────────────────
# Inject JS to click the second tab button after the page settles.

if st.session_state.flow_stage == "complete":
    st.markdown(
        """
        <script>
        (function() {
          function switchTab() {
            var tabs = window.parent.document.querySelectorAll(
              '[data-testid="stTabs"] [data-testid="stTab"]'
            );
            if (tabs && tabs.length > 1) {
              tabs[1].click();
            } else {
              setTimeout(switchTab, 120);
            }
          }
          setTimeout(switchTab, 150);
        })();
        </script>
        """,
        unsafe_allow_html=True,
    )
