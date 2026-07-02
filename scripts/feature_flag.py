#!/usr/bin/env python3
"""agent-verify Skill — Feature Flag 管理 + A/B 对比。

对应命令: /agent-verify:compare

从 config.yaml 读取/验证 Flag 定义，
注入 AGENT_FLAG_<NAME> 环境变量，
Flag=OFF/ON 双跑编排，
逐维度 diff 对比，生成对比报告。

⚠️ MVP 阶段此脚本不参与集成测试，V1.0 启用。
"""

import json
import os
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (
    load_yaml_config, build_flag_env, build_all_flag_env,
    PROJECT_DIR_NAME, SUITE_DIR, BASELINE_DIR,
)
from regression_runner import run_regression, load_baseline, list_baselines, save_baseline
from report_generator import generate_comparison_report, write_report


# ---------------------------------------------------------------------------
# 导出函数
# ---------------------------------------------------------------------------

def load_flag_definitions(config: dict) -> list[dict]:
    """从 config.yaml 解析 feature_flags.flags 列表。

    返回预定义的 Flag 定义。
    """
    feature_flags = config.get("feature_flags", {})
    if not isinstance(feature_flags, dict):
        raise ValueError("'feature_flags' 配置必须为 dict 类型")

    flags = feature_flags.get("flags", [])
    if not isinstance(flags, list):
        raise ValueError("'feature_flags.flags' 必须为列表")

    if not flags:
        print("警告: config.yaml 中未定义任何 Feature Flag。", file=sys.stderr)

    # 验证每个 Flag
    validated: list[dict] = []
    for idx, flag in enumerate(flags):
        if not isinstance(flag, dict):
            raise ValueError(f"第 {idx} 个 Flag 不是 dict 类型")
        if "name" not in flag:
            raise ValueError(f"第 {idx} 个 Flag 缺少 'name' 字段")
        if "description" not in flag:
            print(f"警告: Flag '{flag['name']}' 缺少 'description' 字段", file=sys.stderr)

        validated.append(flag)

    return validated


def validate_flag(flag_name: str, config: dict) -> dict:
    """验证 Flag 是否在 config.yaml 中预定义。

    未定义的 Flag 抛出 ValueError（防御拼写错误）。
    返回 Flag 定义 dict。
    """
    flags = load_flag_definitions(config)
    for flag in flags:
        if flag["name"] == flag_name:
            return flag

    available = [f["name"] for f in flags]
    raise ValueError(
        f"Flag '{flag_name}' 未在 config.yaml 的 feature_flags.flags 中定义。"
        f"可用 Flag: {available}"
    )


def run_flag_comparison(
    flag_name: str,
    suite_file: str,
    config_file: str,
    baseline_name: str | None = None,
    enable_judge: bool = False,
) -> dict:
    """执行 Feature Flag A/B 对比。

    Args:
        flag_name: Flag 名称（必须在 config.yaml 中预定义）
        suite_file: 测试套件 YAML 文件路径
        config_file: config.yaml 文件路径
        baseline_name: 若提供，用基线数据替代 Flag=OFF 的实际运行
        enable_judge: 是否启用 LLM 裁判

    Returns:
        {
            "flag_name": str,
            "off_summary": RegressionSummary (as dict),
            "on_summary": RegressionSummary (as dict),
            "diffs": [...],
            "per_case_diffs": [...],
            "conclusion": str,
        }
    """
    config = load_yaml_config(config_file)

    # 验证 Flag
    flag_def = validate_flag(flag_name, config)

    # ---- Flag=OFF: 运行回归 ----
    print(f"运行 Flag={flag_name}=OFF...", file=sys.stderr)
    if baseline_name:
        # 从基线加载
        verify_dir = os.path.dirname(config_file)
        baselines_dir = os.path.join(verify_dir, BASELINE_DIR)
        all_baselines = list_baselines(baselines_dir)
        matched = [b for b in all_baselines if b["name"] == baseline_name]
        if not matched:
            raise ValueError(
                f"未找到名为 '{baseline_name}' 的基线。"
                f"可用: {[b['name'] for b in all_baselines]}"
            )
        baseline_data = load_baseline(matched[0]["path"])
        off_result = baseline_data
        print(f"  从基线 '{baseline_name}' 加载 OFF 数据。", file=sys.stderr)
    else:
        off_result = run_regression(
            suite_file=suite_file,
            config_file=config_file,
            scope="all",
            enable_judge=enable_judge,
        )

    off_summary = off_result.get("summary", {})

    # ---- Flag=ON: 运行回归 ----
    print(f"运行 Flag={flag_name}=ON...", file=sys.stderr)
    flag_overrides = build_flag_env(flag_name, "ON")
    on_result = run_regression(
        suite_file=suite_file,
        config_file=config_file,
        scope="all",
        enable_judge=enable_judge,
        flag_overrides=flag_overrides,
    )
    on_summary = on_result.get("summary", {})

    # ---- Diff 对比 ----
    diffs = _compute_diffs(off_summary, on_summary)

    # 逐用例对比
    off_cases = {c["case_id"]: c for c in off_result.get("cases", [])}
    on_cases = {c["case_id"]: c for c in on_result.get("cases", [])}
    all_case_ids = set(list(off_cases.keys()) + list(on_cases.keys()))

    per_case_diffs: list[dict] = []
    for cid in sorted(all_case_ids):
        off_case = off_cases.get(cid, {})
        on_case = on_cases.get(cid, {})

        assertion_changes = _diff_assertions(
            off_case.get("assertion_results", []),
            on_case.get("assertion_results", []),
        )

        score_changes = _diff_scores(
            off_case.get("judge_scores"),
            on_case.get("judge_scores"),
        )

        perf_before = {
            "duration_ms": off_case.get("duration_ms", 0),
            "steps": off_case.get("steps", 0),
        }
        perf_after = {
            "duration_ms": on_case.get("duration_ms", 0),
            "steps": on_case.get("steps", 0),
        }
        perf_change = {
            "duration_change_ms": perf_after["duration_ms"] - perf_before["duration_ms"],
            "steps_change": perf_after["steps"] - perf_before["steps"],
        }

        if assertion_changes or score_changes or perf_change.get("duration_change_ms", 0) != 0 or perf_change.get("steps_change", 0) != 0:
            per_case_diffs.append({
                "case_id": cid,
                "assertion_changes": assertion_changes,
                "score_changes": score_changes,
                "performance_change": perf_change,
            })

    # 结论
    conclusion = _generate_conclusion(diffs, flag_def)

    return {
        "flag_name": flag_name,
        "flag_description": flag_def.get("description", ""),
        "off_summary": off_summary,
        "on_summary": on_summary,
        "diffs": diffs,
        "per_case_diffs": per_case_diffs,
        "conclusion": conclusion,
    }


# ---------------------------------------------------------------------------
# 内部辅助函数
# ---------------------------------------------------------------------------

def _compute_diffs(
    off_summary: dict,
    on_summary: dict,
) -> list[dict]:
    """计算两个结果的逐维度 diff。"""
    diffs: list[dict] = []

    # 断言通过率
    off_rate = off_summary.get("assertion_pass_rate", 0)
    on_rate = on_summary.get("assertion_pass_rate", 0)
    rate_change = round(on_rate - off_rate, 4)
    diffs.append(diff_dimension(
        off_rate, on_rate,
        dimension_name="assertion_pass_rate",
    ))

    # 用例通过数
    off_passed = off_summary.get("passed_cases", 0)
    on_passed = on_summary.get("passed_cases", 0)
    diffs.append(diff_dimension(
        off_passed, on_passed,
        dimension_name="passed_cases",
        threshold_better=1, threshold_worse=-1,
    ))

    # 平均耗时
    off_dur = off_summary.get("avg_duration_ms", 0)
    on_dur = on_summary.get("avg_duration_ms", 0)
    dur_change = on_dur - off_dur
    if dur_change > 0 and off_dur > 0 and (dur_change / off_dur) > 0.2:
        dur_dir = "worse"
    elif dur_change < 0:
        dur_dir = "better"
    else:
        dur_dir = "neutral"
    diffs.append({
        "dimension": "avg_duration_ms",
        "off_value": off_dur,
        "on_value": on_dur,
        "change": dur_change,
        "direction": dur_dir,
        "significant": abs(dur_change) > 500,
    })

    # 平均步数
    off_steps = off_summary.get("avg_steps", 0)
    on_steps = on_summary.get("avg_steps", 0)
    steps_change = on_steps - off_steps
    diffs.append(diff_dimension(
        off_steps, on_steps,
        dimension_name="avg_steps",
        threshold_better=-0.5, threshold_worse=0.5,
    ))

    return diffs


def diff_dimension(
    off_value: float | int,
    on_value: float | int,
    dimension_name: str = "",
    threshold_better: float = 0.5,
    threshold_worse: float = -0.5,
) -> dict:
    """单维度 diff 判断。

    返回: {dimension, off_value, on_value, change, direction, significant}
    """
    change = round(float(on_value) - float(off_value), 4)
    significant = False

    if isinstance(off_value, float) and off_value <= 1.0 and on_value <= 1.0:
        # 比率值
        if change >= 0.05:
            direction = "better"
            significant = True
        elif change <= -0.05:
            direction = "worse"
            significant = True
        else:
            direction = "neutral"
    else:
        # 绝对值
        if change >= threshold_better:
            direction = "better"
            significant = True
        elif change <= threshold_worse:
            direction = "worse"
            significant = True
        else:
            direction = "neutral"

    return {
        "dimension": dimension_name,
        "off_value": off_value,
        "on_value": on_value,
        "change": change,
        "direction": direction,
        "significant": significant,
    }


def _diff_assertions(
    off_results: list[dict],
    on_results: list[dict],
) -> list[dict]:
    """对比两组的断言结果变化。"""
    off_map = {r.get("assertion_id"): r for r in off_results}
    on_map = {r.get("assertion_id"): r for r in on_results}
    all_ids = set(list(off_map.keys()) + list(on_map.keys()))

    changes: list[dict] = []
    for aid in sorted(all_ids):
        off_r = off_map.get(aid, {})
        on_r = on_map.get(aid, {})
        off_pass = off_r.get("pass_", True)
        on_pass = on_r.get("pass_", True)

        if off_pass and not on_pass:
            changes.append({"assertion_id": aid, "change": "PASS_TO_FAIL"})
        elif not off_pass and on_pass:
            changes.append({"assertion_id": aid, "change": "FAIL_TO_PASS"})

    return changes


def _diff_scores(
    off_scores: dict | None,
    on_scores: dict | None,
) -> dict | None:
    """对比两组的评分变化。"""
    if not off_scores and not on_scores:
        return None

    off_scores = off_scores or {}
    on_scores = on_scores or {}
    all_dims = set(list(off_scores.keys()) + list(on_scores.keys()))

    changes = {}
    for dim in all_dims:
        off_val = off_scores.get(dim, {})
        on_val = on_scores.get(dim, {})
        if isinstance(off_val, dict) and isinstance(on_val, dict):
            off_mean = off_val.get("mean", 0)
            on_mean = on_val.get("mean", 0)
        elif isinstance(off_val, (int, float)) and isinstance(on_val, (int, float)):
            off_mean = off_val
            on_mean = on_val
        else:
            continue
        changes[dim] = round(float(on_mean) - float(off_mean), 2)

    return changes if changes else None


def _generate_conclusion(diffs: list[dict], flag_def: dict) -> str:
    """根据 diff 数据生成人类可读的结论建议。"""
    significant = [d for d in diffs if d.get("significant")]
    worse = [d for d in significant if d.get("direction") == "worse"]
    better = [d for d in significant if d.get("direction") == "better"]

    parts: list[str] = []
    if not significant:
        parts.append(
            f"Flag '{flag_def.get('name', '')}' 开启后未检测到显著变化，"
            f"可能安全发布。"
        )
    else:
        if worse:
            parts.append(
                f"检测到 {len(worse)} 个维度退化: "
                + ", ".join(f"'{d['dimension']}' ({d['change']:+.2f})" for d in worse)
                + "。建议进一步排查后再发布。"
            )
        if better:
            parts.append(
                f"检测到 {len(better)} 个维度改善: "
                + ", ".join(f"'{d['dimension']}' ({d['change']:+.2f})" for d in better)
                + "。"
            )

    return " ".join(parts) if parts else "对比完成，建议人工审查结果。"


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="agent-verify Skill — Feature Flag A/B 对比",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n"
               "  python scripts/feature_flag.py --flag NEW_FEATURE --suite suites/suites.yaml --config config.yaml\n"
               "  python scripts/feature_flag.py --flag NEW_FEATURE --suite suites/suites.yaml --config config.yaml --baseline baseline-001\n"
               "  python scripts/feature_flag.py --flag NEW_FEATURE --suite suites/suites.yaml --config config.yaml --judge\n",
    )
    parser.add_argument("--flag", required=True, help="Feature Flag 名称")
    parser.add_argument("--suite", required=True, help="测试套件 YAML 文件路径")
    parser.add_argument("--config", required=True, help="config.yaml 文件路径")
    parser.add_argument("--baseline", help="基线名称（用于替代 Flag=OFF 运行）")
    parser.add_argument("--judge", action="store_true", help="启用 LLM 裁判")
    parser.add_argument("--output", metavar="FILE", help="输出 JSON 结果到文件")

    args = parser.parse_args()

    if not os.path.exists(args.suite):
        print(f"错误: 套件文件不存在: {args.suite}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.config):
        print(f"错误: 配置文件不存在: {args.config}", file=sys.stderr)
        sys.exit(1)

    try:
        comparison = run_flag_comparison(
            flag_name=args.flag,
            suite_file=args.suite,
            config_file=args.config,
            baseline_name=args.baseline,
            enable_judge=args.judge,
        )
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        from common import save_json
        save_json(comparison, args.output)
        print(f"对比结果已保存: {args.output}")

    # 输出报告
    print(generate_comparison_report(comparison, "markdown"))
