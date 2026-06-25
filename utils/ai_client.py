import json
import os

import requests
import streamlit as st

API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"


def get_api_key() -> str:
    try:
        api_key = st.secrets["ZHIPU_API_KEY"]
    except Exception:
        api_key = os.getenv("ZHIPU_API_KEY", "")
    if not api_key:
        st.error("❌ 未找到 ZHIPU_API_KEY，请在 .streamlit/secrets.toml 中配置")
        st.stop()
    return api_key


def call_ai(prompt: str, system: str = "") -> str:
    """调用智谱 GLM API，返回文本字符串。出错时返回空字符串并显示错误。"""
    try:
        api_key = get_api_key()
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json; charset=utf-8",
            },
            data=json.dumps(
                {"model": "glm-4-flash", "messages": messages, "temperature": 0.6},
                ensure_ascii=False,
            ).encode("utf-8"),
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"AI调用失败：{e}")
        return ""
