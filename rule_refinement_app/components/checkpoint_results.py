"""Checkpoint evaluation result card renderer."""

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
    """Render an SVG radial arc confidence meter (0–100%)."""
    pct = int(pass_rate * 100)
    r = 54
    circumference = 2 * math.pi * r
    dash = circumference * pass_rate
    gap = circumference - dash

    if pct >= 80:
        arc_color = "#00E676"
    elif pct >= 60:
        arc_color = "#FFD740"
    else:
        arc_color = "#FF5252"

    svg = f"""
    <div style="display:flex;flex-direction:column;align-items:center;gap:0.25rem;">
      <svg width="130" height="130" viewBox="0 0 130 130">
        <circle cx="65" cy="65" r="{r}" fill="none"
          stroke="rgba(255,255,255,0.07)" stroke-width="10"/>
        <circle cx="65" cy="65" r="{r}" fill="none"
          stroke="{arc_color}" stroke-width="10"
          stroke-dasharray="{dash:.2f} {gap:.2f}"
          stroke-linecap="round"
          transform="rotate(-90 65 65)"
          style="transition: stroke-dasharray 0.8s ease;"/>
        <text x="65" y="62" text-anchor="middle"
          font-family="DM Sans,sans-serif" font-size="22" font-weight="700"
          fill="{arc_color}">{pct}%</text>
        <text x="65" y="80" text-anchor="middle"
          font-family="DM Sans,sans-serif" font-size="10"
          fill="rgba(230,241,255,0.6)">CONFIDENCE</text>
      </svg>
    </div>
    """
    st.markdown(svg, unsafe_allow_html=True)


def render_summary_banner(summary: dict[str, int], pass_rate: float) -> None:
    total = summary["total_checkpoints"]
    passed = summary["passed"]
    failed = summary["failed"]

    st.markdown(
        f"""
        <div class="dq-card dq-animate-in" style="
            display:flex; align-items:center; gap:1.2rem;
            flex-wrap:wrap; margin-bottom:0.5rem;">
          <div style="flex:1; min-width:160px;">
            <div class="dq-label">Evaluation Summary</div>
            <div style="font-size:1.55rem; font-weight:700; color:#E6F1FF; margin-top:0.2rem;">
              {total} Checkpoints
            </div>
          </div>
          <div style="display:flex; gap:0.75rem; flex-wrap:wrap;">
            <span style="
              background:rgba(0,230,118,0.12); color:#00E676;
              border:1px solid rgba(0,230,118,0.3);
              border-radius:20px; padding:0.3rem 0.9rem;
              font-weight:700; font-size:1rem; letter-spacing:0.03em;">
              ✓ {passed} Passed
            </span>
            <span style="
              background:{'rgba(255,82,82,0.12)' if failed else 'rgba(0,230,118,0.06)'};
              color:{'#FF5252' if failed else 'rgba(230,241,255,0.45)'};
              border:1px solid {'rgba(255,82,82,0.3)' if failed else 'rgba(255,255,255,0.08)'};
              border-radius:20px; padding:0.3rem 0.9rem;
              font-weight:700; font-size:1rem; letter-spacing:0.03em;">
              {'✗' if failed else '–'} {failed} Failed
            </span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_checkpoint_card(cp: dict[str, str], index: int) -> None:
    outcome = cp["outcome"].lower()
    is_pass = outcome == "pass"
    pill_bg = "rgba(0,230,118,0.13)" if is_pass else "rgba(255,82,82,0.13)"
    pill_color = "#00E676" if is_pass else "#FF5252"
    pill_border = "rgba(0,230,118,0.35)" if is_pass else "rgba(255,82,82,0.35)"
    pill_label = "PASS" if is_pass else "FAIL"

    st.markdown(
        f"""
        <div class="dq-card dq-animate-in" style="display:flex;align-items:flex-start;gap:1rem;">
          <div style="flex-shrink:0;padding-top:0.15rem;">
            <span style="
              background:{pill_bg}; color:{pill_color};
              border:1px solid {pill_border};
              border-radius:6px; padding:0.2rem 0.65rem;
              font-size:0.72rem; font-weight:700; letter-spacing:0.1em;
              font-family:'Space Mono',monospace;">{pill_label}</span>
          </div>
          <div style="flex:1; min-width:0;">
            <div style="font-weight:600; font-size:0.95rem; color:#E6F1FF; margin-bottom:0.25rem;">
              {_escape(cp['checkpoint_key'])}
            </div>
            <div class="dq-muted">{_escape(cp['notes'])}</div>
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

    chips_html = " ".join(
        f'<span style="background:rgba(0,212,255,0.12);color:#00D4FF;'
        f'border:1px solid rgba(0,212,255,0.3);border-radius:20px;'
        f'padding:0.2rem 0.75rem;font-size:0.82rem;font-weight:600;">'
        f'{_escape(d)}</span>'
        for d in dims
    )

    split_badge = (
        '<span style="background:rgba(255,82,82,0.12);color:#FF5252;'
        'border:1px solid rgba(255,82,82,0.3);border-radius:6px;'
        'padding:0.15rem 0.6rem;font-size:0.75rem;font-weight:700;">SPLIT RECOMMENDED</span>'
        if should_split
        else
        '<span style="background:rgba(0,230,118,0.10);color:#00E676;'
        'border:1px solid rgba(0,230,118,0.25);border-radius:6px;'
        'padding:0.15rem 0.6rem;font-size:0.75rem;font-weight:700;">NO SPLIT REQUIRED</span>'
    )

    st.markdown(
        f"""
        <div class="dq-card dq-animate-in">
          <div class="dq-label" style="margin-bottom:0.6rem;">Dimension Analysis</div>
          <div style="display:flex;align-items:center;gap:0.75rem;flex-wrap:wrap;margin-bottom:0.6rem;">
            <span style="color:rgba(230,241,255,0.6);font-size:0.82rem;">Detected:</span>
            {chips_html}
            {split_badge}
          </div>
          <div class="dq-muted" style="font-size:0.84rem;">{_escape(split_reason)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_checkpoint_results(results: dict[str, Any]) -> None:
    """Main entry point — renders the full checkpoint section."""
    cp_eval = results["checkpoint_evaluation"]
    summary = cp_eval["summary"]
    checkpoints = cp_eval["checkpoint_results"]
    dim_analysis = cp_eval["dimension_analysis"]

    pass_rate = summary["passed"] / max(summary["total_checkpoints"], 1)

    st.markdown('<div class="dq-section-title">Checkpoint Evaluation Results</div>', unsafe_allow_html=True)

    col_summary, col_meter = st.columns([3, 1])
    with col_summary:
        render_summary_banner(summary, pass_rate)
    with col_meter:
        render_confidence_arc(pass_rate)

    st.markdown("<hr/>", unsafe_allow_html=True)

    for i, cp in enumerate(checkpoints):
        render_checkpoint_card(cp, i)

    st.markdown("<hr/>", unsafe_allow_html=True)
    render_dimension_analysis(dim_analysis)
