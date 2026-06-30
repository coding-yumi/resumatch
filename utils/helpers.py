"""
ResuMatch 公共工具函数，供各页面复用。
"""

import json
import re


def strip_json_fence(text: str) -> str:
    """去除 AI 返回内容中的 markdown 代码块标记。"""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def parse_ai_json(text: str) -> tuple[dict | None, str]:
    """将 AI 返回的文本解析为 dict，失败返回 (None, raw_text)。"""
    cleaned = strip_json_fence(text)
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            return data, cleaned
        return None, cleaned
    except json.JSONDecodeError:
        return None, cleaned


def parse_json_array(text: str) -> tuple[list | None, str]:
    """将 AI 返回的文本解析为 list，失败返回 (None, raw_text)。"""
    cleaned = strip_json_fence(text)
    try:
        data = json.loads(cleaned)
        if isinstance(data, list):
            return data, cleaned
        return None, cleaned
    except json.JSONDecodeError:
        return None, cleaned


def parse_rewrite_lines(text: str) -> list[str]:
    """将 AI 改写输出解析为逐条列表，自动去除编号和项目符号。"""
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    cleaned = []
    for line in lines:
        line = re.sub(r"^[\d]+[\.\)、]\s*", "", line)
        line = re.sub(r"^[-•*✨]\s*", "", line)
        if line:
            cleaned.append(line)
    return cleaned


DATE_PATTERN = re.compile(r"^\d{4}-\d{2}$")


def validate_date(value: str, field_name: str) -> str | None:
    """验证 YYYY-MM 格式日期，返回错误信息或 None。"""
    if not value.strip():
        return f"{field_name}不能为空"
    if field_name == "结束时间" and value.strip() == "至今":
        return None
    if not DATE_PATTERN.match(value.strip()):
        return f"{field_name}格式应为 YYYY-MM（如 2024-07）"
    return None
