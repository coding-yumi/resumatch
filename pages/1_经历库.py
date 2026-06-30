import time

import streamlit as st

from utils.data_manager import add_experience, delete_experience, load_experiences
from utils.helpers import validate_date
from utils.theme import inject_global_css

inject_global_css()

TYPE_OPTIONS = {
    "实习经历": "internship",
    "项目经历": "project",
}
TYPE_LABELS = {v: k for k, v in TYPE_OPTIONS.items()}

if "pending_delete_id" not in st.session_state:
    st.session_state.pending_delete_id = None
if "exp_search" not in st.session_state:
    st.session_state.exp_search = ""
if "exp_filter_type" not in st.session_state:
    st.session_state.exp_filter_type = "全部"


# ── Page Header ───────────────────────────────────────────────────
st.markdown(
    '<h1 style="margin-top:0;">经历库</h1>',
    unsafe_allow_html=True,
)

# ── Add Experience Form ───────────────────────────────────────────
with st.form("add_experience_form", clear_on_submit=True):
    st.markdown(
        '<p style="font-size:0.85rem;font-weight:500;color:#6B6B6B;'
        'letter-spacing:0.08em;text-transform:uppercase;margin-bottom:1rem;">'
        'New Experience</p>',
        unsafe_allow_html=True,
    )

    exp_type_label = st.selectbox("经历类型", list(TYPE_OPTIONS.keys()))
    title = st.text_input("职位 / 项目名称")
    company_or_project = st.text_input("公司 / 项目名称")

    col_start, col_end = st.columns(2)
    with col_start:
        start_date = st.text_input("开始时间", placeholder="2024-07")
    with col_end:
        end_date = st.text_input("结束时间", placeholder="2024-10 或 至今")

    tags_input = st.text_input("技能标签", placeholder="Python, 数据分析, SQL")
    bullets_input = st.text_area(
        "经历要点",
        placeholder="每行一条，至少 3 条\n负责用户行为数据分析\n搭建 SQL 报表看板\n优化查询性能 30%",
        height=140,
    )

    if st.form_submit_button("保存经历", type="primary"):
        errors = []
        if not title.strip():
            errors.append("职位 / 项目名称不能为空")
        if not company_or_project.strip():
            errors.append("公司 / 项目名称不能为空")

        start_error = validate_date(start_date, "开始时间")
        if start_error:
            errors.append(start_error)
        end_error = validate_date(end_date, "结束时间")
        if end_error:
            errors.append(end_error)

        bullets = [line.strip() for line in bullets_input.splitlines() if line.strip()]
        if len(bullets) < 3:
            errors.append("经历要点至少需要 3 条（每行一条）")

        if errors:
            for msg in errors:
                st.error(msg)
        else:
            tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
            exp_dict = {
                "id": f"exp_{int(time.time() * 1000)}",
                "type": TYPE_OPTIONS[exp_type_label],
                "title": title.strip(),
                "company_or_project": company_or_project.strip(),
                "start_date": start_date.strip(),
                "end_date": end_date.strip(),
                "tags": tags,
                "bullets": bullets,
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
            placeholder="按职位、公司或技能标签搜索...",
            key="exp_search_bar",
        )
    with col_f:
        all_types = ["全部"] + list(TYPE_OPTIONS.keys())
        filter_type = st.selectbox("类型筛选", all_types, label_visibility="collapsed")

    # Apply filters
    filtered = experiences
    if search:
        filtered = [
            e for e in filtered
            if search.lower() in e.get("title", "").lower()
            or search.lower() in e.get("company_or_project", "").lower()
            or any(search.lower() in t.lower() for t in e.get("tags", []))
        ]
    if filter_type != "全部":
        filtered = [
            e for e in filtered
            if e.get("type") == TYPE_OPTIONS[filter_type]
        ]

    st.markdown(
        f'<p style="font-size:0.82rem;color:#6B6B6B;margin-top:0.5rem;">'
        f'{len(filtered)} 条经历</p>',
        unsafe_allow_html=True,
    )
else:
    filtered = []
    st.markdown(
        '<p style="color:#6B6B6B;font-size:0.9rem;">暂无经历，请在上方添加。</p>',
        unsafe_allow_html=True,
    )

st.markdown('<div style="height:1rem;"></div>', unsafe_allow_html=True)

# ── Experience Cards ──────────────────────────────────────────────
for exp in reversed(filtered):
    exp_id = exp.get("id")
    type_label = TYPE_LABELS.get(exp.get("type", ""), exp.get("type", "未知"))
    period = f"{exp.get('start_date', '')} — {exp.get('end_date', '')}"
    company = exp.get("company_or_project", "-")
    bullets = exp.get("bullets", [])
    tags = exp.get("tags", [])

    # Build card HTML
    tags_html = "".join(f'<span class="tag">{t}</span>' for t in tags)
    bullets_html = "".join(
        f'<div class="exp-card-bullet">— {b}</div>' for b in bullets
    )

    st.markdown(
        f"""
        <div class="exp-card">
            <div class="exp-card-header">
                <div>
                    <span class="exp-card-title">{exp.get('title', '未命名')}</span>
                    <span class="exp-card-meta" style="margin-left:10px;">{type_label}</span>
                </div>
                <div class="exp-card-meta">{period}</div>
            </div>
            <div class="exp-card-meta" style="margin-bottom:0.5rem;">{company}</div>
            {bullets_html}
            <div style="margin-top:0.75rem;">{tags_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Delete flow
    if st.session_state.pending_delete_id == exp_id:
        st.warning("确定删除这条经历？此操作不可撤销。")
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
