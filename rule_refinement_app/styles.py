"""Custom theme CSS for DQ Rule Refinement Studio (injected via st.markdown)."""

APP_CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

html, body, [data-testid="stAppViewContainer"] {
  font-family: 'DM Sans', system-ui, sans-serif;
  background: #0B1929 !important;
  color: #E6F1FF;
}
[data-testid="stAppViewContainer"] .main { background: #0B1929; }
[data-testid="stHeader"] { background: rgba(11,25,41,0.95); backdrop-filter: blur(8px); }

/* tighter main content padding */
.block-container {
  padding-top: 3.75rem !important;
  padding-bottom: 1.5rem;
  max-width: 1280px;
}

h1, h2, h3 { font-family: 'DM Sans', system-ui, sans-serif !important; }

/* ── Section titles ──────────────────────────────────────── */
.dq-section-title {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #00D4FF;
  border-left: 3px solid #00D4FF;
  padding-left: 0.65rem;
  margin: 1rem 0 0.6rem 0;
}

/* ── Standard card ───────────────────────────────────────── */
.dq-card {
  background: #112240;
  border: 1px solid rgba(0,212,255,0.15);
  border-radius: 12px;
  padding: 0.75rem 1rem;
  margin-bottom: 0.55rem;
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
}
.dq-card:hover {
  box-shadow: 0 0 0 1px rgba(0,212,255,0.25), 0 6px 20px rgba(0,212,255,0.07);
  border-color: rgba(0,212,255,0.32);
}

/* ── Compact checkpoint card ─────────────────────────────── */
.dq-cp-card {
  background: #112240;
  border: 1px solid rgba(0,212,255,0.13);
  border-radius: 10px;
  padding: 0.55rem 0.85rem;
  margin-bottom: 0.4rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  transition: border-color 0.15s;
}
.dq-cp-card:hover { border-color: rgba(0,212,255,0.28); }

/* ── Property grid ───────────────────────────────────────── */
.dq-prop-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}
.dq-prop-cell {
  background: #112240;
  border: 1px solid rgba(0,212,255,0.13);
  border-radius: 10px;
  padding: 0.55rem 0.8rem;
}

/* ── Label / value / muted ───────────────────────────────── */
.dq-muted  { color: rgba(230,241,255,0.62); font-size: 0.875rem; }
.dq-label  { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.08em;
              color: rgba(0,212,255,0.82); margin-bottom: 0.15rem; }
.dq-value  { font-family: 'Space Mono', ui-monospace, monospace;
              font-size: 0.85rem; color: #E6F1FF; line-height: 1.4; }

/* ── Hero / instruction ──────────────────────────────────── */
.dq-hero {
  background: linear-gradient(135deg, rgba(17,34,64,0.95), rgba(11,25,41,0.9));
  border: 1px solid rgba(0,212,255,0.2);
  border-radius: 14px;
  padding: 1rem 1.25rem;
  margin-bottom: 0.75rem;
}
.dq-instruction { color: rgba(230,241,255,0.72); font-size: 0.93rem; }

/* ── Selectbox ───────────────────────────────────────────── */
div[data-testid="stSelectbox"] > div > div {
  background-color: #112240 !important;
  border: 1.5px solid rgba(0,212,255,0.45) !important;
  border-radius: 10px !important;
  color: #E6F1FF !important;
}
div[data-testid="stSelectbox"] > div > div:hover {
  border-color: rgba(0,212,255,0.75) !important;
}
div[data-testid="stSelectbox"] label { color: #00D4FF !important; font-weight: 600 !important; }

/* ── Text area ───────────────────────────────────────────── */
div[data-testid="stTextArea"] textarea {
  background-color: #0d1f33 !important;
  color: #E6F1FF !important;
  border: 1px solid rgba(0,212,255,0.2) !important;
  border-radius: 10px !important;
  font-family: 'Space Mono', ui-monospace, monospace !important;
  font-size: 0.84rem !important;
}
div[data-testid="stTextArea"] label { color: #00D4FF !important; font-weight: 600 !important; }

/* ── Buttons ─────────────────────────────────────────────── */
div[data-testid="stButton"] > button[kind="primary"] {
  background: linear-gradient(90deg,#0099cc,#00D4FF) !important;
  color: #0B1929 !important; font-weight: 700 !important;
  border: none !important; border-radius: 10px !important;
  padding: 0.6rem 1rem !important; width: 100%;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
  box-shadow: 0 0 20px rgba(0,212,255,0.35);
}
div[data-testid="stButton"] > button[kind="secondary"] {
  background: #112240 !important; color: #E6F1FF !important;
  border: 1px solid rgba(0,212,255,0.25) !important; border-radius: 10px !important;
}

/* ── Tabs ────────────────────────────────────────────────── */
div[data-testid="stTabs"] [data-testid="stTab"] {
  background: transparent !important;
  color: rgba(230,241,255,0.55) !important;
  border: none !important;
  border-bottom: 2px solid transparent !important;
  border-radius: 0 !important;
  font-size: 0.88rem !important;
  font-weight: 600 !important;
  padding: 0.4rem 0.9rem 0.5rem !important;
  transition: color 0.15s, border-color 0.15s;
}
div[data-testid="stTabs"] [data-testid="stTab"]:hover {
  color: #E6F1FF !important;
  border-bottom-color: rgba(0,212,255,0.4) !important;
}
div[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"] {
  color: #00D4FF !important;
  border-bottom: 2px solid #00D4FF !important;
  background: transparent !important;
}
div[data-testid="stTabContent"] {
  border: 1px solid rgba(0,212,255,0.12);
  border-top: none;
  border-radius: 0 0 12px 12px;
  padding: 0.85rem 0.75rem;
  background: rgba(17,34,64,0.35);
}

/* ── Expander ────────────────────────────────────────────── */
div[data-testid="stExpander"] {
  background: #112240;
  border: 1px solid rgba(0,212,255,0.12);
  border-radius: 10px;
}

/* ── Sidebar ─────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
  background: #0d1f33;
  border-right: 1px solid rgba(0,212,255,0.12);
}

/* ── Progress bar ────────────────────────────────────────── */
div[data-testid="stProgress"] > div > div > div > div {
  background: linear-gradient(90deg,#00D4FF,#00E676) !important;
}

/* ── Download button ─────────────────────────────────────── */
div[data-testid="stDownloadButton"] button {
  background: #112240 !important; color: #00D4FF !important;
  border: 1px solid rgba(0,212,255,0.3) !important; border-radius: 10px !important;
}

/* ── Dividers ────────────────────────────────────────────── */
hr { border: none; border-top: 1px solid rgba(0,212,255,0.1); margin: 0.85rem 0; }

/* ── Fade-up animation ───────────────────────────────────── */
@keyframes dqFadeUp {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.dq-animate-in { animation: dqFadeUp 0.4s ease-out both; }

/* ── Top bar ─────────────────────────────────────────────── */
.dq-topbar {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.4rem 0 0.6rem 0;
  border-bottom: 1px solid rgba(0,212,255,0.1);
  margin-bottom: 0.7rem;
}
.dq-topbar-brand {
  display: flex; align-items: center; gap: 0.55rem; flex-shrink: 0;
}
.dq-topbar-brand h1 {
  margin: 0; font-size: 1.15rem !important; font-weight: 800;
  color: #E6F1FF; letter-spacing: -0.01em; line-height: 1.1;
  white-space: nowrap;
}
.dq-topbar-brand .sub {
  font-size: 0.72rem; color: rgba(230,241,255,0.45); margin-top: 0.05rem;
  white-space: nowrap;
}
"""
