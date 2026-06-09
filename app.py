from __future__ import annotations

from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from core.file_reader import read_uploaded_file
from core.grading_service import SUPPORTED_COURSES, SUPPORTED_MODES, grade_homework
from core.model_client import MODEL_MOCK, MODEL_OPTIONS, SILICONFLOW_MODEL_OPTIONS, get_available_model
from core.report_service import generate_learning_report
from core.settings import get_setting


load_dotenv()

st.set_page_config(
    page_title="教师作业批改助手 Pro",
    page_icon="📝",
    layout="wide",
)


def render_sidebar() -> tuple[str, str, str, str | None]:
    st.sidebar.title("教师作业批改助手 Pro")
    st.sidebar.caption("Python + Streamlit 智能批改演示项目")

    course = st.sidebar.selectbox("课程类型", SUPPORTED_COURSES)
    mode = st.sidebar.selectbox("批改模式", SUPPORTED_MODES, index=1)
    selected_model = st.sidebar.selectbox("批改大模型", MODEL_OPTIONS)
    api_model = None
    if selected_model != MODEL_MOCK:
        api_model = st.sidebar.selectbox("硅基流动模型", SILICONFLOW_MODEL_OPTIONS)

    effective_model = get_available_model(selected_model)
    if effective_model != selected_model:
        st.sidebar.warning(f"未检测到 {selected_model} API Key，已自动切换到 Mock 演示模型。")
        api_model = None
    else:
        st.sidebar.success(f"当前模型：{effective_model}")
        if api_model:
            st.sidebar.caption(f"模型 ID：{api_model}")

    return course, mode, effective_model, api_model


def build_download_name(prefix: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.md"


def get_public_agent_config() -> tuple[str, str]:
    agent_name = get_setting("PUBLIC_AGENT_NAME", "教师作业批改助手 Pro 在线 Agent")
    agent_url = get_setting("PUBLIC_AGENT_URL")
    return agent_name, agent_url


def render_grading_tab(course: str, mode: str, model_name: str, api_model: str | None) -> None:
    st.header("作业智能批改")

    input_col, preview_col = st.columns([1.1, 0.9])
    with input_col:
        pasted_text = st.text_area(
            "直接粘贴作业内容",
            height=260,
            placeholder="例如：粘贴学生作文、数学解题过程或英语作文...",
        )
        uploaded_file = st.file_uploader("或上传作业文件", type=["txt", "docx", "pdf"])

    file_text = ""
    if uploaded_file is not None:
        try:
            file_text = read_uploaded_file(uploaded_file)
        except Exception as exc:  # noqa: BLE001 - UI needs a friendly message for any reader failure.
            st.error(f"文件读取失败：{exc}")

    homework_text = (pasted_text or file_text).strip()
    with preview_col:
        st.subheader("输入预览")
        if homework_text:
            st.markdown(homework_text[:3000])
            if len(homework_text) > 3000:
                st.caption("内容较长，预览仅显示前 3000 个字符。")
        else:
            st.info("请粘贴文本或上传 txt、docx、pdf 文件。")

    if "grading_result" not in st.session_state:
        st.session_state.grading_result = ""

    grade_clicked = st.button("开始批改", type="primary", use_container_width=True)
    if grade_clicked:
        if not homework_text:
            st.warning("请先输入或上传作业内容。")
        else:
            with st.spinner("正在生成批改结果..."):
                st.session_state.grading_result = grade_homework(
                    homework_text=homework_text,
                    course=course,
                    mode=mode,
                    model_name=model_name,
                    api_model=api_model,
                )

    if st.session_state.grading_result:
        st.divider()
        st.subheader("批改结果")
        st.markdown(st.session_state.grading_result)
        st.download_button(
            label="下载 Markdown 批改结果",
            data=st.session_state.grading_result,
            file_name=build_download_name("grading_result"),
            mime="text/markdown",
            use_container_width=True,
        )


def render_report_tab(model_name: str, api_model: str | None) -> None:
    st.header("学情分析报告")
    grading_results = st.text_area(
        "粘贴多份批改结果",
        height=340,
        placeholder="请粘贴多名学生或多次作业的 Markdown 批改结果...",
    )

    if "learning_report" not in st.session_state:
        st.session_state.learning_report = ""

    if st.button("生成学情分析报告", type="primary", use_container_width=True):
        if not grading_results.strip():
            st.warning("请先粘贴批改结果。")
        else:
            with st.spinner("正在生成学情分析报告..."):
                st.session_state.learning_report = generate_learning_report(
                    grading_results=grading_results,
                    model_name=model_name,
                    api_model=api_model,
                )

    if st.session_state.learning_report:
        st.divider()
        st.subheader("报告结果")
        st.markdown(st.session_state.learning_report)
        st.download_button(
            label="下载 Markdown 学情报告",
            data=st.session_state.learning_report,
            file_name=build_download_name("learning_report"),
            mime="text/markdown",
            use_container_width=True,
        )


def render_public_agent_tab() -> None:
    st.header("公开 AI Agent 链接")
    agent_name, agent_url = get_public_agent_config()

    if agent_url:
        st.success("已配置公开访问入口。")
        st.markdown(f"### [{agent_name}]({agent_url})")
        st.caption(agent_url)
        st.link_button("打开公开 AI Agent", agent_url, use_container_width=True)
    else:
        st.warning("尚未配置公开访问链接。")
        st.markdown(
            """
请在 `.env` 中配置：

```env
PUBLIC_AGENT_NAME=教师作业批改助手 Pro 在线 Agent
PUBLIC_AGENT_URL=https://你的公网访问链接
```

这个链接可以是 Streamlit Cloud、Hugging Face Spaces、Dify、Coze、FastGPT 等平台发布后的公开地址。
"""
        )


def main() -> None:
    course, mode, model_name, api_model = render_sidebar()

    st.title("教师作业批改助手 Pro")
    st.caption("输入作业内容，选择课程、批改模式和模型，即可生成结构化 Markdown 批改结果。")

    grading_tab, report_tab, public_agent_tab = st.tabs(["作业批改", "学情分析", "公开 Agent"])
    with grading_tab:
        render_grading_tab(course, mode, model_name, api_model)
    with report_tab:
        render_report_tab(model_name, api_model)
    with public_agent_tab:
        render_public_agent_tab()


if __name__ == "__main__":
    main()
