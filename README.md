# ResuMatch 🎯

**AI-powered resume experience matcher & rewriter**

**AI 驱动的简历经历匹配与优化工具**

ResuMatch helps job seekers paste a job description (JD), automatically extract key requirements, match their existing experiences, and generate tailored resume bullet points — all in about 30 seconds.

ResuMatch 帮助求职者粘贴岗位 JD，自动提取关键要求，匹配已有经历，并生成针对性的简历要点描述，全程约 30 秒完成。

---

## Features / 功能

- **Experience Library** — Manage internship and project experiences  
  **经历库** — 管理实习与项目经历

- **JD Analysis** — AI extracts skills, direction, and priorities from job posts  
  **JD 分析** — AI 提取岗位技能、方向与核心要求

- **Smart Matching** — Score experiences against JD and rewrite top matches  
  **智能匹配** — 对经历打分并改写 Top 推荐描述

---

## Local Setup / 本地运行

### 1. Clone & install dependencies

```bash
git clone <your-repo-url>
cd resumatch
pip install -r requirements.txt
```

### 2. Configure API Key

Create `.streamlit/secrets.toml`:

```toml
ZHIPU_API_KEY = "your-zhipu-api-key"
```

Get your key at [智谱开放平台](https://open.bigmodel.cn/).

Alternatively, set the environment variable:

```bash
export ZHIPU_API_KEY="your-zhipu-api-key"
```

### 3. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](https://coding-yumi-resumatch.streamlit.app) in your browser.

---

## Deploy to Streamlit Cloud / 部署到 Streamlit Cloud

1. Push the project to a **GitHub** repository  
   将项目推送到 GitHub 仓库

2. Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub  
   访问 Streamlit Cloud 并用 GitHub 登录

3. Click **New app** → select your repo, branch, and main file `app.py`  
   点击 **New app**，选择仓库、分支和入口文件 `app.py`

4. Open **Advanced settings → Secrets** and add:

   ```toml
   ZHIPU_API_KEY = "your-zhipu-api-key"
   ```

5. Click **Deploy** — the app will be live in a few minutes  
   点击 **Deploy**，数分钟后即可访问

> **Note:** Do not commit real API keys. `.streamlit/secrets.toml` is listed in `.gitignore`.

---

## Tech Highlights / 技术亮点

1. **Multi-step AI pipeline with structured JSON output** — JD parsing, batch experience scoring, and per-item rewriting are orchestrated as separate prompt stages with fence-stripped JSON parsing and graceful fallbacks.  
   **多阶段 AI 流水线 + 结构化 JSON 输出** — JD 解析、批量经历评分、逐条改写分步编排，含 JSON 容错解析与降级处理。

2. **Session-state driven workflow across Streamlit multipage app** — `jd_analysis` and `match_results` persist across pages, enabling a seamless three-page user journey without a backend database.  
   **Streamlit 多页面 + Session State 工作流** — 跨页面共享分析结果，无需后端数据库即可串联完整用户流程。

3. **Modular prompt & data layer design** — Prompts, AI client, JSON data manager, and theme utilities are decoupled for easy iteration and interview-ready architecture discussion.  
   **模块化 Prompt 与数据层设计** — Prompt 模板、API 封装、JSON 存储、主题样式解耦，便于迭代与架构讲解。

---

## Project Structure / 项目结构

```
resumatch/
├── app.py                 # Main entry & home page
├── pages/
│   ├── 1_经历库.py         # Experience library
│   ├── 2_JD分析.py         # JD analysis
│   └── 3_匹配结果.py       # Matching & rewriting
├── utils/
│   ├── ai_client.py       # Zhipu GLM API wrapper
│   ├── data_manager.py    # JSON persistence
│   ├── prompts.py         # Prompt templates
│   └── theme.py           # Global CSS theme
├── data/
│   └── experiences.json
├── .streamlit/
│   └── secrets.toml
└── requirements.txt
```

---

## Screenshots

<!-- Add screenshots here after running the app -->

| Home | JD Analysis | Match Results |
|------|-------------|---------------|
| _screenshot pending_ | _screenshot pending_ | _screenshot pending_ |

---

## License

MIT (or specify your license)
