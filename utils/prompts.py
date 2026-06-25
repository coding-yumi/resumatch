PROMPTS: dict[str, str] = {}

JD_ANALYSIS_SYSTEM = "你是一位专业的HR和职位分析专家，擅长从招聘JD中提取关键信息。"

JD_ANALYSIS_USER = """请分析以下职位描述，提取关键信息，只输出JSON，不要有任何多余说明或markdown代码块：

{jd_text}

输出格式（所有字段用中文）：
{{
  "job_title": "岗位名称",
  "company": "公司名称（如JD中有）",
  "direction": "岗位方向（产品/运营/技术/数据等）",
  "hard_skills": ["技能1", "技能2"],
  "soft_skills": ["能力1", "能力2"],
  "bonus_points": ["加分项1", "加分项2"],
  "summary": "用一句话总结这个岗位最看重什么"
}}"""

MATCH_SCORING_SYSTEM = "你是一位资深招聘顾问，擅长评估候选人经历与岗位的匹配程度。"

MATCH_SCORING_USER = """【目标岗位】
{jd_summary_json}

【候选人所有经历】
{experiences_list}

请为每条经历打分（0-100分），并给出简短理由（不超过30字）。
只输出JSON数组，不要有任何多余说明或markdown代码块，格式：
[
  {{
    "id": "经历的id",
    "score": 85,
    "reason": "有A/B测试经验，与JD要求的数据驱动能力高度匹配"
  }}
]"""

REWRITE_SYSTEM = "你是一位专业的简历优化顾问，擅长根据目标岗位改写求职者的经历描述。"

REWRITE_USER = """【目标岗位核心需求】
岗位方向：{direction}
重点技能：{hard_skills}
核心能力：{soft_skills}

【待优化的经历原文】
公司/项目：{company}
职位/角色：{title}
时间段：{date_range}
经历要点：
{bullets}

请根据目标岗位对以上经历进行改写优化。规则：
1. 每条以动作动词开头（负责/主导/构建/分析/优化等）
2. 突出与JD最相关的技能和成果
3. 数据和事实保持不变，不得捏造
4. 每条不超过50字，保持3-4条
5. 直接输出要点列表，每条一行，不加编号或符号"""
