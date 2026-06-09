from __future__ import annotations

from core.model_client import call_model
from core.prompt_templates import build_report_prompt


def generate_learning_report(
    grading_results: str,
    model_name: str,
    api_model: str | None = None,
) -> str:
    prompt = build_report_prompt(grading_results=grading_results)
    return call_model(prompt=prompt, model_name=model_name, api_model=api_model)
