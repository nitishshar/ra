"""Rule refinement result renderer."""

from __future__ import annotations

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


def render_improved_text_card(improved_text: str) -> None:
    st.markdown(
        f"""
        <div class="dq-animate-in" style="
            background:linear-gradient(135deg,rgba(0,212,255,0.08),rgba(0,230,118,0.06));
            border:1px solid rgba(0,212,255,0.3);
            border-radius:14px; padding:1.25rem 1.35rem; margin-bottom:1rem;
            position:relative;">
          <span style="
            position:absolute; top:-0.55rem; left:1rem;
            background:linear-gradient(90deg,#00D4FF,#00E676);
            color:#0B1929; font-size:0.68rem; font-weight:800;
            letter-spacing:0.12em; border-radius:4px; padding:0.15rem 0.55rem;">
            NEW
          </span>
          <div class="dq-label" style="margin-bottom:0.5rem;">Improved Business Rule Text</div>
          <div style="
            font-family:'Space Mono',ui-monospace,monospace;
            font-size:0.875rem; color:#E6F1FF; line-height:1.6;">
            {_escape(improved_text)}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_suggested_rule_card(suggested: dict[str, str]) -> None:
    """Render the AI-generated suggested rule when no business_text was provided."""
    biz_text = suggested.get("business_text", "")
    dimension = suggested.get("dimension", "")
    rationale = suggested.get("rationale", "")
    note = suggested.get("note", "")

    st.markdown(
        f"""
        <div class="dq-animate-in" style="
            background:linear-gradient(135deg,rgba(255,215,64,0.06),rgba(0,212,255,0.06));
            border:1px solid rgba(255,215,64,0.35);
            border-radius:14px; padding:1.25rem 1.35rem; margin-bottom:1rem;
            position:relative;">
          <span style="
            position:absolute; top:-0.55rem; left:1rem;
            background:linear-gradient(90deg,#FFD740,#FFA726);
            color:#0B1929; font-size:0.68rem; font-weight:800;
            letter-spacing:0.12em; border-radius:4px; padding:0.15rem 0.55rem;">
            AI SUGGESTED
          </span>
          <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.75rem;flex-wrap:wrap;">
            <div class="dq-label" style="margin:0;">Generated Business Rule</div>
            <span style="
              background:rgba(0,212,255,0.1);color:#00D4FF;
              border:1px solid rgba(0,212,255,0.3);border-radius:20px;
              padding:0.15rem 0.65rem;font-size:0.75rem;font-weight:700;">
              {_escape(dimension)}
            </span>
          </div>
          <div style="
            font-family:'Space Mono',ui-monospace,monospace;
            font-size:0.875rem; color:#E6F1FF; line-height:1.6;
            margin-bottom:{'0.85rem' if rationale or note else '0'};">
            {_escape(biz_text)}
          </div>
          {'<div style="border-top:1px solid rgba(255,215,64,0.15);padding-top:0.75rem;margin-top:0.1rem;">' if rationale else ''}
          {'<div class="dq-label" style="margin-bottom:0.3rem;color:rgba(255,215,64,0.7);">Rationale</div>' if rationale else ''}
          {'<div style="color:rgba(230,241,255,0.7);font-size:0.87rem;line-height:1.55;">' + _escape(rationale) + '</div>' if rationale else ''}
          {'</div>' if rationale else ''}
          {'<div style="margin-top:0.85rem;display:flex;gap:0.5rem;align-items:flex-start;">'
           '<span style="color:#FFD740;font-size:0.95rem;flex-shrink:0;">⚠</span>'
           '<div style="color:rgba(255,215,64,0.85);font-size:0.82rem;line-height:1.5;">' + _escape(note) + '</div>'
           '</div>' if note else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_key_changes(changes: list[str]) -> None:
    items_html = "".join(
        f"""
        <div style="display:flex;gap:0.65rem;align-items:flex-start;margin-bottom:0.6rem;">
          <span style="color:#00E676;font-size:1.1rem;line-height:1.35;flex-shrink:0;">✓</span>
          <span style="color:#E6F1FF;font-size:0.92rem;line-height:1.5;">{_escape(c)}</span>
        </div>
        """
        for c in changes
    )
    st.markdown(
        f"""
        <div class="dq-card dq-animate-in">
          <div class="dq-label" style="margin-bottom:0.75rem;">Key Changes</div>
          {items_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_side_by_side(original_text: str, improved_text: str) -> None:
    st.markdown('<div class="dq-section-title">Rule Comparison</div>', unsafe_allow_html=True)
    col_orig, col_new = st.columns(2, gap="medium")

    with col_orig:
        st.markdown(
            f"""
            <div style="
                background:rgba(255,255,255,0.03);
                border:1px solid rgba(255,255,255,0.1);
                border-radius:12px; padding:1rem 1.1rem; height:100%;">
              <div style="
                font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em;
                color:rgba(230,241,255,0.45); margin-bottom:0.5rem; font-weight:700;">
                Original Rule
              </div>
              <div style="
                font-family:'Space Mono',ui-monospace,monospace;
                font-size:0.82rem; color:rgba(230,241,255,0.65);
                line-height:1.6;">
                {_escape(original_text)}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_new:
        st.markdown(
            f"""
            <div style="
                background:rgba(0,212,255,0.05);
                border:1px solid rgba(0,212,255,0.25);
                border-radius:12px; padding:1rem 1.1rem; height:100%;">
              <div style="
                font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em;
                color:#00D4FF; margin-bottom:0.5rem; font-weight:700;">
                Refined Rule
              </div>
              <div style="
                font-family:'Space Mono',ui-monospace,monospace;
                font-size:0.82rem; color:#E6F1FF;
                line-height:1.6;">
                {_escape(improved_text)}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_copy_button(improved_text: str) -> None:
    """Injects a JS-backed copy-to-clipboard button."""
    escaped_js = improved_text.replace("\\", "\\\\").replace("`", "\\`").replace("'", "\\'")
    copy_js = f"""
    <button onclick="
      navigator.clipboard.writeText('{escaped_js}').then(function(){{
        this.innerText='✓ Copied!';
        this.style.color='#00E676';
        setTimeout(()=>{{ this.innerText='📋 Copy Refined Rule'; this.style.color=''; }}, 2000);
      }}.bind(this)).catch(function(){{ alert('Copy failed — please copy manually.'); }});
    " style="
      background:#112240; color:#00D4FF;
      border:1px solid rgba(0,212,255,0.3);
      border-radius:10px; padding:0.5rem 1rem;
      font-family:'DM Sans',sans-serif; font-size:0.88rem;
      font-weight:600; cursor:pointer; transition:all 0.2s;
      margin-right:0.5rem;
    ">📋 Copy Refined Rule</button>
    """
    st.markdown(copy_js, unsafe_allow_html=True)


def render_refinement_results(
    results: dict[str, Any],
    original_text: str,
    *,
    on_reevaluate: Any = None,
) -> None:
    """Main entry — renders the full refinement section.

    Branches on whether the LLM produced an improved_business_text (existing rule
    was refined) or a suggested_rule (rule was absent / TBD and was generated
    from scratch).
    """
    ref = results["rule_refinement"]
    improved_text: str | None = ref.get("improved_business_text")
    suggested: dict[str, str] | None = ref.get("suggested_rule")
    key_changes: list[str] = ref.get("key_changes", [])
    rationale: str = ref.get("rationale", "")

    st.markdown('<div class="dq-section-title">Rule Refinement Results</div>', unsafe_allow_html=True)

    # ── Suggested rule (generated from scratch) ───────────────────────────────
    if suggested and not improved_text:
        render_suggested_rule_card(suggested)
        rule_for_actions = suggested["business_text"]

    # ── Improved rule (existing rule was refined) ─────────────────────────────
    else:
        render_improved_text_card(improved_text or "")
        rule_for_actions = improved_text or ""
        render_side_by_side(original_text, rule_for_actions)

    if key_changes:
        render_key_changes(key_changes)

    if rationale and not suggested:
        with st.expander("Rationale", expanded=False):
            st.markdown(
                f'<div style="color:rgba(230,241,255,0.8);font-size:0.92rem;line-height:1.6;">'
                f'{_escape(rationale)}</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br/>", unsafe_allow_html=True)

    action_col, copy_col = st.columns([1, 1], gap="small")
    with action_col:
        render_copy_button(rule_for_actions)
    with copy_col:
        btn_label = "🔄 Evaluate Suggested Rule" if suggested else "🔄 Re-evaluate with Refined Rule"
        if st.button(btn_label, key="reevaluate_btn", type="secondary"):
            if on_reevaluate:
                on_reevaluate(rule_for_actions)
