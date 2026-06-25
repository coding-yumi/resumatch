import streamlit as st

PRIMARY_DARK = "#1E3A5F"
PRIMARY_LIGHT = "#4A90D9"

GLOBAL_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }}

    /* Hero */
    .hero-container {{
        background: linear-gradient(135deg, {PRIMARY_DARK} 0%, {PRIMARY_LIGHT} 100%);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 24px rgba(30, 58, 95, 0.18);
    }}
    .hero-title {{
        font-size: 2.6rem;
        font-weight: 700;
        margin: 0 0 0.6rem 0;
        color: white !important;
        letter-spacing: -0.02em;
    }}
    .hero-subtitle {{
        font-size: 1.15rem;
        opacity: 0.92;
        margin: 0;
        font-weight: 400;
    }}

    /* Cards */
    .resumatch-card {{
        background: #f4f6f9;
        border-radius: 12px;
        padding: 1.4rem 1.2rem;
        border: 1px solid #e8ecf1;
        height: 100%;
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }}
    .resumatch-card:hover {{
        box-shadow: 0 6px 20px rgba(30, 58, 95, 0.1);
        transform: translateY(-2px);
    }}
    .resumatch-card .step-num {{
        color: {PRIMARY_LIGHT};
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.4rem;
    }}
    .resumatch-card .step-title {{
        color: {PRIMARY_DARK};
        font-size: 1.05rem;
        font-weight: 600;
        margin: 0;
    }}

    /* Tech tags */
    .tech-stack {{
        text-align: center;
        margin-top: 2.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e8ecf1;
    }}
    .tech-tag {{
        display: inline-block;
        background: {PRIMARY_DARK};
        color: white;
        padding: 0.35rem 0.9rem;
        border-radius: 20px;
        font-size: 0.82rem;
        margin: 0.25rem 0.35rem;
        font-weight: 500;
    }}
    .tech-separator {{
        color: {PRIMARY_LIGHT};
        font-weight: 600;
        margin: 0 0.15rem;
    }}

    /* Page titles on subpages */
    h1 {{
        color: {PRIMARY_DARK} !important;
    }}
    h2, h3 {{
        color: {PRIMARY_DARK} !important;
    }}

    /* Primary button */
    .stButton > button[kind="primary"] {{
        background: {PRIMARY_LIGHT} !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }}
    .stButton > button[kind="primary"]:hover {{
        background: {PRIMARY_DARK} !important;
    }}

    /* Success & warning alerts */
    div[data-testid="stAlert"] div[data-baseweb="notification"] {{
        border-radius: 10px !important;
    }}
    .stSuccess, div[data-testid="stAlert"]:has(svg[data-testid="stIconSuccess"]) {{
        background-color: #d1fae5 !important;
        border-left: 4px solid #059669 !important;
        border-radius: 10px !important;
    }}
    .stWarning, div[data-testid="stAlert"]:has(svg[data-testid="stIconWarning"]) {{
        background-color: #ffedd5 !important;
        border-left: 4px solid #ea580c !important;
        border-radius: 10px !important;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
    }}
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2 {{
        color: {PRIMARY_DARK} !important;
    }}

    /* Expander as card */
    .streamlit-expanderHeader {{
        background: #f4f6f9 !important;
        border-radius: 10px !important;
    }}
    details[data-testid="stExpander"] {{
        background: #f4f6f9;
        border-radius: 12px;
        border: 1px solid #e8ecf1;
        overflow: hidden;
    }}
</style>
"""


def inject_global_css() -> None:
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
