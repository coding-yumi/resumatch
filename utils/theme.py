import streamlit as st

GLOBAL_CSS = """
<style>
    /* ================================================================
       ResuMatch — Quiet Precision Design System
       Inspired by Linear / Notion / Stripe
    ================================================================ */

    /* ---------- Root & Base ---------- */
    .stApp {
        background: #F5F0EB;
    }
    html, body, [class*="css"] {
        font-family: system-ui, -apple-system, "PingFang SC", "Helvetica Neue", sans-serif;
        color: #1A1A1A;
    }
    .block-container {
        padding-top: 3rem;
        padding-bottom: 5rem;
        max-width: 960px;
    }

    /* ---------- Typography ---------- */
    h1 {
        font-weight: 300 !important;
        font-size: 2rem !important;
        color: #1A1A1A !important;
        letter-spacing: -0.01em !important;
        padding: 0 !important;
        margin-bottom: 0.25rem !important;
    }
    h2 {
        font-weight: 400 !important;
        font-size: 1.35rem !important;
        color: #1A1A1A !important;
        letter-spacing: -0.005em !important;
    }
    h3 {
        font-weight: 400 !important;
        font-size: 1.1rem !important;
        color: #1A1A1A !important;
    }
    p, li {
        line-height: 1.7;
    }

    /* ---------- Hero (Homepage) ---------- */
    .hero-container {
        padding: 4rem 0 2rem 0;
    }
    .hero-logo {
        font-size: 0.82rem;
        font-weight: 500;
        color: #6B6B6B;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 2.5rem;
    }
    .hero-title {
        font-size: 52px;
        font-weight: 300;
        color: #1A1A1A !important;
        margin: 0 0 1rem 0;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 18px;
        color: #6B6B6B;
        font-weight: 400;
        margin: 0 0 3rem 0;
        line-height: 1.6;
    }
    .hero-stat {
        font-size: 2.2rem;
        font-weight: 300;
        color: #1A1A1A;
        line-height: 1;
    }
    .hero-stat-label {
        font-size: 0.78rem;
        color: #6B6B6B;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-top: 0.3rem;
    }

    /* ---------- Step List ---------- */
    .step-item {
        padding: 1.5rem 0;
        border-top: 1px solid #E0DDD9;
    }
    .step-num {
        font-size: 0.78rem;
        font-weight: 500;
        color: #6B6B6B;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }
    .step-label {
        font-size: 1.15rem;
        font-weight: 400;
        color: #1A1A1A;
        margin-bottom: 0.35rem;
    }
    .step-desc {
        font-size: 0.92rem;
        color: #6B6B6B;
        line-height: 1.6;
    }

    /* ---------- Cards ---------- */
    .resumatch-card {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 28px 28px;
        border: 1px solid #E0DDD9;
    }

    /* ---------- Form Card ---------- */
    .form-card {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 32px;
        border: 1px solid #E0DDD9;
        margin-bottom: 2rem;
    }
    div[data-testid="stForm"] {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 2rem;
        border: 1px solid #E0DDD9;
    }

    /* ---------- Input Fields: bottom-border style ---------- */
    div[data-baseweb="input"] input,
    div[data-baseweb="input"] input:focus {
        border: none !important;
        border-radius: 0 !important;
        border-bottom: 1px solid #E0DDD9 !important;
        box-shadow: none !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        font-size: 0.95rem !important;
        color: #1A1A1A !important;
        background: transparent !important;
    }
    div[data-baseweb="input"] input:focus {
        border-bottom: 1.5px solid #1A1A1A !important;
    }
    div[data-baseweb="input"] {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
    }

    /* Textarea */
    textarea[data-testid="stTextAreaTextArea"] {
        background: #FFFFFF !important;
        border: 1px solid #E0DDD9 !important;
        border-radius: 8px !important;
        padding: 16px !important;
        font-size: 0.92rem !important;
        color: #1A1A1A !important;
        line-height: 1.7 !important;
        resize: vertical !important;
    }
    textarea[data-testid="stTextAreaTextArea"]:focus {
        border-color: #1A1A1A !important;
        box-shadow: none !important;
        outline: none !important;
    }
    textarea[data-testid="stTextAreaTextArea"]::placeholder {
        color: #B0B0B0 !important;
    }

    /* Select box */
    div[data-baseweb="select"] {
        border: none !important;
        border-bottom: 1px solid #E0DDD9 !important;
        border-radius: 0 !important;
    }
    div[data-baseweb="select"]:focus-within {
        border-bottom-color: #1A1A1A !important;
    }

    /* ---------- Buttons ---------- */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 500 !important;
        border: 1px solid #E0DDD9 !important;
        font-size: 0.9rem !important;
        padding: 0.45rem 1.4rem !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.01em !important;
    }
    .stButton > button[kind="primary"] {
        background: #1A1A1A !important;
        color: #FFFFFF !important;
        border-color: #1A1A1A !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: #333333 !important;
        border-color: #333333 !important;
    }
    .stButton > button[kind="secondary"] {
        background: #FFFFFF !important;
        color: #1A1A1A !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: #F5F0EB !important;
    }
    button[data-testid="stFormSubmitButton"] {
        background: #1A1A1A !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        padding: 0.45rem 1.6rem !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.01em !important;
    }
    button[data-testid="stFormSubmitButton"]:hover {
        background: #333333 !important;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: #EDEBE8;
        border-right: 1px solid #E0DDD9;
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {
        color: #1A1A1A !important;
        font-size: 0.88rem;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #1A1A1A !important;
    }
    /* Sidebar nav links — clean text, selected gets 2px dark bar */
    section[data-testid="stSidebar"] a {
        color: #1A1A1A !important;
        text-decoration: none !important;
        display: block;
        padding: 0.5rem 0.75rem;
        border-radius: 4px;
        border-left: 2px solid transparent;
        transition: all 0.15s ease;
        font-size: 0.88rem !important;
    }
    section[data-testid="stSidebar"] a:hover {
        background: rgba(0, 0, 0, 0.04);
    }
    section[data-testid="stSidebar"] a[aria-current="page"],
    section[data-testid="stSidebar"] a.st-emotion-cache-16ttjct {
        border-left: 2px solid #1A1A1A !important;
        font-weight: 500 !important;
    }

    /* ---------- Expanders ---------- */
    .streamlit-expanderHeader {
        background: #FFFFFF !important;
        border: 1px solid #E0DDD9 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        color: #1A1A1A !important;
    }
    details[data-testid="stExpander"] {
        background: transparent;
        border-radius: 8px;
        border: none;
        overflow: hidden;
    }

    /* ---------- Alerts ---------- */
    div[data-baseweb="notification"] {
        border-radius: 8px !important;
    }
    div[data-testid="stAlert"] {
        border-radius: 8px !important;
        border: 1px solid #E0DDD9 !important;
        background: #FFFFFF !important;
    }
    div[data-testid="stInfo"] {
        background: #FFFFFF !important;
        border-radius: 8px !important;
        border: 1px solid #E0DDD9 !important;
    }
    div[data-testid="stWarning"] {
        background: #FFFFFF !important;
        border-radius: 8px !important;
        border: 1px solid #E0DDD9 !important;
        border-left: 3px solid #C4A24A !important;
    }
    div[data-testid="stSuccess"] {
        background: #FFFFFF !important;
        border-radius: 8px !important;
        border: 1px solid #E0DDD9 !important;
    }
    div[data-testid="stError"] {
        background: #FFFFFF !important;
        border-radius: 8px !important;
        border: 1px solid #E0DDD9 !important;
    }

    /* ---------- Dividers ---------- */
    hr {
        border-color: #E0DDD9 !important;
        margin: 2.5rem 0 !important;
        border-width: 0.5px !important;
    }

    /* ---------- Score Display ---------- */
    .score-display {
        font-size: 64px;
        font-weight: 200;
        color: #1A1A1A;
        line-height: 1;
        margin: 0;
    }
    .score-unit {
        font-size: 18px;
        font-weight: 300;
        color: #6B6B6B;
        margin-left: 2px;
    }

    /* ---------- Comparison: Vertical Layout ---------- */
    .compare-original {
        background: #FAFAF8;
        border-radius: 8px;
        padding: 24px 28px;
        border: 1px solid #E0DDD9;
        margin-bottom: 0;
    }
    .compare-rewritten {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 24px 28px;
        border: 1px solid #E0DDD9;
        margin-top: 0;
    }
    .compare-label {
        font-size: 0.72rem;
        font-weight: 500;
        color: #6B6B6B;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 16px;
    }
    .compare-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    .compare-list li {
        color: #1A1A1A;
        font-size: 0.92rem;
        line-height: 1.7;
        padding: 4px 0 4px 14px;
        position: relative;
    }
    .compare-list li::before {
        content: "";
        position: absolute;
        left: 0;
        top: 11px;
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: #D1CFCC;
    }

    /* ---------- Tags ---------- */
    .tag {
        display: inline-block;
        background: #FFFFFF;
        color: #1A1A1A;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        margin: 3px 6px 3px 0;
        border: 1px solid #E0DDD9;
        letter-spacing: 0.02em;
    }

    /* ---------- Experience Card ---------- */
    .exp-card {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 24px 28px;
        border: 1px solid #E0DDD9;
        margin-bottom: 1rem;
    }
    .exp-card-header {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 0.75rem;
    }
    .exp-card-title {
        font-size: 1.05rem;
        font-weight: 500;
        color: #1A1A1A;
    }
    .exp-card-meta {
        font-size: 0.85rem;
        color: #6B6B6B;
    }
    .exp-card-bullet {
        font-size: 0.9rem;
        color: #4A4A4A;
        line-height: 1.65;
        padding: 2px 0;
    }

    /* ---------- Match Section Divider ---------- */
    .match-divider {
        border: none;
        border-top: 1px solid #E0DDD9;
        margin: 20px 0;
    }

    /* ---------- Progress / Spinner ---------- */
    div[data-testid="stSpinner"] {
        color: #1A1A1A !important;
    }

    /* ---------- Progress bar → hide ---------- */
    div[data-testid="stProgressBar"] {
        display: none;
    }

    /* ---------- Multi-select tags ---------- */
    div[data-baseweb="tag"] {
        border-radius: 6px !important;
        background: #FFFFFF !important;
        border: 1px solid #E0DDD9 !important;
    }

    /* ---------- Metric boxes ---------- */
    div[data-testid="stMetric"] {
        background: transparent !important;
        padding: 0 !important;
    }
    div[data-testid="stMetric"] label {
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        color: #6B6B6B !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 300 !important;
        color: #1A1A1A !important;
    }

    /* ---------- Tooltip ---------- */
    div[data-testid="stTooltipHoverTarget"] {
        border-bottom: 1px dotted #6B6B6B !important;
    }

    /* ---------- Hide Streamlit default elements ---------- */
    #MainMenu, footer, header[data-testid="stHeader"] {
        display: none;
    }
    .stDeployButton {
        display: none;
    }
    div[data-testid="stDecoration"] {
        display: none;
    }
</style>
"""


def inject_global_css() -> None:
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
