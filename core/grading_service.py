from __future__ import annotations

from core.model_client import call_model
from core.prompt_templates import build_grading_prompt


SUPPORTED_COURSES = ["语文作文", "数学解答题", "英语作文"]
SUPPORTED_MODES = ["快速批改", "标准批改", "详细批改", "严格评分"]


def grade_homework(
    homework_text: str,
    course: str,
    mode: str,
    model_name: str,
    api_model: str | None = None,
) -> str:
    prompt = build_grading_prompt(
        homework_text=homework_text,
        course=course,
        mode=mode,
    )
    return call_model(prompt=prompt, model_name=model_name, api_model=api_model)
