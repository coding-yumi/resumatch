import json

import streamlit as st

from utils.ai_client import call_ai
from utils.data_manager import load_experiences
from utils.helpers import parse_json_array, parse_rewrite_lines, strip_json_fence
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


# ── Helpers ────────────────────────────────────────────────────────

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


def _render_match_card(result: dict) -> None:
    exp = result["experience"]
    score = result["score"]
    reason = result["reason"]
    rewritten = result.get("rewritten", [])
    original_bullets = exp.get("bullets", [])
    title = exp.get("title", "未命名")
    company = exp.get("company_or_project", "-")
    date_range = f"{exp.get('start_date', '')} — {exp.get('end_date', '')}"

    st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)

    # Header row
    st.markdown(
        f'<div style="display:flex;justify-content:space-between;align-items:baseline;'
        f'margin-bottom:0.5rem;">'
        f'<span style="font-size:1.1rem;font-weight:500;color:#1A1A1A;">{title}</span>'
        f'<span style="font-size:0.85rem;color:#6B6B6B;">{company}  ·  {date_range}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Score
    st.markdown(
        f'<div style="margin:1rem 0 0.75rem 0;">'
        f'<span class="score-display">{score}</span>'
        f'<span class="score-unit">/ 100</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Reason
    st.markdown(
        f'<p style="font-size:0.92rem;color:#6B6B6B;line-height:1.7;margin-bottom:1.5rem;">'
        f'{reason}</p>',
        unsafe_allow_html=True,
    )

    # Original bullets
    st.markdown(
        '<div class="compare-original">'
        '<div class="compare-label">Original</div>'
        '<ul class="compare-list">'
        + "".join(f"<li>{b}</li>" for b in original_bullets) +
        '</ul></div>',
        unsafe_allow_html=True,
    )

    # Divider between original and rewritten
    st.markdown('<div class="match-divider"></div>', unsafe_allow_html=True)

    # Rewritten bullets
    rewritten_list_html = "".join(f"<li>{b}</li>" for b in rewritten) if rewritten else "<li>改写中...</li>"
    st.markdown(
        '<div class="compare-rewritten">'
        '<div class="compare-label">AI Optimized</div>'
        f'<ul class="compare-list">{rewritten_list_html}</ul>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Copy-friendly text area
    copy_text = "\n".join(f"• {line}" for line in rewritten)
    st.text_area(
        "改写文本（全选复制）",
        value=copy_text,
        height=120,
        key=f"copy_{exp.get('id', '')}",
        label_visibility="collapsed",
    )
    st.markdown('<hr style="margin:2rem 0 1.5rem 0;">', unsafe_allow_html=True)


def _run_matching(jd_analysis: dict) -> None:
    experiences = load_experiences()
    if not experiences:
        st.warning("经历库为空，请先在「经历库」页面添加经历。")
        return

    # Step 1: Scoring
    with st.spinner("AI 正在评估经历匹配度..."):
        prompt = MATCH_SCORING_USER.format(
            jd_summary_json=json.dumps(jd_analysis, ensure_ascii=False, indent=2),
            experiences_list=_format_experiences_for_prompt(experiences),
        )
        score_response = call_ai(prompt, system=MATCH_SCORING_SYSTEM)

    if not score_response:
        st.error("匹配评分失败，请稍后重试。")
        return

    scores, raw_scores = parse_json_array(score_response)
    if scores is None:
        st.error("匹配结果 JSON 解析失败，以下为 AI 原始返回：")
        st.text(raw_scores)
        return

    exp_map = {exp["id"]: exp for exp in experiences}
    qualified = [
        item for item in scores
        if item.get("score", 0) >= 55 and item.get("id") in exp_map
    ]
    qualified.sort(key=lambda x: x.get("score", 0), reverse=True)
    top_matches = qualified[:3]

    if not top_matches:
        st.warning("没有找到高匹配度的经历，建议补充相关经历或调整 JD。")
        st.session_state.match_results = []
        return

    direction = jd_analysis.get("direction", "")
    hard_skills = "、".join(jd_analysis.get("hard_skills", []))
    soft_skills = "、".join(jd_analysis.get("soft_skills", []))

    # Step 2: Rewrite each top match
    results = []
    total = len(top_matches)
    progress_container = st.empty()

    for idx, match in enumerate(top_matches, start=1):
        exp = exp_map[match["id"]]
        progress_container.info(f"正在改写第 {idx} / {total} 条经历...")

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

        rewritten = parse_rewrite_lines(rewrite_response) if rewrite_response else []
        if not rewritten:
            rewritten = ["（改写失败，请重试）"]

        results.append({
            "experience": exp,
            "score": match.get("score", 0),
            "reason": match.get("reason", ""),
            "rewritten": rewritten,
        })

    progress_container.empty()
    st.session_state.match_results = results
    st.success(f"匹配完成，共推荐 {len(results)} 条经历。")


# ── Page ──────────────────────────────────────────────────────────
st.markdown('<h1 style="margin-top:0;">匹配结果</h1>', unsafe_allow_html=True)

if not st.session_state.jd_analysis:
    st.warning("请先在「JD分析」页面输入 JD 并完成分析。")
    st.stop()

jd = st.session_state.jd_analysis
st.markdown(
    f'<p style="color:#6B6B6B;font-size:0.92rem;">'
    f'当前 JD：{jd.get("job_title", "未知岗位")}'
    f'{" — " + jd.get("company", "") if jd.get("company") else ""}</p>',
    unsafe_allow_html=True,
)

if st.button("开始匹配与改写", type="primary"):
    _run_matching(jd)

if st.session_state.match_results:
    st.markdown('<div style="height:1rem;"></div>', unsafe_allow_html=True)

    # Score overview bar chart
    scores_data = {r["experience"].get("title", "?"): r["score"] for r in st.session_state.match_results}
    st.bar_chart(scores_data, use_container_width=True, height=140)

    for result in st.session_state.match_results:
        _render_match_card(result)

    # Aggregate copy all
    all_rewritten = "\n\n".join(
        f"【{r['experience'].get('title', '')}】得分：{r['score']}/100\n"
        + "\n".join(f"• {line}" for line in r.get("rewritten", []))
        for r in st.session_state.match_results
    )
    st.download_button(
        label="导出全部改写内容",
        data=all_rewritten,
        file_name="resumatch_output.txt",
        mime="text/plain",
    )
