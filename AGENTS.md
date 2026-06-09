# AGENTS.md

本项目是一个 Python + Streamlit 演示应用，中文产品名为“教师作业批改助手 Pro”。

## 开发约定

- 不要在代码中写死任何 API Key。
- 默认必须支持 Mock 演示模型，保证无外部服务时也能运行。
- 大模型调用统一放在 `core/model_client.py`。
- Prompt 模板统一放在 `core/prompt_templates.py`。
- 文件读取逻辑统一放在 `core/file_reader.py`。
- 页面入口为 `app.py`。

## 验证建议

优先运行：

```bash
python -m compileall .
streamlit run app.py
```
