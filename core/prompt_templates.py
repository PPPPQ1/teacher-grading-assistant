from __future__ import annotations


def build_grading_prompt(homework_text: str, course: str, mode: str) -> str:
    return f"""请作为专业教师，对以下作业进行智能批改。

课程类型：{course}
批改模式：{mode}

请严格使用 Markdown 输出，并包含以下四个部分：

## 评分总览
请用表格给出分项评分和总分，满分 100 分。

## 详细评语
请指出作业的优点、不足和关键问题。

## 修改建议
请给出可执行的修改建议，适合学生据此订正。

## 综合评价
请用简洁语言总结学生当前水平和下一步提升方向。

作业内容：
{homework_text}
"""


def build_report_prompt(grading_results: str) -> str:
    return f"""请根据多份作业批改结果生成一份班级或学生阶段性学情分析报告。

请严格使用 Markdown 输出，并包含以下五个部分：

## 学习表现总览
概括整体表现、完成质量和分数趋势。

## 主要问题分析
归纳高频错误、共性短板和可能原因。

## 能力维度分析
从理解能力、表达能力、逻辑能力、迁移应用能力等角度分析。

## 改进建议
给出学生可执行的学习改进建议。

## 教师教学建议
给出教师后续讲评、训练和分层辅导建议。

批改结果集合：
{grading_results}
"""
