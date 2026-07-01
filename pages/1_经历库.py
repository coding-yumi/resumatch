import time

import streamlit as st

from utils.data_manager import add_experience, delete_experience, load_experiences, save_experiences
from utils.theme import inject_global_css

inject_global_css()

TYPE_OPTIONS = {
    "实习经历": "internship",
    "项目经历": "project",
}
TYPE_LABELS = {v: k for k, v in TYPE_OPTIONS.items()}

if "pending_delete_id" not in st.session_state:
    st.session_state.pending_delete_id = None


# ── Data Migration: old format → new format ────────────────────────
def _migrate_experiences():
    experiences = load_experiences()
    changed = False
    for exp in experiences:
        if "story" not in exp:
            # Build story from old fields
            parts = []
            if exp.get("start_date") or exp.get("end_date"):
                parts.append(f"时间段：{exp.get('start_date', '?')} — {exp.get('end_date', '?')}")
            if exp.get("bullets"):
                parts.append("\n".join(exp.get("bullets", [])))
            exp["story"] = "\n".join(parts) if parts else ""
            changed = True
        # Remove old fields
        for key in ["start_date", "end_date", "tags", "bullets"]:
            if key in exp:
                del exp[key]
                changed = True
    if changed:
        save_experiences(experiences)


_migrate_experiences()

# ── Page Header ───────────────────────────────────────────────────
st.markdown(
    '<h1 style="margin-top:0;">Career Asset Library</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p style="color:#6B6B6B;font-size:0.95rem;margin-bottom:2rem;line-height:1.7;">'
    '用你自己的话讲述每段经历，AI 帮你在不同岗位讲出不同的故事。</p>',
    unsafe_allow_html=True,
)

# ── Add Experience Form ───────────────────────────────────────────
with st.form("add_experience_form", clear_on_submit=True):
    st.markdown(
        '<p style="font-size:0.85rem;font-weight:500;color:#6B6B6B;'
        'letter-spacing:0.08em;text-transform:uppercase;margin-bottom:1rem;">'
        'New Story</p>',
        unsafe_allow_html=True,
    )

    exp_type_label = st.selectbox("经历类型", list(TYPE_OPTIONS.keys()))
    title = st.text_input("职位 / 项目名称")
    company_or_project = st.text_input("公司 / 项目名称")

    story = st.text_area(
        "经历故事",
        placeholder="用自己的话描述这段经历就好，可以参考 STAR 结构：\n"
                    "- 当时的背景是什么？（Situation）\n"
                    "- 你负责做什么？（Task）\n"
                    "- 你具体怎么做的？（Action）\n"
                    "- 最终结果如何？有没有数据？（Result）\n\n"
                    "例如：我在字节跳动电商团队负责用户增长，"
                    "当时转化率只有3%，我通过分析用户行为漏斗，"
                    "设计了3组A/B测试方案，最终将转化率提升到5.4%，"
                    "三个月内新增用户2万人。",
        height=220,
    )

    if st.form_submit_button("保存故事", type="primary"):
        errors = []
        if not title.strip():
            errors.append("职位 / 项目名称不能为空")
        if not company_or_project.strip():
            errors.append("公司 / 项目名称不能为空")
        if not story.strip():
            errors.append("经历故事不能为空")
        elif len(story.strip()) < 30:
            errors.append("经历故事内容过短，建议至少写 30 个字")

        if errors:
            for msg in errors:
                st.error(msg)
        else:
            exp_dict = {
                "id": f"exp_{int(time.time() * 1000)}",
                "type": TYPE_OPTIONS[exp_type_label],
                "title": title.strip(),
                "company_or_project": company_or_project.strip(),
                "story": story.strip(),
            }
            add_experience(exp_dict)
            st.success(f"已保存：{exp_dict['title']}")
            st.rerun()

st.markdown('<div style="height:2rem;"></div>', unsafe_allow_html=True)

# ── Search & Filter ───────────────────────────────────────────────
experiences = load_experiences()

if experiences:
    col_s, col_f = st.columns([3, 1])
    with col_s:
        search = st.text_input(
            "搜索经历",
            placeholder="按职位、公司或故事内容搜索...",
            key="exp_search_bar",
        )
    with col_f:
        all_types = ["全部"] + list(TYPE_OPTIONS.keys())
        filter_type = st.selectbox("类型筛选", all_types, label_visibility="collapsed")

    filtered = experiences
    if search:
        filtered = [
            e for e in filtered
            if search.lower() in e.get("title", "").lower()
            or search.lower() in e.get("company_or_project", "").lower()
            or search.lower() in e.get("story", "").lower()
        ]
    if filter_type != "全部":
        filtered = [
            e for e in filtered
            if e.get("type") == TYPE_OPTIONS[filter_type]
        ]

    st.markdown(
        f'<p style="font-size:0.82rem;color:#6B6B6B;margin-top:0.5rem;">'
        f'{len(filtered)} 段故事</p>',
        unsafe_allow_html=True,
    )
else:
    filtered = []
    st.markdown(
        '<p style="color:#6B6B6B;font-size:0.9rem;">'
        '暂无经历故事，请在上方添加你的第一段经历。</p>',
        unsafe_allow_html=True,
    )

st.markdown('<div style="height:1rem;"></div>', unsafe_allow_html=True)

# ── Experience Cards ──────────────────────────────────────────────
for exp in reversed(filtered):
    exp_id = exp.get("id")
    type_label = TYPE_LABELS.get(exp.get("type", ""), exp.get("type", "未知"))
    company = exp.get("company_or_project", "-")
    story_text = exp.get("story", "")
    story_preview = story_text[:120] + ("..." if len(story_text) > 120 else "")

    st.markdown(
        f"""
        <div class="exp-card">
            <div class="exp-card-header">
                <div>
                    <span class="exp-card-title">{exp.get('title', '未命名')}</span>
                    <span class="exp-card-meta" style="margin-left:10px;">{type_label}</span>
                </div>
                <div class="exp-card-meta">{company}</div>
            </div>
            <div class="exp-card-bullet">{story_preview}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Expand to read full story
    with st.expander("阅读完整故事", expanded=False):
        st.markdown(
            f'<p style="font-size:0.92rem;color:#1A1A1A;line-height:1.8;'
            f'white-space:pre-wrap;">{story_text}</p>',
            unsafe_allow_html=True,
        )

    # Delete flow
    if st.session_state.pending_delete_id == exp_id:
        st.warning("确定要删除这段经历吗？此操作不可撤销。")
        col_confirm, col_cancel = st.columns(2)
        with col_confirm:
            if st.button("确认删除", key=f"confirm_{exp_id}", type="primary"):
                if delete_experience(exp_id):
                    st.session_state.pending_delete_id = None
                    st.rerun()
        with col_cancel:
            if st.button("取消", key=f"cancel_{exp_id}"):
                st.session_state.pending_delete_id = None
                st.rerun()
    else:
        if st.button("删除", key=f"del_{exp_id}"):
            st.session_state.pending_delete_id = exp_id
            st.rerun()
    st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)
