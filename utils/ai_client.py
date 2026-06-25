from zhipuai import ZhipuAI
import streamlit as st

def get_client():
    # 优先从 st.secrets 读取（Streamlit Cloud用），其次从环境变量读取（本地用）
    try:
        api_key = st.secrets["ZHIPU_API_KEY"]
    except Exception:
        import os
        api_key = os.getenv("ZHIPU_API_KEY", "")
    if not api_key:
        st.error("❌ 未找到 ZHIPU_API_KEY，请在 .streamlit/secrets.toml 中配置")
        st.stop()
    return ZhipuAI(api_key=api_key)

def call_ai(prompt: str, system: str = "") -> str:
    """调用智谱GLM API，返回文本字符串。出错时返回空字符串并显示错误。"""
    try:
        client = get_client()
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model="glm-4-flash",   # 免费模型，够用
            messages=messages,
            temperature=0.6
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"AI调用失败：{e}")
        return ""
