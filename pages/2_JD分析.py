import json
import re

import streamlit as st

from utils.ai_client import call_ai
from utils.prompts import JD_ANALYSIS_SYSTEM, JD_ANALYSIS_USER
from utils.theme import inject_global_css

inject_global_css()

if "jd_analysis" not in st.session_state:
    st.session_state.jd_analysis = None


def _strip_json_fence(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _parse_ai_json(text: str) -> tuple[dict | None, str]:
    cleaned = _strip_json_fence(text)
    try:
        return json.loads(cleaned), cleaned
    except json.JSONDecodeError:
        return None, cleaned


def _render_tags(label: str, items: list) -> None:
    st.markdown(f"**{label}**")
    if items:
        tags_html = " ".join(
            f'<span class="apple-tag">{item}</span>' for item in items
        )
        st.markdown(tags_html, unsafe_allow_html=True)
    else:
        st.caption("暂无")


def _render_analysis(result: dict) -> None:
    st.markdown("---")
    st.subheader("分析结果")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### {result.get('job_title', '未知岗位')}")
        company = result.get("company") or "未提及"
        st.markdown(
            f'<span style="color:#6E6E73;font-size:0.95rem;">{company}</span>',
            unsafe_allow_html=True,
        )
    with col2:
        direction = result.get("direction") or "未分类"
        st.markdown(
            f'<span class="apple-tag" style="font-weight:600;font-size:0.9rem;'
            f'margin-top:1.5em;">{direction}</span>',
            unsafe_allow_html=True,
        )

    summary = result.get("summary")
    if summary:
        st.info(summary)

    _render_tags("硬技能", result.get("hard_skills", []))
    _render_tags("软技能", result.get("soft_skills", []))
    _render_tags("加分项", result.get("bonus_points", []))

    with st.expander("原始 JSON（调试）", expanded=False):
        st.json(result)


st.title("JD 分析")
st.markdown(
    '<p style="color:#6E6E73;font-size:1rem;margin-bottom:1.5rem;">'
    '粘贴完整职位描述，AI 将提取岗位关键要求，供后续经历匹配使用。</p>',
    unsafe_allow_html=True,
)

jd_text = st.text_area(
    "职位描述",
    placeholder="请粘贴招聘岗位描述...",
    height=280,
    label_visibility="collapsed",
)

col_btn, _ = st.columns([1, 4])
with col_btn:
    analyze_clicked = st.button("分析 JD", type="primary")

if analyze_clicked:
    if not jd_text.strip():
        st.warning("请先粘贴职位描述后再分析。")
    else:
        with st.spinner("AI 分析中..."):
            prompt = JD_ANALYSIS_USER.format(jd_text=jd_text.strip())
            response = call_ai(prompt, system=JD_ANALYSIS_SYSTEM)

        if not response:
            st.error("AI 未返回有效结果，请检查 API Key 或稍后重试。")
        else:
            parsed, raw_text = _parse_ai_json(response)
            if parsed is None:
                st.error("JSON 解析失败，以下为 AI 原始返回：")
                st.text(raw_text)
            else:
                st.session_state.jd_analysis = parsed
                _render_analysis(parsed)

elif st.session_state.jd_analysis:
    _render_analysis(st.session_state.jd_analysis)
