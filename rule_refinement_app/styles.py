"""Custom theme CSS for DQ Rule Refinement Studio (injected via st.markdown)."""

APP_CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

html, body, [data-testid="stAppViewContainer"] {
  font-family: 'DM Sans', system-ui, sans-serif;
  background: #0B1929 !important;
  color: #E6F1FF;
}

[data-testid="stAppViewContainer"] .main {
  background: #0B1929;
}

[data-testid="stHeader"] {
  background: rgba(11, 25, 41, 0.92);
}

.block-container {
  padding-top: 1.25rem;
  padding-bottom: 2rem;
  max-width: 1200px;
}

h1, h2, h3 {
  font-family: 'DM Sans', system-ui, sans-serif !important;
  letter-spacing: 0.02em;
}

.dq-section-title {
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #00D4FF;
  border-left: 3px solid #00D4FF;
  padding-left: 0.75rem;
  margin: 1.75rem 0 1rem 0;
}

.dq-card {
  background: #112240;
  border: 1px solid rgba(0, 212, 255, 0.15);
  border-radius: 12px;
  padding: 1rem 1.1rem;
  margin-bottom: 0.75rem;
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
}

.dq-card:hover {
  box-shadow: 0 0 0 1px rgba(0, 212, 255, 0.25), 0 8px 28px rgba(0, 212, 255, 0.08);
  border-color: rgba(0, 212, 255, 0.35);
}

.dq-muted {
  color: rgba(230, 241, 255, 0.65);
  font-size: 0.9rem;
}

.dq-label {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: rgba(0, 212, 255, 0.85);
  margin-bottom: 0.2rem;
}

.dq-value {
  font-family: 'Space Mono', ui-monospace, monospace;
  font-size: 0.88rem;
  color: #E6F1FF;
  line-height: 1.45;
}

.dq-hero {
  background: linear-gradient(135deg, rgba(17, 34, 64, 0.95), rgba(11, 25, 41, 0.9));
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 14px;
  padding: 1.25rem 1.35rem;
  margin-bottom: 1rem;
}

.dq-instruction {
  color: rgba(230, 241, 255, 0.72);
  font-size: 0.95rem;
  padding: 0.5rem 0;
}

/* Selectbox */
div[data-testid="stSelectbox"] > div > div {
  background-color: #112240 !important;
  border: 1px solid rgba(0, 212, 255, 0.2) !important;
  border-radius: 10px !important;
  color: #E6F1FF !important;
}

div[data-testid="stSelectbox"] label {
  color: #00D4FF !important;
  font-weight: 600 !important;
}

/* Text area */
div[data-testid="stTextArea"] textarea {
  background-color: #0d1f33 !important;
  color: #E6F1FF !important;
  border: 1px solid rgba(0, 212, 255, 0.2) !important;
  border-radius: 10px !important;
  font-family: 'Space Mono', ui-monospace, monospace !important;
  font-size: 0.85rem !important;
}

div[data-testid="stTextArea"] label {
  color: #00D4FF !important;
  font-weight: 600 !important;
}

/* Primary button */
div[data-testid="stButton"] > button[kind="primary"] {
  background: linear-gradient(90deg, #0099cc, #00D4FF) !important;
  color: #0B1929 !important;
  font-weight: 700 !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 0.65rem 1rem !important;
  width: 100%;
}

div[data-testid="stButton"] > button[kind="primary"]:hover {
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.35);
}

div[data-testid="stButton"] > button[kind="secondary"] {
  background: #112240 !important;
  color: #E6F1FF !important;
  border: 1px solid rgba(0, 212, 255, 0.25) !important;
  border-radius: 10px !important;
}

/* Expander */
div[data-testid="stExpander"] {
  background: #112240;
  border: 1px solid rgba(0, 212, 255, 0.12);
  border-radius: 12px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: #0d1f33;
  border-right: 1px solid rgba(0, 212, 255, 0.12);
}

/* Property grid animation */
@keyframes dqFadeUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.dq-animate-in {
  animation: dqFadeUp 0.45s ease-out both;
}

/* Progress bar */
div[data-testid="stProgress"] > div > div > div > div {
  background: linear-gradient(90deg, #00D4FF, #00E676) !important;
}

/* Spinner text */
div[data-testid="stSpinner"] {
  color: #00D4FF !important;
}

/* Download button */
div[data-testid="stDownloadButton"] button {
  background: #112240 !important;
  color: #00D4FF !important;
  border: 1px solid rgba(0, 212, 255, 0.3) !important;
  border-radius: 10px !important;
}

/* Dividers */
hr {
  border: none;
  border-top: 1px solid rgba(0, 212, 255, 0.12);
  margin: 1.25rem 0;
}
"""
