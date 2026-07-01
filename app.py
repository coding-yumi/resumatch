import streamlit as st

from utils.data_manager import load_experiences
from utils.theme import inject_global_css

st.set_page_config(
    page_title="ResuMatch",
    page_icon="◾",
    layout="wide",
)

inject_global_css()

experiences = load_experiences()
exp_count = len(experiences)

# ── Hero ──────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-logo">ResuMatch</div>
        <h1 class="hero-title">简历，匹配你真正的价值</h1>
        <p class="hero-subtitle">
            录入经历，解析 JD，AI 为你精准匹配并优化描述
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Stats ─────────────────────────────────────────────────────────
if exp_count > 0:
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(f'<div class="hero-stat">{exp_count}</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-stat-label">Experiences</div>', unsafe_allow_html=True)
    with col_s2:
        st.markdown('<div class="hero-stat">3</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-stat-label">Steps</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:2.5rem;"></div>', unsafe_allow_html=True)
else:
    st.markdown(
        '<p style="color:#6B6B6B;font-size:0.9rem;margin-bottom:2rem;">'
        '请先前往「经历库」页面添加你的实习和项目经历。</p>',
        unsafe_allow_html=True,
    )
    st.markdown('<div style="height:1rem;"></div>', unsafe_allow_html=True)

# ── Nav (fallback when sidebar is collapsed) ──────────────────────
with st.container():
    st.markdown(
        '<p style="font-size:0.8rem;font-weight:500;color:#6B6B6B;'
        'letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.75rem;">'
        'Navigation</p>',
        unsafe_allow_html=True,
    )
    nav_cols = st.columns(3)
    with nav_cols[0]:
        st.page_link("pages/1_经历库.py", label="经历库")
    with nav_cols[1]:
        st.page_link("pages/2_JD分析.py", label="JD 分析")
    with nav_cols[2]:
        st.page_link("pages/3_匹配结果.py", label="匹配结果")
    st.markdown('<div style="height:2rem;"></div>', unsafe_allow_html=True)

# ── Steps ─────────────────────────────────────────────────────────
steps = [
    ("01", "录入经历库", "添加实习与项目经历，沉淀你的求职素材"),
    ("02", "粘贴岗位 JD", "AI 自动提取岗位要求、技能标签与核心能力"),
    ("03", "获取匹配结果", "智能匹配 Top 经历，生成 JD 对口的优化描述"),
]

for num, label, desc in steps:
    st.markdown(
        f"""
        <div class="step-item">
            <div class="step-num">{num}</div>
            <div class="step-label">{label}</div>
            <div class="step-desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
