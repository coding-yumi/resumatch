import json

import streamlit as st

from utils.ai_client import call_ai
from utils.helpers import parse_ai_json
from utils.prompts import JD_ANALYSIS_SYSTEM, JD_ANALYSIS_USER
from utils.theme import inject_global_css

inject_global_css()

if "jd_analysis" not in st.session_state:
    st.session_state.jd_analysis = None
if "jd_analysis_raw" not in st.session_state:
    st.session_state.jd_analysis_raw = None


def _render_tags(label: str, items: list) -> None:
    if not items:
        return
    tags_html = " ".join(f'<span class="tag">{item}</span>' for item in items)
    st.markdown(
        f'<p style="font-size:0.82rem;font-weight:500;color:#6B6B6B;'
        f'margin-bottom:0.5rem;">{label}</p>'
        f'<div style="margin-bottom:1rem;">{tags_html}</div>',
        unsafe_allow_html=True,
    )


def _render_analysis(result: dict) -> None:
    job_title = result.get("job_title", "未知岗位")
    company = result.get("company") or "未提及公司"
    direction = result.get("direction") or "未分类"
    summary = result.get("summary", "")

    st.markdown(
        f'<h2 style="margin-top:2rem;">{job_title}</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<p style="color:#6B6B6B;font-size:0.95rem;margin-top:-0.5rem;">'
        f'{company}  ·  {direction}</p>',
        unsafe_allow_html=True,
    )

    if summary:
        st.markdown(
            f'<div style="background:#FFFFFF;border:1px solid #E0DDD9;'
            f'border-radius:8px;padding:20px 24px;margin:1.5rem 0;'
            f'font-size:0.92rem;color:#4A4A4A;line-height:1.7;">'
            f'{summary}</div>',
            unsafe_allow_html=True,
        )

    _render_tags("HARD SKILLS", result.get("hard_skills", []))
    _render_tags("SOFT SKILLS", result.get("soft_skills", []))
    _render_tags("BONUS", result.get("bonus_points", []))


# ── Page ──────────────────────────────────────────────────────────
st.markdown('<h1 style="margin-top:0;">JD 分析</h1>', unsafe_allow_html=True)

jd_text = st.text_area(
    "职位描述",
    placeholder="粘贴完整职位描述，AI 将提取关键信息...",
    height=300,
    label_visibility="collapsed",
)

if st.button("分析 JD", type="primary"):
    if not jd_text.strip():
        st.warning("请先粘贴职位描述后再分析。")
    else:
        with st.spinner("AI 分析中..."):
            prompt = JD_ANALYSIS_USER.format(jd_text=jd_text.strip())
            response = call_ai(prompt, system=JD_ANALYSIS_SYSTEM)

        if not response:
            st.error("AI 未返回有效结果，请检查 API Key 或稍后重试。")
        else:
            parsed, raw_text = parse_ai_json(response)
            if parsed is None:
                st.error("JSON 解析失败，以下为 AI 原始返回：")
                st.text(raw_text)
            else:
                st.session_state.jd_analysis = parsed
                st.session_state.jd_analysis_raw = raw_text
                # Store raw JD text for history
                if "jd_history" not in st.session_state:
                    st.session_state.jd_history = []
                # Avoid duplicates
                existing = [h for h in st.session_state.jd_history if h["jd"] == jd_text.strip()]
                if not existing:
                    st.session_state.jd_history.insert(0, {
                        "jd": jd_text.strip()[:200],
                        "job_title": parsed.get("job_title", ""),
                        "company": parsed.get("company", ""),
                        "result": parsed,
                        "timestamp": json.dumps({"date": ""}),  # placeholder
                    })
                    if len(st.session_state.jd_history) > 10:
                        st.session_state.jd_history = st.session_state.jd_history[:10]
                _render_analysis(parsed)
                st.rerun()

elif st.session_state.jd_analysis:
    _render_analysis(st.session_state.jd_analysis)

# ── JD History ────────────────────────────────────────────────────
if "jd_history" in st.session_state and len(st.session_state.jd_history) > 1:
    st.markdown('<div style="height:2rem;"></div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:0.8rem;font-weight:500;color:#6B6B6B;'
        'letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.5rem;">'
        'Recent JDs</p>',
        unsafe_allow_html=True,
    )
    for i, h in enumerate(st.session_state.jd_history[1:8]):
        label = f"{h.get('job_title', 'JD')} — {h.get('company', '')}"[:50]
        if st.button(label, key=f"jd_hist_{i}"):
            st.session_state.jd_analysis = h["result"]
            st.rerun()
