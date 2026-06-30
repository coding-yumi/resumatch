import json
import os
import time

import requests
import streamlit as st

API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"


class AIClientError(Exception):
    """AI 调用异常，调用方应捕获并展示友好错误提示。"""
    pass


def get_api_key() -> str:
    try:
        api_key = st.secrets["ZHIPU_API_KEY"]
    except Exception:
        api_key = os.getenv("ZHIPU_API_KEY", "")
    if not api_key:
        raise AIClientError("未找到 ZHIPU_API_KEY，请在 .streamlit/secrets.toml 中配置。")
    return api_key


def _get_model() -> str:
    return st.secrets.get("ZHIPU_MODEL", "glm-4-flash")


def _get_temperature() -> float:
    return float(st.secrets.get("ZHIPU_TEMPERATURE", 0.6))


def call_ai(prompt: str, system: str = "", max_retries: int = 3) -> str:
    """
    调用智谱 GLM API，返回文本字符串。

    失败时自动重试（指数退避），全部重试失败后返回空字符串。
    """

    api_key = get_api_key()
    model = _get_model()
    temperature = _get_temperature()

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(
                API_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json; charset=utf-8",
                },
                data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                timeout=90,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

        except requests.exceptions.Timeout:
            last_error = "请求超时"
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else "?"
            if status == 429:
                last_error = "API 调用频率过高 (429)"
            elif status == 401:
                raise AIClientError("API Key 无效或已过期，请检查 ZHIPU_API_KEY。") from e
            else:
                body = ""
                try:
                    body = e.response.text[:200] if e.response is not None else ""
                except Exception:
                    pass
                last_error = f"HTTP {status}: {body}"
        except requests.exceptions.ConnectionError:
            last_error = "网络连接失败"
        except Exception as e:
            last_error = str(e)

        if attempt < max_retries:
            wait = 2 ** attempt
            time.sleep(wait)
            continue

    st.error(f"AI 调用失败（已重试 {max_retries} 次）：{last_error}")
    return ""
