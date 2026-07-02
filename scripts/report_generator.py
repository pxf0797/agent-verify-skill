#!/usr/bin/env python3
"""agent-verify Skill — 报告生成器。

对应命令: /agent-verify:report

将 assertion_results + judge_scores + comparison_data
渲染为 Markdown / JSON / HTML 格式报告。
"""

import json
import os
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import save_json, load_json


# ---------------------------------------------------------------------------
# 导出函数
# ---------------------------------------------------------------------------

def generate_regression_report(
    result: dict,
    format: str = "markdown",
) -> str:
    """生成回归测试报告。

    Args:
        result: run_regression() 返回的 dict
        format: "markdown" | "json" | "html"

    Returns:
        格式化的报告字符串。
    """
    if format == "json":
        return json.dumps(result, ensure_ascii=False, indent=2)

    summary = result.get("summary", {})
    cases = result.get("cases", [])
    baseline_comparison = result.get("baseline_comparison")

    lines: list[str] = []

    if format == "html":
        return _generate_html_report(result)
    elif format == "markdown":
        lines.append(f"# 回归测试报告\n")
        lines.append(f"**套件**: {summary.get('suite_name', 'N/A')}\n")

        # 摘要
        lines.append("## 总体摘要\n")
        lines.append(f"| 指标 | 值 |")
        lines.append(f"|------|-----|")
        lines.append(f"| 总用例 | {summary.get('total_cases', 0)} |")
        lines.append(f"| 通过 | {summary.get('passed_cases', 0)} |")
        lines.append(f"| 失败 | {summary.get('failed_cases', 0)} |")
        lines.append(f"| 断言通过率 | {summary.get('assertion_pass_rate', 0):.1%} |")
        lines.append(f"| 平均耗时 | {summary.get('avg_duration_ms', 0)}ms |")
        lines.append(f"| 平均步数 | {summary.get('avg_steps', 0):.1f} |")
        lines.append("")

        # LLM 评分
        llm_scores = summary.get("llm_scores")
        if llm_scores:
            lines.append("## LLM 评分\n")
            lines.append(format_score_table(llm_scores))
            lines.append("")

        # 失败详情
        failed_details = summary.get("failed_details", [])
        if failed_details:
            lines.append("## 失败详情\n")
            lines.append("| 用例 | 断言 | 原因 |")
            lines.append("|------|------|------|")
            for fd in failed_details:
                lines.append(f"| {fd.get('case_id', 'N/A')} | {fd.get('assertion_id', 'N/A')} | {fd.get('reason', '')} |")
            lines.append("")

        # 逐用例详情
        if cases:
            lines.append("## 逐用例详情\n")
            for case in cases:
                status = "PASS" if case.get("error") is None and all(
                    r.get("pass_") for r in case.get("assertion_results", [])
                ) else "FAIL"
                lines.append(f"### {case.get('case_id', 'N/A')} — {status}\n")
                lines.append(f"- **名称**: {case.get('case_name', 'N/A')}")
                lines.append(f"- **耗时**: {case.get('duration_ms', 0)}ms")
                lines.append(f"- **步数**: {case.get('steps', 0)}")
                if case.get("error"):
                    lines.append(f"- **错误**: {case['error']}")
                if case.get("assertion_results"):
                    lines.append("")
                    lines.append(format_assertion_table(case["assertion_results"]))
                lines.append("")

        # 基线对比
        if baseline_comparison:
            lines.append("## 基线对比\n")
            lines.append(format_diff_table(baseline_comparison.get("diffs", [])))
            lines.append("")

        # Flags
        flags = summary.get("flags", {})
        if flags:
            lines.append(f"**运行时 Flag**: `{json.dumps(flags)}`\n")

    return "\n".join(lines)


def generate_comparison_report(
    comparison: dict,
    format: str = "markdown",
) -> str:
    """生成 A/B 对比报告。"""
    if format == "json":
        return json.dumps(comparison, ensure_ascii=False, indent=2)
    if format == "html":
        return _generate_html_comparison(comparison)

    lines: list[str] = []
    lines.append(f"# Feature Flag A/B 对比报告\n")
    lines.append(f"**Flag**: `{comparison.get('flag_name', 'N/A')}`\n")

    diffs = comparison.get("diffs", [])
    if diffs:
        lines.append("## 维度对比\n")
        lines.append(format_diff_table(diffs))
        lines.append("")

    per_case = comparison.get("per_case_diffs", [])
    if per_case:
        lines.append("## 逐用例变化\n")
        for cd in per_case:
            lines.append(f"### {cd.get('case_id', 'N/A')}\n")
            perf = cd.get("performance_change", {})
            if perf:
                lines.append(f"- 耗时变化: {perf.get('duration_change_ms', 'N/A')}ms")
                lines.append(f"- 步数变化: {perf.get('steps_change', 0)}")
            lines.append("")

    lines.append(f"**结论**: {comparison.get('conclusion', 'N/A')}\n")
    return "\n".join(lines)


def generate_baseline_comparison_report(
    comparison: dict,
    format: str = "markdown",
) -> str:
    """生成基线对比报告。"""
    if format == "json":
        return json.dumps(comparison, ensure_ascii=False, indent=2)

    lines: list[str] = []
    lines.append("# 基线对比报告\n")
    lines.append(f"**基线1**: {comparison.get('baseline1_name', 'N/A')}")
    lines.append(f"**基线2**: {comparison.get('baseline2_name', 'N/A')}\n")

    diffs = comparison.get("diffs", [])
    if diffs:
        lines.append("## 维度对比\n")
        lines.append(format_diff_table(diffs))
        lines.append("")

    return "\n".join(lines)


def write_report(content: str, output_path: str) -> str:
    """将报告内容写入文件。返回文件路径。"""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    return output_path


# ---------------------------------------------------------------------------
# 内部格式化函数
# ---------------------------------------------------------------------------

def format_assertion_table(results: list) -> str:
    """将断言结果列表格式化为 Markdown 表格。"""
    if not results:
        return "（无断言结果）"

    lines = ["| ID | 名称 | 类型 | 结果 | 原因 |", "|-----|------|------|------|------|"]
    for r in results:
        status = "PASS" if r.get("pass_") else "FAIL"
        reason = (r.get("reason") or "")[:60]
        lines.append(
            f"| {r.get('assertion_id', 'N/A')} "
            f"| {r.get('assertion_name', '')[:30]} "
            f"| {r.get('assertion_type', '')} "
            f"| {status} "
            f"| {reason} |"
        )
    return "\n".join(lines)


def format_score_table(scores: dict) -> str:
    """将 LLM 评分格式化为 Markdown 表格。"""
    if not scores:
        return "（无评分数据）"

    lines = ["| 维度 | 均值 | 标准差 |", "|------|------|--------|"]
    for dim, data in scores.items():
        mean = data.get("mean", "N/A")
        std = data.get("std", "N/A")
        lines.append(f"| {dim} | {mean} | {std} |")
    return "\n".join(lines)


def format_diff_table(diffs: list) -> str:
    """将 diff 数据格式化为 Markdown 对比表格。"""
    if not diffs:
        return "（无差异数据）"

    lines = [
        "| 维度 | OFF 值 | ON 值 | 变化 | 方向 | 显著 |",
        "|------|--------|-------|------|------|------|",
    ]
    for d in diffs:
        lines.append(
            f"| {d.get('dimension', 'N/A')} "
            f"| {d.get('off_value', 'N/A')} "
            f"| {d.get('on_value', 'N/A')} "
            f"| {d.get('change', 'N/A')} "
            f"| {d.get('direction', 'N/A')} "
            f"| {d.get('significant', False)} |"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# HTML 报告
# ---------------------------------------------------------------------------

def _generate_html_report(result: dict) -> str:
    """生成 HTML 格式的回归测试报告。"""
    summary = result.get("summary", {})
    failed = summary.get("failed_details", [])
    pass_rate = summary.get("assertion_pass_rate", 0) * 100

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>回归测试报告 — {summary.get('suite_name', 'N/A')}</title>
<style>
body {{ font-family: -apple-system, sans-serif; max-width: 960px; margin: auto; padding: 20px; }}
table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background: #f5f5f5; }}
.pass {{ color: #22c55e; }} .fail {{ color: #ef4444; }}
</style>
</head>
<body>
<h1>回归测试报告</h1>
<p><strong>套件</strong>: {summary.get('suite_name', 'N/A')}</p>
<h2>总体摘要</h2>
<table>
<tr><th>总用例</th><td>{summary.get('total_cases', 0)}</td></tr>
<tr><th>通过</th><td class="pass">{summary.get('passed_cases', 0)}</td></tr>
<tr><th>失败</th><td class="fail">{summary.get('failed_cases', 0)}</td></tr>
<tr><th>断言通过率</th><td>{pass_rate:.1f}%</td></tr>
<tr><th>平均耗时</th><td>{summary.get('avg_duration_ms', 0)}ms</td></tr>
</table>"""
    if failed:
        html += "<h2>失败详情</h2><table><tr><th>用例</th><th>断言</th><th>原因</th></tr>"
        for fd in failed:
            html += f"<tr><td>{fd.get('case_id', '')}</td><td>{fd.get('assertion_id', '')}</td><td>{fd.get('reason', '')}</td></tr>"
        html += "</table>"
    html += "</body></html>"
    return html


def _generate_html_comparison(comparison: dict) -> str:
    """生成 HTML 格式的对比报告。"""
    return _generate_html_report(comparison)  # 简化实现


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="agent-verify Skill — 报告生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n  python scripts/report_generator.py --input result.json --format markdown --output report.md",
    )
    parser.add_argument("--input", required=True, help="输入 JSON 结果文件路径")
    parser.add_argument(
        "--format", default="markdown", choices=["markdown", "json", "html"],
        help="输出格式",
    )
    parser.add_argument("--output", help="输出文件路径（可选，默认 stdout）")
    parser.add_argument(
        "--type", default="regression", choices=["regression", "comparison", "baseline"],
        help="报告类型",
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"错误: 输入文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        data = load_json(args.input)
    except (FileNotFoundError, ValueError) as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

    if args.type == "regression":
        content = generate_regression_report(data, args.format)
    elif args.type == "comparison":
        content = generate_comparison_report(data, args.format)
    elif args.type == "baseline":
        content = generate_baseline_comparison_report(data, args.format)

    if args.output:
        path = write_report(content, args.output)
        print(f"报告已写入: {path}")
    else:
        print(content)
