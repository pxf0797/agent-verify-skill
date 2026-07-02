#!/usr/bin/env python3
"""agent-verify Skill — LLM 裁判评分器（三级仲裁体系）。

对应命令: /agent-verify:regression --judge

三级仲裁体系:
    一级: haiku 初裁（n_runs 次打分）
    二级: 方差检测（std > max_variance 触发升级）
    三级: sonnet 仲裁（覆盖 haiku 结果）

MVP 阶段此脚本不参与集成测试，V1.0 启用。
"""

import json
import math
import os
import re
import sys
import time
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_yaml_config


# ---------------------------------------------------------------------------
# 数据模型
# ---------------------------------------------------------------------------

class JudgeResult:
    """LLM 裁判评分结果。"""
    __slots__ = (
        "scores", "primary_model", "arbitration_triggered",
        "arbitration_model", "warnings", "cost_usd",
    )

    def __init__(
        self,
        scores: dict[str, dict],
        primary_model: str = "claude-haiku",
        arbitration_triggered: bool = False,
        arbitration_model: str | None = None,
        warnings: list[str] | None = None,
        cost_usd: float = 0.0,
    ):
        self.scores = scores
        self.primary_model = primary_model
        self.arbitration_triggered = arbitration_triggered
        self.arbitration_model = arbitration_model
        self.warnings = warnings or []
        self.cost_usd = cost_usd

    def to_dict(self) -> dict:
        return {s: getattr(self, s, None) for s in self.__slots__}


# ---------------------------------------------------------------------------
# 导出函数
# ---------------------------------------------------------------------------

def build_judge_prompt(
    task_description: str,
    agent_output: str,
    quality_criteria: dict[str, str],
    expected_path: list[str] | None = None,
    calibration_examples: list[dict] | None = None,
) -> str:
    """构建 LLM 裁判评分 prompt。

    Args:
        task_description: 用户原始输入 + 任务上下文
        agent_output: Agent 的完整 final_output
        quality_criteria: {维度名: 评分要求描述}
        expected_path: 预期执行路径（供参考，不直接影响评分）
        calibration_examples: 参考答案锚点列表

    Returns:
        完整的评分 prompt 字符串。
    """
    lines: list[str] = []

    # System prompt
    lines.append("你是一个 AI Agent 输出质量裁判。你的任务是评估以下 Agent 输出的质量。")
    lines.append("请严格遵循评分标准，输出必须是 JSON 格式。")
    lines.append("")

    # Quality criteria
    lines.append("## 质量评分维度")
    lines.append("请对以下每个维度从 1（最低）到 10（最高）打分：")
    lines.append("")
    for dim_name, dim_desc in quality_criteria.items():
        lines.append(f"- {dim_name}: {dim_desc}")
    lines.append("")

    # Calibration examples
    if calibration_examples:
        lines.append("## 参考答案锚点")
        lines.append("以下示例帮助你校准评分尺度：")
        lines.append("")
        for i, ex in enumerate(calibration_examples, 1):
            lines.append(f"### 示例 {i}: {'优秀' if ex.get('type') == 'good_output' else '低质量'}")
            lines.append(f"描述: {ex.get('description', '')}")
            lines.append(f"输出样本: {ex.get('agent_output', '')}")
            if "scores" in ex:
                scores_str = ", ".join(f"{k}={v}" for k, v in ex["scores"].items())
                lines.append(f"评分: {scores_str}")
            if "justification" in ex:
                lines.append(f"评分说明: {ex['justification']}")
            lines.append("")

    # Task description
    lines.append("## 任务描述")
    lines.append(task_description)
    lines.append("")

    # Expected path (optional)
    if expected_path:
        lines.append("## 预期执行路径（参考）")
        lines.append(" -> ".join(expected_path))
        lines.append("")

    # Agent output
    lines.append("## Agent 输出")
    lines.append(agent_output)
    lines.append("")

    # Output format
    lines.append("## 输出格式要求")
    lines.append("你必须在你的响应中输出一个 JSON 对象（不要包含其他文字）：")
    lines.append("")
    lines.append("```json")
    lines.append("{")
    dim_list = list(quality_criteria.keys())
    for i, dim in enumerate(dim_list):
        comma = "," if i < len(dim_list) - 1 else ""
        lines.append(f'  "{dim}": <1-10 的整数>{comma}')
    lines.append('  "justification": "简要说明评分的理由"')
    lines.append("}")
    lines.append("```")

    return "\n".join(lines)


def score_with_haiku(
    task: str,
    agent_output: str,
    quality_criteria: dict,
    dimensions: list[str] | None = None,
    n_runs: int = 3,
    max_variance: float = 1.5,
) -> JudgeResult:
    """一级初裁 + 二级方差检测 + 三级仲裁（sonnet）。

    流程:
        1. 使用 claude-haiku 打分 n_runs 次
        2. 计算每个维度的 std
        3. 若任何维度 std > max_variance → 升级到 claude-sonnet 仲裁
        4. 若升级: sonnet 打分 n_runs 次，结果覆盖 haiku 结果
        5. 返回 JudgeResult（含仲裁标记）

    若未配置 ANTHROPIC_API_KEY 环境变量，抛出 RuntimeError。
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY 环境变量未设置。"
            "LLM 裁判需要 Anthropic API 密钥才能运行。"
        )

    if dimensions is None:
        dimensions = list(quality_criteria.keys())

    prompt = build_judge_prompt(task, agent_output, quality_criteria)
    cost_accumulated = 0.0

    # ---- Level 1: Haiku 初裁 ----
    primary_model = "claude-haiku"
    haiku_scores: dict[str, list[float]] = {dim: [] for dim in dimensions}
    haiku_warnings: list[str] = []

    for run_idx in range(n_runs):
        try:
            result_text = _call_anthropic_api(
                api_key=api_key,
                model=primary_model,
                prompt=prompt,
            )
            parsed = _parse_judge_response(result_text, dimensions)
            cost_accumulated += estimate_cost(
                _estimate_tokens(prompt), _estimate_tokens(result_text), primary_model
            )

            for dim in dimensions:
                if dim in parsed["scores"]:
                    score = float(parsed["scores"][dim])
                    # 限制在 1-10
                    score = max(1.0, min(10.0, score))
                    haiku_scores[dim].append(score)
        except Exception as e:
            haiku_warnings.append(f"第 {run_idx + 1} 次 haiku 调用失败: {e}")

    # 检查是否有足够的有效评分
    final_scores: dict[str, dict] = {}
    highest_variance = 0.0
    arbitration_triggered = False

    for dim in dimensions:
        runs = haiku_scores[dim]
        if not runs:
            final_scores[dim] = {"mean": 0.0, "std": 0.0, "runs": []}
            continue
        mean = sum(runs) / len(runs)
        variance = sum((x - mean) ** 2 for x in runs) / len(runs)
        std = math.sqrt(variance)
        final_scores[dim] = {"mean": round(mean, 2), "std": round(std, 2), "runs": [round(s, 1) for s in runs]}
        if std > highest_variance:
            highest_variance = std

    warnings = haiku_warnings[:]

    # ---- Level 2: 方差检测 ----
    if highest_variance > max_variance:
        arbitration_triggered = True
        warnings.append(
            f"方差超标 (max_variance={max_variance})，"
            f"最高 std={highest_variance:.2f}，触发三级仲裁"
        )

        # ---- Level 3: Sonnet 仲裁 ----
        arb_model = "claude-sonnet"
        sonnet_scores: dict[str, list[float]] = {dim: [] for dim in dimensions}

        for run_idx in range(n_runs):
            try:
                result_text = _call_anthropic_api(
                    api_key=api_key,
                    model=arb_model,
                    prompt=prompt,
                )
                parsed = _parse_judge_response(result_text, dimensions)
                cost_accumulated += estimate_cost(
                    _estimate_tokens(prompt), _estimate_tokens(result_text), arb_model
                )

                for dim in dimensions:
                    if dim in parsed["scores"]:
                        score = float(parsed["scores"][dim])
                        score = max(1.0, min(10.0, score))
                        sonnet_scores[dim].append(score)
            except Exception as e:
                warnings.append(f"第 {run_idx + 1} 次 sonnet 仲裁调用失败: {e}")

        # 用 sonnet 结果覆盖
        for dim in dimensions:
            runs = sonnet_scores[dim]
            if not runs:
                continue
            mean = sum(runs) / len(runs)
            variance = sum((x - mean) ** 2 for x in runs) / len(runs)
            std = math.sqrt(variance)
            final_scores[dim] = {"mean": round(mean, 2), "std": round(std, 2), "runs": [round(s, 1) for s in runs]}
    else:
        arb_model = None

    return JudgeResult(
        scores=final_scores,
        primary_model=primary_model,
        arbitration_triggered=arbitration_triggered,
        arbitration_model=arb_model,
        warnings=warnings,
        cost_usd=round(cost_accumulated, 4),
    )


def estimate_cost(
    input_tokens: int,
    output_tokens: int,
    model: str = "claude-haiku",
) -> float:
    """估算单次评分的 API 成本（USD）。

    基于 Anthropic API 公开定价（2025年）:
    - Haiku: $0.25/M input, $1.25/M output
    - Sonnet: $3.00/M input, $15.00/M output
    - Opus: $15.00/M input, $75.00/M output
    """
    pricing = {
        "claude-haiku": {"input": 0.25, "output": 1.25},
        "claude-sonnet": {"input": 3.00, "output": 15.00},
        "claude-opus": {"input": 15.00, "output": 75.00},
    }
    # 回退到 haiku 定价
    price = pricing.get(model, pricing["claude-haiku"])
    input_cost = (input_tokens / 1_000_000) * price["input"]
    output_cost = (output_tokens / 1_000_000) * price["output"]
    return round(input_cost + output_cost, 6)


def check_budget(
    current_monthly_cost: float,
    max_budget: float = 50.0,
) -> bool:
    """检查是否超出月度预算。返回 True 表示可以继续。"""
    return current_monthly_cost < max_budget


# ---------------------------------------------------------------------------
# 内部辅助函数
# ---------------------------------------------------------------------------

def _call_anthropic_api(
    api_key: str,
    model: str,
    prompt: str,
    max_tokens: int = 1024,
) -> str:
    """调用 Anthropic API。

    使用 HTTP 请求直接调用（不依赖第三方 SDK）。
    """
    import urllib.request
    import urllib.error

    # Map model name to Anthropic API model ID
    model_map = {
        "claude-haiku": "claude-3-5-haiku-latest",
        "claude-sonnet": "claude-3-5-sonnet-latest",
        "claude-opus": "claude-3-opus-latest",
    }
    api_model = model_map.get(model, model)

    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }

    body = json.dumps({
        "model": api_model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            response_data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Anthropic API 调用失败 (HTTP {e.code}): {error_body}"
        ) from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Anthropic API 网络错误: {e}") from e

    # 解析响应
    content_blocks = response_data.get("content", [])
    text_parts: list[str] = []
    for block in content_blocks:
        if block.get("type") == "text":
            text_parts.append(block.get("text", ""))

    return "\n".join(text_parts)


def _parse_judge_response(text: str, dimensions: list[str]) -> dict:
    """从 LLM 响应中解析评分 JSON。"""
    # 尝试直接解析 JSON
    # 先找 ```json ... ``` 块
    json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(1))
            return _validate_judge_json(data, dimensions)
        except json.JSONDecodeError:
            pass

    # 尝试找裸 JSON
    brace_match = re.search(r"\{[^{}]*\}", text, re.DOTALL)
    if brace_match:
        try:
            data = json.loads(brace_match.group(0))
            return _validate_judge_json(data, dimensions)
        except json.JSONDecodeError:
            pass

    raise ValueError(f"无法从 LLM 响应中解析评分 JSON。响应: {text[:200]}")


def _validate_judge_json(data: dict, dimensions: list[str]) -> dict:
    """验证并规范化评分 JSON。"""
    scores = {}
    for dim in dimensions:
        if dim in data:
            try:
                scores[dim] = max(1, min(10, int(data[dim])))
            except (ValueError, TypeError):
                scores[dim] = 5  # 回退到中间值
    justification = data.get("justification", "")
    return {"scores": scores, "justification": justification}


def _estimate_tokens(text: str) -> int:
    """粗略估计 token 数量（约 4 字符/token）。"""
    return len(text) // 4 + 1


# ---------------------------------------------------------------------------
# 参考答案锚点
# ---------------------------------------------------------------------------

DEFAULT_CALIBRATION_EXAMPLES: dict[str, list[dict]] = {
    "search": [
        {
            "type": "good_output",
            "description": "搜索回答的高质量示例",
            "agent_output": (
                "2024年诺贝尔物理学奖授予John Hopfield和Geoffrey Hinton，"
                "表彰他们在人工神经网络和机器学习方面的基础性发现。"
                "来源：[诺贝尔官网](https://nobelprize.org/physics2024)"
            ),
            "scores": {"accuracy": 9, "completeness": 8, "reasonableness": 9},
            "justification": (
                "事实正确、引用来源、结构清晰。扣分原因：缺少获奖理由的简要说明。"
            ),
        },
        {
            "type": "bad_output",
            "description": "搜索回答的低质量示例",
            "agent_output": "2024年诺贝尔物理学奖得主在物理学领域做出了重要贡献。",
            "scores": {"accuracy": 3, "completeness": 2, "reasonableness": 4},
            "justification": (
                "回答过于模糊、未给出具体名字、未提供引用、信息量严重不足。"
            ),
        },
    ]
}


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="agent-verify Skill — LLM 裁判评分器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n  python scripts/llm_judge.py --task '搜索Python信息' --output 'Python是...' --criteria '{\"accuracy\": \"必须正确\"}'",
    )
    parser.add_argument("--task", required=True, help="任务描述")
    parser.add_argument("--output", required=True, help="Agent 输出内容")
    parser.add_argument("--criteria", required=True, help='质量评分维度 JSON，如 {"accuracy": "必须正确"}')
    parser.add_argument("--dimensions", help="评分维度列表 JSON，如 ['accuracy']")
    parser.add_argument("--n-runs", type=int, default=3, help="每次模型评分的运行次数")
    parser.add_argument("--max-variance", type=float, default=1.5, help="方差阈值")
    parser.add_argument("--dry-run", action="store_true", help="仅生成 prompt 不调用 API")

    args = parser.parse_args()

    try:
        criteria = json.loads(args.criteria)
    except json.JSONDecodeError as e:
        print(f"错误: criteria JSON 解析失败: {e}", file=sys.stderr)
        sys.exit(1)

    dimensions = None
    if args.dimensions:
        try:
            dimensions = json.loads(args.dimensions)
        except json.JSONDecodeError as e:
            print(f"错误: dimensions JSON 解析失败: {e}", file=sys.stderr)
            sys.exit(1)

    if args.dry_run:
        prompt = build_judge_prompt(args.task, args.output, criteria)
        print(prompt)
        sys.exit(0)

    try:
        result = score_with_haiku(
            task=args.task,
            agent_output=args.output,
            quality_criteria=criteria,
            dimensions=dimensions,
            n_runs=args.n_runs,
            max_variance=args.max_variance,
        )
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    except RuntimeError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
