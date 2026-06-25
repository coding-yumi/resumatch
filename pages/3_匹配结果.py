import json
import re

import streamlit as st

from utils.ai_client import call_ai
from utils.data_manager import load_experiences
from utils.prompts import (
    MATCH_SCORING_SYSTEM,
    MATCH_SCORING_USER,
    REWRITE_SYSTEM,
    REWRITE_USER,
)
from utils.theme import inject_global_css

inject_global_css()

if "jd_analysis" not in st.session_state:
    st.session_state.jd_analysis = None
if "match_results" not in st.session_state:
    st.session_state.match_results = None


def _strip_json_fence(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _parse_json_array(text: str) -> tuple[list | None, str]:
    cleaned = _strip_json_fence(text)
    try:
        data = json.loads(cleaned)
        if isinstance(data, list):
            return data, cleaned
        return None, cleaned
    except json.JSONDecodeError:
        return None, cleaned


def _format_experiences_for_prompt(experiences: list) -> str:
    slim = []
    for exp in experiences:
        slim.append({
            "id": exp.get("id"),
            "type": exp.get("type"),
            "title": exp.get("title"),
            "company_or_project": exp.get("company_or_project"),
            "start_date": exp.get("start_date"),
            "end_date": exp.get("end_date"),
            "tags": exp.get("tags", []),
            "bullets": exp.get("bullets", []),
        })
    return json.dumps(slim, ensure_ascii=False, indent=2)


def _parse_rewrite_lines(text: str) -> list[str]:
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    cleaned = []
    for line in lines:
        line = re.sub(r"^[\d]+[\.\)、]\s*", "", line)
        line = re.sub(r"^[-•*✨]\s*", "", line)
        if line:
            cleaned.append(line)
    return cleaned


def _render_match_card(result: dict) -> None:
    exp = result["experience"]
    score = result["score"]
    reason = result["reason"]
    rewritten = result["rewritten"]
    title = exp.get("title", "未命名")
    company = exp.get("company_or_project", "-")
    date_range = f"{exp.get('start_date', '')} — {exp.get('end_date', '')}"
    original_bullets = exp.get("bullets", [])

    st.markdown(f"### {title} · {company}")
    st.caption(f"📅 {date_range}")
    st.progress(score / 100, text=f"匹配度 {score} 分")
    st.markdown(f"**推荐理由：** {reason}")

    col_left, col_right = st.columns(2)

    original_html = "".join(f"<li>{b}</li>" for b in original_bullets)
    with col_left:
        st.markdown(
            f'<div style="background:#f5f5f5;padding:16px;border-radius:8px;min-height:200px">'
            f"<strong>📄 原文</strong>"
            f"<ul style='margin-top:8px;padding-left:20px'>{original_html}</ul>"
            f"</div>",
            unsafe_allow_html=True,
        )

    rewritten_display = "".join(f"<li>✨ {b}</li>" for b in rewritten)
    with col_right:
        st.markdown(
            f'<div style="background:#e0f7fa;padding:16px;border-radius:8px;min-height:200px">'
            f"<strong>✨ AI 改写</strong>"
            f"<ul style='margin-top:8px;padding-left:20px'>{rewritten_display}</ul>"
            f"</div>",
            unsafe_allow_html=True,
        )
        st.code("\n".join(rewritten), language=None)

    st.divider()


def _run_matching(jd_analysis: dict) -> None:
    experiences = load_experiences()
    if not experiences:
        st.warning("经历库为空，请先在「经历库」页面添加经历。")
        return

    with st.spinner("AI 正在评估经历匹配度..."):
        prompt = MATCH_SCORING_USER.format(
            jd_summary_json=json.dumps(jd_analysis, ensure_ascii=False, indent=2),
            experiences_list=_format_experiences_for_prompt(experiences),
        )
        score_response = call_ai(prompt, system=MATCH_SCORING_SYSTEM)

    if not score_response:
        st.error("匹配评分失败，请稍后重试。")
        return

    scores, raw_scores = _parse_json_array(score_response)
    if scores is None:
        st.error("匹配结果 JSON 解析失败，以下为 AI 原始返回：")
        st.text(raw_scores)
        return

    exp_map = {exp["id"]: exp for exp in experiences}
    qualified = [
        item for item in scores
        if item.get("score", 0) >= 60 and item.get("id") in exp_map
    ]
    qualified.sort(key=lambda x: x.get("score", 0), reverse=True)
    top_matches = qualified[:3]

    if not top_matches:
        st.warning("没有找到匹配度 ≥ 60 分的经历，建议补充相关经历或调整 JD。")
        st.session_state.match_results = []
        return

    direction = jd_analysis.get("direction", "")
    hard_skills = "、".join(jd_analysis.get("hard_skills", []))
    soft_skills = "、".join(jd_analysis.get("soft_skills", []))

    results = []
    total = len(top_matches)
    progress_msg = st.empty()

    for idx, match in enumerate(top_matches, start=1):
        exp = exp_map[match["id"]]
        progress_msg.info(f"正在改写第 {idx} / {total} 条经历...")

        date_range = f"{exp.get('start_date', '')} — {exp.get('end_date', '')}"
        rewrite_prompt = REWRITE_USER.format(
            direction=direction,
            hard_skills=hard_skills,
            soft_skills=soft_skills,
            company=exp.get("company_or_project", ""),
            title=exp.get("title", ""),
            date_range=date_range,
            bullets="\n".join(exp.get("bullets", [])),
        )
        rewrite_response = call_ai(rewrite_prompt, system=REWRITE_SYSTEM)

        if rewrite_response:
            rewritten = _parse_rewrite_lines(rewrite_response)
        else:
            rewritten = ["（改写失败，请重试）"]

        results.append({
            "experience": exp,
            "score": match.get("score", 0),
            "reason": match.get("reason", ""),
            "rewritten": rewritten,
        })

    progress_msg.empty()
    st.session_state.match_results = results
    st.success(f"✅ 匹配完成！共推荐 {len(results)} 条经历。")


st.title("匹配结果")
st.markdown("根据 JD 分析结果，为你推荐最匹配的经历并生成优化版描述。")

if not st.session_state.jd_analysis:
    st.warning("请先在「JD分析」页面输入 JD")
    st.stop()

jd = st.session_state.jd_analysis
st.subheader(f"🎯 {jd.get('job_title', '未知岗位')}")
if jd.get("summary"):
    st.info(jd["summary"])

if st.button("🚀 开始匹配与改写", type="primary"):
    _run_matching(jd)

if st.session_state.match_results:
    st.markdown("---")
    st.subheader("推荐经历与改写")
    for result in st.session_state.match_results:
        _render_match_card(result)
