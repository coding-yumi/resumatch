import streamlit as st

GLOBAL_CSS = """
<style>
    /* ================================================================
       ResuMatch — Apple Design Language
    ================================================================ */

    /* ---------- Global Typography & Base ---------- */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text",
                     "PingFang SC", "Helvetica Neue", sans-serif;
        color: #1D1D1F;
    }

    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 4rem;
        max-width: 1100px;
    }

    /* ---------- Hero (Homepage Banner Replacement) ---------- */
    .hero-container {
        background: #FFFFFF;
        padding: 4rem 2rem 3.5rem 2rem;
        margin-bottom: 3rem;
        text-align: center;
    }
    .hero-title {
        font-size: 48px;
        font-weight: 600;
        color: #1D1D1F !important;
        margin: 0;
        letter-spacing: -0.02em;
        line-height: 1.15;
    }
    .hero-subtitle {
        font-size: 18px;
        color: #6E6E73;
        margin: 12px 0 0 0;
        font-weight: 400;
        letter-spacing: 0;
    }

    /* ---------- Step Cards ---------- */
    .resumatch-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 32px 28px;
        border: 1px solid #E5E5E5;
        height: 100%;
        transition: box-shadow 0.3s ease;
    }
    .resumatch-card:hover {
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    .resumatch-card .step-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #0071E3;
        margin-bottom: 16px;
    }
    .resumatch-card .step-num {
        color: #0071E3;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 8px;
    }
    .resumatch-card .step-title {
        color: #1D1D1F;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0 0 8px 0;
    }
    .resumatch-card .step-desc {
        color: #6E6E73;
        font-size: 0.92rem;
        margin: 0;
        line-height: 1.5;
    }

    /* ---------- Form Card ---------- */
    .form-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 32px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 2rem;
    }

    /* ---------- Page Titles ---------- */
    h1 {
        color: #1D1D1F !important;
        font-weight: 600 !important;
        font-size: 2rem !important;
    }
    h2, h3 {
        color: #1D1D1F !important;
        font-weight: 600 !important;
    }

    /* ---------- Input Fields: bottom-border style ---------- */
    div[data-baseweb="input"] input,
    div[data-baseweb="input"] input:focus {
        border: none !important;
        border-radius: 0 !important;
        border-bottom: 1px solid #E5E5E5 !important;
        box-shadow: none !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        font-size: 1rem !important;
        color: #1D1D1F !important;
        background: transparent !important;
    }
    div[data-baseweb="input"] input:focus {
        border-bottom: 1px solid #0071E3 !important;
    }
    div[data-baseweb="input"] {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
    }

    /* Textarea */
    textarea[data-testid="stTextAreaTextArea"] {
        background: #FFFFFF !important;
        border: 1px solid #E5E5E5 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-size: 0.95rem !important;
        color: #1D1D1F !important;
        resize: vertical !important;
    }
    textarea[data-testid="stTextAreaTextArea"]:focus {
        border-color: #0071E3 !important;
        box-shadow: 0 0 0 3px rgba(0, 113, 227, 0.12) !important;
        outline: none !important;
    }

    /* Select box */
    div[data-baseweb="select"] {
        border: none !important;
        border-bottom: 1px solid #E5E5E5 !important;
        border-radius: 0 !important;
    }
    div[data-baseweb="select"]:focus-within {
        border-bottom-color: #0071E3 !important;
    }

    /* ---------- Form Container ---------- */
    div[data-testid="stForm"] {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        border: none;
    }

    /* ---------- Buttons: Capsule Style ---------- */
    .stButton > button {
        border-radius: 24px !important;
        font-weight: 500 !important;
        border: none !important;
        font-size: 0.95rem !important;
        padding: 0.5rem 1.6rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"] {
        background: #0071E3 !important;
        color: #FFFFFF !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: #0066CC !important;
    }
    .stButton > button[kind="secondary"] {
        background: #F5F5F7 !important;
        color: #1D1D1F !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: #E5E5E5 !important;
    }

    /* Form submit button */
    button[data-testid="stFormSubmitButton"] {
        background: #0071E3 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 24px !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        padding: 0.5rem 1.6rem !important;
        transition: all 0.2s ease !important;
    }
    button[data-testid="stFormSubmitButton"]:hover {
        background: #0066CC !important;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: #F5F5F7;
        border-right: 1px solid #E5E5E5;
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {
        color: #1D1D1F !important;
        font-size: 0.92rem;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #1D1D1F !important;
    }
    /* Sidebar nav links */
    section[data-testid="stSidebar"] a {
        color: #1D1D1F !important;
        text-decoration: none !important;
        display: block;
        padding: 0.5rem 0.75rem;
        border-radius: 8px;
        border-left: 3px solid transparent;
        transition: all 0.15s ease;
    }
    section[data-testid="stSidebar"] a:hover {
        background: rgba(0, 113, 227, 0.06);
    }
    /* Selected nav item — blue accent bar */
    section[data-testid="stSidebar"] a[aria-current="page"],
    section[data-testid="stSidebar"] a.st-emotion-cache-16ttjct {
        border-left: 3px solid #0071E3 !important;
        font-weight: 500 !important;
    }

    /* ---------- Expanders ---------- */
    .streamlit-expanderHeader {
        background: #FFFFFF !important;
        border: 1px solid #E5E5E5 !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
        color: #1D1D1F !important;
    }
    details[data-testid="stExpander"] {
        background: transparent;
        border-radius: 12px;
        border: none;
        overflow: hidden;
    }

    /* ---------- Alerts ---------- */
    div[data-baseweb="notification"] {
        border-radius: 12px !important;
    }
    div[data-testid="stAlert"] {
        border-radius: 12px !important;
        border: none !important;
    }

    /* ---------- Dividers ---------- */
    hr {
        border-color: #E5E5E5 !important;
        margin: 2rem 0 !important;
    }

    /* ---------- Score Display ---------- */
    .score-display {
        font-size: 48px;
        font-weight: 700;
        color: #0071E3;
        line-height: 1;
        margin: 0.5rem 0;
    }
    .score-label {
        font-size: 14px;
        color: #6E6E73;
        margin-top: 4px;
    }

    /* ---------- Comparison Cards ---------- */
    .compare-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid #E5E5E5;
        min-height: 220px;
    }
    .compare-card.original {
        background: #FAFAFA;
    }
    .compare-card.rewritten {
        border-left: 3px solid #0071E3;
    }
    .compare-card .compare-label {
        font-size: 0.82rem;
        font-weight: 600;
        color: #6E6E73;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 16px;
    }
    .compare-card ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    .compare-card ul li {
        color: #1D1D1F;
        font-size: 0.93rem;
        line-height: 1.7;
        padding: 4px 0;
        padding-left: 16px;
        position: relative;
    }
    .compare-card ul li::before {
        content: "";
        position: absolute;
        left: 0;
        top: 12px;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #D1D1D6;
    }
    .compare-card.rewritten ul li::before {
        background: #0071E3;
    }

    /* ---------- Tags ---------- */
    .apple-tag {
        display: inline-block;
        background: #F5F5F7;
        color: #1D1D1F;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.85rem;
        margin: 3px 6px 3px 0;
    }

    /* ---------- Tech Stack Footer ---------- */
    .tech-stack {
        text-align: center;
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid #E5E5E5;
    }
    .tech-tag {
        display: inline-block;
        color: #6E6E73;
        font-size: 0.85rem;
        margin: 0.25rem 0.35rem;
    }
    .tech-separator {
        color: #D1D1D6;
        margin: 0 0.25rem;
    }

    /* ---------- Spinner ---------- */
    div[data-testid="stSpinner"] {
        color: #0071E3 !important;
    }

    /* ---------- Progress bar → hide (replaced by score number) ---------- */
    div[data-testid="stProgressBar"] {
        display: none;
    }

    /* ---------- Info boxes ---------- */
    div[data-testid="stInfo"] {
        background: #F5F5F7 !important;
        border-radius: 12px !important;
    }

    /* ---------- Warning boxes ---------- */
    div[data-testid="stWarning"] {
        background: #FFF9F0 !important;
        border-radius: 12px !important;
    }

    /* ---------- Success boxes ---------- */
    div[data-testid="stSuccess"] {
        background: #F0FFF4 !important;
        border-radius: 12px !important;
    }
</style>
"""


def inject_global_css() -> None:
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
