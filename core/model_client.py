from __future__ import annotations

import os
from dataclasses import dataclass

import requests


MODEL_MOCK = "Mock 演示模型"
MODEL_SILICONFLOW = "硅基流动 SiliconFlow"

MODEL_OPTIONS = [
    MODEL_MOCK,
    MODEL_SILICONFLOW,
]

SILICONFLOW_MODEL_OPTIONS = [
    "Qwen/Qwen2.5-72B-Instruct",
    "Qwen/Qwen2.5-32B-Instruct",
    "Qwen/Qwen2.5-14B-Instruct",
    "deepseek-ai/DeepSeek-V3",
    "deepseek-ai/DeepSeek-R1",
    "Pro/deepseek-ai/DeepSeek-V3",
    "Pro/deepseek-ai/DeepSeek-R1",
]


@dataclass(frozen=True)
class ModelConfig:
    api_key_env: str
    base_url_env: str
    default_base_url: str
    model_env: str
    default_model: str


MODEL_CONFIGS = {
    MODEL_SILICONFLOW: ModelConfig(
        api_key_env="SILICONFLOW_API_KEY",
        base_url_env="SILICONFLOW_BASE_URL",
        default_base_url="https://api.siliconflow.cn/v1",
        model_env="SILICONFLOW_MODEL",
        default_model="Qwen/Qwen2.5-72B-Instruct",
    ),
}


def get_available_model(selected_model: str) -> str:
    if selected_model == MODEL_MOCK:
        return MODEL_MOCK

    config = MODEL_CONFIGS.get(selected_model)
    if not config:
        return MODEL_MOCK

    api_key = os.getenv(config.api_key_env, "").strip()
    model = os.getenv(config.model_env, config.default_model).strip()
    base_url = os.getenv(config.base_url_env, config.default_base_url).strip()
    if not api_key or not model or not base_url:
        return MODEL_MOCK
    return selected_model


def call_model(prompt: str, model_name: str, api_model: str | None = None) -> str:
    if model_name == MODEL_MOCK:
        return build_mock_response(prompt)

    config = MODEL_CONFIGS.get(model_name)
    if not config:
        return build_mock_response(prompt)

    api_key = os.getenv(config.api_key_env, "").strip()
    base_url = os.getenv(config.base_url_env, config.default_base_url).strip().rstrip("/")
    model = (api_model or os.getenv(config.model_env, config.default_model)).strip()
    if not api_key or not base_url or not model:
        return build_mock_response(prompt)

    return call_openai_compatible_api(
        prompt=prompt,
        api_key=api_key,
        base_url=base_url,
        model=model,
    )


def call_openai_compatible_api(prompt: str, api_key: str, base_url: str, model: str) -> str:
    url = f"{base_url}/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "你是一名严谨、专业、表达清晰的教师批改助手。"},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers, timeout=90)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


def build_mock_response(prompt: str) -> str:
    if "学情分析" in prompt or "学习表现总览" in prompt:
        return """# 学情分析报告

## 学习表现总览
本批作业整体完成度较好，多数学生能够理解题目要求并给出基本完整的表达或解题过程。优秀样本体现出结构清晰、论据充分、步骤规范等特点。

## 主要问题分析
- 部分学生审题不够细致，答题重点与题目要求存在偏差。
- 过程表达略显简略，缺少必要推理、例证或语言润色。
- 个别作业存在格式不规范、结论不明确的问题。

## 能力维度分析
| 维度 | 表现 | 建议 |
| --- | --- | --- |
| 理解能力 | 基本达标 | 强化关键词圈画与题意复述 |
| 表达能力 | 中等偏上 | 训练分层表达和规范术语 |
| 迁移能力 | 有待提升 | 增加变式练习与同类题归纳 |

## 改进建议
1. 先进行审题清单训练，再进入正式作答。
2. 要求学生在答案中补充关键依据或推理链条。
3. 对典型错误进行归类讲评，并安排二次订正。

## 教师教学建议
建议下节课使用“优秀样例 + 问题样例”对照讲评，重点强化答题结构、核心概念和表达规范。"""

    return """# 作业批改结果

## 评分总览
| 项目 | 得分 |
| --- | ---: |
| 内容理解 | 24 / 30 |
| 结构与逻辑 | 22 / 30 |
| 表达规范 | 18 / 25 |
| 创新与亮点 | 12 / 15 |
| **总分** | **76 / 100** |

## 详细评语
本次作业能够围绕题目要求展开，主体内容比较完整，能体现一定的思考过程。答案中有明确观点或关键步骤，但部分论证、推理或语言表达还不够充分，导致整体说服力和规范性略受影响。

## 修改建议
1. 开头或第一步应更明确地回应题目要求。
2. 补充关键依据、例证或计算过程，避免只给结论。
3. 结尾建议进行归纳总结，使答案更完整。
4. 检查标点、术语和格式，提升卷面规范度。

## 综合评价
整体达到标准批改下的良好水平。建议在下一次作业中重点提升“过程完整性”和“表达准确性”，争取把答案从基本正确提升到清晰、严谨、有层次。"""
