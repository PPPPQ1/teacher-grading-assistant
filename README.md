# 教师作业批改助手 Pro

`teacher-grading-assistant-pro` 是一个基于 Python + Streamlit 的网页演示项目，用于完成作业智能批改和学情分析。项目不部署本地大模型，可通过现有 API 调用模型；未配置 API Key 时自动使用 Mock 演示模型。

## 功能

- 课程选择：语文作文、数学解答题、英语作文
- 批改模式：快速批改、标准批改、详细批改、严格评分
- 模型选择：Mock 演示模型、硅基流动 SiliconFlow
- 作业输入：直接粘贴文本，或上传 `txt`、`docx`、`pdf` 文件
- 批改结果：评分总览、详细评语、修改建议、综合评价
- 学情分析：学习表现总览、主要问题分析、能力维度分析、改进建议、教师教学建议
- 下载：批改结果和学情报告均可下载为 Markdown 文件
- 公开 Agent 链接：支持在页面中展示公网可访问的 AI Agent 地址

## 项目结构

```text
teacher-grading-assistant-pro/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── AGENTS.md
├── core/
│   ├── model_client.py
│   ├── prompt_templates.py
│   ├── file_reader.py
│   ├── grading_service.py
│   └── report_service.py
├── data/
│   └── sample_homework.txt
└── outputs/
    └── .gitkeep
```

## 运行方法

1. 进入项目目录：

```bash
cd teacher-grading-assistant-pro
```

2. 创建并激活虚拟环境：

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

4. 配置环境变量：

```bash
cp .env.example .env
```

如果只演示 Mock 模型，可以不填写任何 API Key。

5. 启动应用：

```bash
streamlit run app.py
```

启动后浏览器会打开本地页面，通常地址为：

```text
http://localhost:8501
```

## 环境变量

`.env.example` 中提供了全部配置项。硅基流动 API Key 可在控制台的 API 密钥页面创建：

```text
https://cloud.siliconflow.cn/account/ak
```

常用配置如下：

```env
SILICONFLOW_API_KEY=
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
SILICONFLOW_MODEL=Qwen/Qwen2.5-72B-Instruct

PUBLIC_AGENT_NAME=教师作业批改助手 Pro 在线 Agent
PUBLIC_AGENT_URL=
```

当用户选择非 Mock 模型但缺少必要配置时，系统会自动切换到 Mock 演示模型，保证应用可运行。

## 公开访问部署

本地 `http://localhost:8501` 只能在自己的电脑访问。老师要求“可公开访问的 AI Agent 链接”时，需要把项目部署到公网平台。

推荐方式：Streamlit Community Cloud。

1. 将本项目上传到 GitHub 仓库。
2. 打开 Streamlit Community Cloud，新建 App。
3. Repository 选择你的 GitHub 仓库。
4. Main file path 填写：

```text
app.py
```

5. 在 App Secrets 中添加配置：

```toml
SILICONFLOW_API_KEY = "你的硅基流动 API Key"
SILICONFLOW_BASE_URL = "https://api.siliconflow.cn/v1"
SILICONFLOW_MODEL = "Qwen/Qwen2.5-72B-Instruct"
PUBLIC_AGENT_NAME = "教师作业批改助手 Pro 在线 Agent"
PUBLIC_AGENT_URL = "部署完成后得到的公网地址"
```

本项目会同时读取 `.env` 和 Streamlit Secrets；本地开发用 `.env`，部署到 Streamlit Cloud 时建议使用 Secrets，不要把真实 API Key 提交到 GitHub。

6. 部署成功后会得到类似下面的公网地址：

```text
https://your-app-name.streamlit.app
```

7. 将这个地址填入 `PUBLIC_AGENT_URL`。页面中的“公开 Agent”标签页会展示该公开入口。

也可以使用 Dify、Coze、FastGPT、Hugging Face Spaces 等平台创建公开 Agent，然后把公开访问地址填入 `PUBLIC_AGENT_URL`。

## 演示步骤

1. 启动应用后，在侧边栏选择课程类型、批改模式和模型。
2. 首次演示建议选择 `Mock 演示模型`；配置 `SILICONFLOW_API_KEY` 后可选择 `硅基流动 SiliconFlow`。
3. 在“作业批改”页粘贴文本，或上传 `data/sample_homework.txt`。
4. 点击“开始批改”，查看 Markdown 结构化结果。
5. 点击“下载 Markdown 批改结果”保存文件。
6. 切换到“学情分析”页，粘贴多份批改结果。
7. 点击“生成学情分析报告”，查看并下载报告。
8. 切换到“公开 Agent”页，检查是否展示公网可访问链接。

## 测试输入样例

```text
题目：谈谈你对“坚持”的理解

坚持是一种重要的品质。生活中很多事情都不是一下子就能成功的，需要我们不断努力。比如学习英语时，背单词很枯燥，但是如果每天坚持积累，就会慢慢看到进步。

我认为坚持不是盲目地做同一件事，而是在目标明确的情况下不断调整方法。遇到困难时，我们可以请教老师和同学，也可以总结自己的错误。只要不轻易放弃，就更有可能实现目标。

所以，坚持能帮助我们养成自律的习惯，也能让我们在面对挑战时更加勇敢。
```

## 注意事项

- 本项目不实现真实付费功能。
- 本项目不本地部署大模型。
- PDF 文本提取效果取决于 PDF 是否包含可复制文本；扫描件可能无法正确读取。
