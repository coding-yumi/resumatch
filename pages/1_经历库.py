import re
import time

import streamlit as st

from utils.data_manager import add_experience, delete_experience, load_experiences
from utils.theme import inject_global_css

inject_global_css()

TYPE_OPTIONS = {
    "实习经历": "internship",
    "项目经历": "project",
}
TYPE_LABELS = {v: k for k, v in TYPE_OPTIONS.items()}
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}$")

if "pending_delete_id" not in st.session_state:
    st.session_state.pending_delete_id = None


def _validate_date(value: str, field_name: str) -> str | None:
    if not value.strip():
        return f"{field_name}不能为空"
    if field_name == "结束时间" and value.strip() == "至今":
        return None
    if not DATE_PATTERN.match(value.strip()):
        return f"{field_name}格式应为 YYYY-MM（如 2024-07）"
    return None


st.title("经历库")
st.markdown(
    '<p style="color:#6E6E73;font-size:1rem;margin-bottom:1.5rem;">'
    '录入并管理你的实习与项目经历，供后续 JD 匹配使用。</p>',
    unsafe_allow_html=True,
)

# ── Add Experience Form ──
st.markdown("### 添加经历")
with st.form("add_experience_form", clear_on_submit=True):
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
        placeholder="每行一条，至少 3 条\n例如：\n负责用户行为数据分析\n搭建 SQL 报表看板\n优化查询性能 30%",
        height=150,
    )

    submitted = st.form_submit_button("保存经历", type="primary")

if submitted:
    errors = []
    if not title.strip():
        errors.append("职位 / 项目名称不能为空")
    if not company_or_project.strip():
        errors.append("公司 / 项目名称不能为空")

    start_error = _validate_date(start_date, "开始时间")
    if start_error:
        errors.append(start_error)
    end_error = _validate_date(end_date, "结束时间")
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
        st.success(f"已保存：{exp_dict['title']}（{TYPE_LABELS[exp_dict['type']]}）")

st.divider()

# ── Existing Experiences ──
st.markdown("### 已有经历")

experiences = load_experiences()

if not experiences:
    st.info("暂无经历，请在上方表单添加。")
else:
    for exp in reversed(experiences):
        type_label = TYPE_LABELS.get(exp.get("type", ""), exp.get("type", "未知"))
        period = f"{exp.get('start_date', '')} — {exp.get('end_date', '')}"
        expander_title = f"{type_label}  ·  {exp.get('title', '未命名')}  ·  {period}"

        with st.expander(expander_title, expanded=False):
            st.markdown(f"**公司 / 项目：** {exp.get('company_or_project', '-')}")
            st.markdown(f"**时间段：** {period}")

            tags = exp.get("tags", [])
            if tags:
                st.markdown(f"**技能标签：** {', '.join(tags)}")

            st.markdown("**经历要点：**")
            for bullet in exp.get("bullets", []):
                st.markdown(f"- {bullet}")

            exp_id = exp.get("id")
            if st.session_state.pending_delete_id == exp_id:
                st.warning("确定要删除这条经历吗？此操作不可撤销。")
                col_confirm, col_cancel = st.columns(2)
                with col_confirm:
                    if st.button("确认删除", key=f"confirm_delete_{exp_id}", type="primary"):
                        if delete_experience(exp_id):
                            st.session_state.pending_delete_id = None
                            st.rerun()
                        else:
                            st.error("删除失败，请重试。")
                with col_cancel:
                    if st.button("取消", key=f"cancel_delete_{exp_id}", type="secondary"):
                        st.session_state.pending_delete_id = None
                        st.rerun()
            else:
                if st.button("删除", key=f"delete_{exp_id}", type="secondary"):
                    st.session_state.pending_delete_id = exp_id
                    st.rerun()
