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


def _render_tags(label: str, items: list, color: str) -> None:
    st.markdown(f"**{label}**")
    if items:
        tags_html = " ".join(
            f'<span style="background:{color};color:#1a1a1a;padding:4px 12px;'
            f'border-radius:16px;margin:3px 4px 3px 0;display:inline-block;'
            f'font-size:0.9em">{item}</span>'
            for item in items
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
        st.markdown(f"**公司：** {company}")
    with col2:
        direction = result.get("direction") or "未分类"
        st.markdown(
            f'<p style="font-size:1.1em;margin-top:1.5em">'
            f'<span style="background:#fff3cd;padding:6px 14px;border-radius:8px;'
            f'font-weight:600">方向：{direction}</span></p>',
            unsafe_allow_html=True,
        )

    summary = result.get("summary")
    if summary:
        st.info(f"💡 {summary}")

    _render_tags("硬技能", result.get("hard_skills", []), "#dbeafe")
    _render_tags("软技能", result.get("soft_skills", []), "#dcfce7")
    _render_tags("加分项", result.get("bonus_points", []), "#fce7f3")

    with st.expander("原始 JSON（调试）", expanded=False):
        st.json(result)


st.title("JD 分析")
st.markdown("粘贴完整职位描述，AI 将提取岗位关键要求，供后续经历匹配使用。")

jd_text = st.text_area(
    "职位描述",
    placeholder="请粘贴招聘岗位描述...",
    height=280,
    label_visibility="collapsed",
)

if st.button("🔍 分析JD", type="primary"):
    if not jd_text.strip():
        st.warning("请先粘贴职位描述后再分析。")
    else:
        with st.spinner("AI分析中..."):
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
                st.success("✅ JD分析完成！请前往「匹配结果」页面查看推荐经历")
                _render_analysis(parsed)

elif st.session_state.jd_analysis:
    st.success("✅ 已加载上次分析结果")
    _render_analysis(st.session_state.jd_analysis)
