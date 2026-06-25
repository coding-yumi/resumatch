import streamlit as st

from utils.data_manager import load_experiences
from utils.theme import inject_global_css

st.set_page_config(
    page_title="ResuMatch",
    page_icon="🎯",
    layout="wide",
)

inject_global_css()

if not load_experiences():
    st.info("👋 欢迎使用！请先前往「经历库」页面添加你的实习和项目经历。")

st.markdown(
    """
    <div class="hero-container">
        <h1 class="hero-title">ResuMatch 🎯</h1>
        <p class="hero-subtitle">粘贴 JD，30 秒获得匹配该岗位的优化简历经历</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### 三步完成简历经历优化")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="resumatch-card">
            <div class="step-num">Step 1</div>
            <p class="step-title">📝 录入经历库</p>
            <p style="color:#64748b;font-size:0.9rem;margin:0.6rem 0 0 0;">
                添加实习与项目经历，沉淀你的求职素材
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="resumatch-card">
            <div class="step-num">Step 2</div>
            <p class="step-title">📋 粘贴岗位 JD</p>
            <p style="color:#64748b;font-size:0.9rem;margin:0.6rem 0 0 0;">
                AI 自动提取岗位技能要求与核心能力
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="resumatch-card">
            <div class="step-num">Step 3</div>
            <p class="step-title">✨ 获取匹配结果</p>
            <p style="color:#64748b;font-size:0.9rem;margin:0.6rem 0 0 0;">
                智能匹配 Top 经历，一键生成优化描述
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="tech-stack">
        <span class="tech-tag">Python</span>
        <span class="tech-separator">·</span>
        <span class="tech-tag">Streamlit</span>
        <span class="tech-separator">·</span>
        <span class="tech-tag">智谱 GLM API</span>
        <span class="tech-separator">·</span>
        <span class="tech-tag">Prompt Engineering</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.header("导航说明")
st.sidebar.markdown(
    """
**ResuMatch 工作流**

1. 📝 **经历库**  
   添加工作经历、项目、技能等素材

2. 📋 **JD 分析**  
   输入岗位描述，AI 解析核心要求

3. ✅ **匹配结果**  
   生成匹配报告与简历优化建议

---
请在 `.streamlit/secrets.toml` 中配置 `ZHIPU_API_KEY`。
"""
)
