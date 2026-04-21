"""Checkpoint evaluation result renderer — compact card layout."""

from __future__ import annotations

import math
from typing import Any

import streamlit as st


def _escape(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_confidence_arc(pass_rate: float) -> None:
    """SVG radial arc confidence meter."""
    pct = int(pass_rate * 100)
    r = 44
    circ = 2 * math.pi * r
    dash, gap = circ * pass_rate, circ * (1 - pass_rate)
    color = "#00E676" if pct >= 80 else ("#FFD740" if pct >= 60 else "#FF5252")

    st.markdown(
        f"""
        <div style="display:flex;flex-direction:column;align-items:center;">
          <svg width="108" height="108" viewBox="0 0 108 108">
            <circle cx="54" cy="54" r="{r}" fill="none"
              stroke="rgba(255,255,255,0.07)" stroke-width="9"/>
            <circle cx="54" cy="54" r="{r}" fill="none"
              stroke="{color}" stroke-width="9"
              stroke-dasharray="{dash:.2f} {gap:.2f}"
              stroke-linecap="round"
              transform="rotate(-90 54 54)"/>
            <text x="54" y="51" text-anchor="middle"
              font-family="DM Sans,sans-serif" font-size="19" font-weight="700"
              fill="{color}">{pct}%</text>
            <text x="54" y="66" text-anchor="middle"
              font-family="DM Sans,sans-serif" font-size="9"
              fill="rgba(230,241,255,0.5)">CONFIDENCE</text>
          </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_summary_banner(summary: dict[str, int]) -> None:
    passed, failed = summary["passed"], summary["failed"]
    total = summary["total_checkpoints"]
    fail_bg = "rgba(255,82,82,0.12)" if failed else "rgba(255,255,255,0.04)"
    fail_col = "#FF5252" if failed else "rgba(230,241,255,0.35)"
    fail_bdr = "rgba(255,82,82,0.3)" if failed else "rgba(255,255,255,0.08)"

    st.markdown(
        f"""
        <div class="dq-card dq-animate-in" style="
            display:flex;align-items:center;gap:1rem;flex-wrap:wrap;
            padding:0.65rem 1rem;margin-bottom:0.5rem;">
          <div style="flex:1;min-width:120px;">
            <div class="dq-label">Summary</div>
            <div style="font-size:1.3rem;font-weight:700;color:#E6F1FF;margin-top:0.1rem;">
              {total} Checkpoints
            </div>
          </div>
          <div style="display:flex;gap:0.6rem;flex-wrap:wrap;align-items:center;">
            <span style="background:rgba(0,230,118,0.12);color:#00E676;
              border:1px solid rgba(0,230,118,0.3);border-radius:20px;
              padding:0.25rem 0.8rem;font-weight:700;font-size:0.92rem;">
              ✓ {passed} Passed
            </span>
            <span style="background:{fail_bg};color:{fail_col};
              border:1px solid {fail_bdr};border-radius:20px;
              padding:0.25rem 0.8rem;font-weight:700;font-size:0.92rem;">
              {'✗' if failed else '–'} {failed} Failed
            </span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_checkpoint_card(cp: dict[str, str]) -> None:
    is_pass = cp["outcome"].lower() == "pass"
    pill_bg  = "rgba(0,230,118,0.13)"  if is_pass else "rgba(255,82,82,0.13)"
    pill_col = "#00E676" if is_pass else "#FF5252"
    pill_bdr = "rgba(0,230,118,0.35)" if is_pass else "rgba(255,82,82,0.35)"
    label    = "PASS" if is_pass else "FAIL"

    # Render compact row; evidence in expander below
    st.markdown(
        f"""
        <div class="dq-cp-card dq-animate-in">
          <span style="
            flex-shrink:0;
            background:{pill_bg};color:{pill_col};
            border:1px solid {pill_bdr};border-radius:5px;
            padding:0.12rem 0.5rem;font-size:0.68rem;font-weight:700;
            font-family:'Space Mono',monospace;letter-spacing:0.08em;">
            {label}
          </span>
          <div style="flex:1;min-width:0;">
            <div style="font-weight:600;font-size:0.88rem;color:#E6F1FF;
              white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
              {_escape(cp['checkpoint_key'])}
            </div>
            <div style="font-size:0.8rem;color:rgba(230,241,255,0.6);
              margin-top:0.1rem;line-height:1.4;
              display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;
              overflow:hidden;">
              {_escape(cp['notes'])}
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander(f"Evidence — {cp['checkpoint_key']}", expanded=False):
        st.code(cp["evidence"], language=None)


def render_dimension_analysis(dim_analysis: dict[str, Any]) -> None:
    dims = dim_analysis.get("detected_dimensions", [])
    should_split = dim_analysis.get("should_split", False)
    split_reason = dim_analysis.get("split_reason", "")

    chips = " ".join(
        f'<span style="background:rgba(0,212,255,0.12);color:#00D4FF;'
        f'border:1px solid rgba(0,212,255,0.3);border-radius:20px;'
        f'padding:0.18rem 0.7rem;font-size:0.8rem;font-weight:600;">'
        f'{_escape(d)}</span>'
        for d in dims
    )
    split_badge = (
        '<span style="background:rgba(255,82,82,0.12);color:#FF5252;'
        'border:1px solid rgba(255,82,82,0.3);border-radius:6px;'
        'padding:0.12rem 0.55rem;font-size:0.72rem;font-weight:700;">SPLIT RECOMMENDED</span>'
        if should_split else
        '<span style="background:rgba(0,230,118,0.09);color:#00E676;'
        'border:1px solid rgba(0,230,118,0.22);border-radius:6px;'
        'padding:0.12rem 0.55rem;font-size:0.72rem;font-weight:700;">NO SPLIT REQUIRED</span>'
    )
    st.markdown(
        f"""
        <div class="dq-card dq-animate-in" style="padding:0.65rem 1rem;">
          <div class="dq-label" style="margin-bottom:0.45rem;">Dimension Analysis</div>
          <div style="display:flex;align-items:center;gap:0.6rem;flex-wrap:wrap;
            margin-bottom:0.45rem;">
            <span style="color:rgba(230,241,255,0.55);font-size:0.8rem;">Detected:</span>
            {chips}
            {split_badge}
          </div>
          <div style="color:rgba(230,241,255,0.6);font-size:0.82rem;line-height:1.5;">
            {_escape(split_reason)}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_checkpoint_results(results: dict[str, Any]) -> None:
    cp_eval    = results["checkpoint_evaluation"]
    summary    = cp_eval["summary"]
    checkpoints = cp_eval["checkpoint_results"]
    dim_analysis = cp_eval["dimension_analysis"]
    pass_rate  = summary["passed"] / max(summary["total_checkpoints"], 1)

    col_sum, col_meter = st.columns([3, 1])
    with col_sum:
        render_summary_banner(summary)
    with col_meter:
        render_confidence_arc(pass_rate)

    st.markdown("<hr/>", unsafe_allow_html=True)

    for cp in checkpoints:
        render_checkpoint_card(cp)

    st.markdown("<hr/>", unsafe_allow_html=True)
    render_dimension_analysis(dim_analysis)
