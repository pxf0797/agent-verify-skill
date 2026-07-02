#!/usr/bin/env python3
"""agent-verify Skill — 回归测试编排器。

对应命令: /agent-verify:regression, /agent-verify:baseline, /agent-verify:suite

功能:
    - 加载测试套件、遍历用例
    - 依次调用 Claude CLI 执行 Agent
    - 结构化日志解析
    - 断言检查
    - (可选) LLM 裁判评分
    - 基线管理（save/load/list/compare）
"""

import json
import os
import sys
import time
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (
    load_yaml_config, save_json, load_json, load_jsonl,
    run_agent_cli, parse_trace_output, build_flag_env,
    compute_config_hash, TraceEvent,
    PROJECT_DIR_NAME, SUITE_DIR, BASELINE_DIR, REPORT_DIR,
)
from assertion_engine import load_assertions, check_assertions
from report_generator import generate_regression_report, write_report


# ---------------------------------------------------------------------------
# 数据模型 (作为普通的 dict 使用，简化序列化)
# ---------------------------------------------------------------------------

class CaseResult:
    """单条测试用例的结果。"""
    __slots__ = (
        "case_id", "case_name", "raw_output", "trace",
        "assertion_results", "judge_scores", "duration_ms",
        "steps", "error",
    )

    def __init__(self, **kwargs):
        self.case_id: str = kwargs.get("case_id", "")
        self.case_name: str = kwargs.get("case_name", "")
        self.raw_output: str = kwargs.get("raw_output", "")
        self.trace: list = kwargs.get("trace", [])
        self.assertion_results: list = kwargs.get("assertion_results", [])
        self.judge_scores: dict | None = kwargs.get("judge_scores")
        self.duration_ms: int = kwargs.get("duration_ms", 0)
        self.steps: int = kwargs.get("steps", 0)
        self.error: str | None = kwargs.get("error")

    def to_dict(self) -> dict:
        d = {s: getattr(self, s, None) for s in self.__slots__}
        # 序列化 TraceEvent
        if self.trace and isinstance(self.trace[0], TraceEvent):
            d["trace"] = [e.to_dict() for e in self.trace]
        if self.assertion_results and hasattr(self.assertion_results[0], "to_dict"):
            d["assertion_results"] = [r.to_dict() for r in self.assertion_results]
        return d


# ---------------------------------------------------------------------------
# 导出函数
# ---------------------------------------------------------------------------

def load_suite(suite_file: str) -> dict:
    """加载 suite YAML 文件。验证必需字段。

    解析 defaults、test_cases、groups。
    应用优先级: 用例级 > defaults > 全局 config.yaml
    """
    data = load_yaml_config(suite_file)

    if "test_cases" not in data:
        raise ValueError(f"套件文件缺少 'test_cases' 字段: {suite_file}")
    if not isinstance(data["test_cases"], list):
        raise ValueError("'test_cases' 必须为列表")

    # 验证每条用例
    for idx, tc in enumerate(data["test_cases"]):
        if not isinstance(tc, dict):
            raise ValueError(f"第 {idx} 条 test_case 不是 dict 类型")
        if "id" not in tc:
            raise ValueError(f"第 {idx} 条 test_case 缺少 'id' 字段")
        if "input" not in tc and "name" not in tc:
            raise ValueError(f"用例 '{tc.get('id', idx)}' 缺少 'input' 字段")

    # 验证 groups（若存在）
    groups = data.get("groups", {})
    if groups:
        all_ids = {tc["id"] for tc in data["test_cases"]}
        for group_name, case_ids in groups.items():
            if not isinstance(case_ids, list):
                raise ValueError(f"分组 '{group_name}' 必须为列表")
            for cid in case_ids:
                if cid not in all_ids:
                    raise ValueError(
                        f"分组 '{group_name}' 引用了不存在的用例 ID: '{cid}'"
                    )

    return data


def resolve_test_cases(
    suite: dict,
    scope: str = "all",
) -> list[dict]:
    """根据 scope 解析要运行的测试用例列表。

    Args:
        suite: load_suite() 返回的数据
        scope: "all" | "smoke" | "full" | 自定义分组名 | 用例 ID

    Returns:
        用例 dict 列表
    """
    test_cases = suite.get("test_cases", [])
    groups = suite.get("groups", {})

    if scope == "all":
        return test_cases

    if scope == "smoke":
        smoke_ids = groups.get("smoke", [])
        return [tc for tc in test_cases if tc["id"] in smoke_ids]

    if scope == "full":
        return test_cases

    # 自定义分组名
    if scope in groups:
        group_ids = groups[scope]
        return [tc for tc in test_cases if tc["id"] in group_ids]

    # 单个用例 ID
    for tc in test_cases:
        if tc["id"] == scope:
            return [tc]

    raise ValueError(
        f"未识别的 scope: '{scope}'。"
        f"可用分组: {list(groups.keys()) + ['all', 'smoke']}。"
        f"可用用例: {[tc['id'] for tc in test_cases[:10]]}"
    )


def run_agent_with_case(
    test_case: dict,
    defaults: dict,
    config: dict,
    flag_overrides: dict | None = None,
) -> tuple[str, list]:
    """对单个测试用例执行 Agent。

    Returns:
        (raw_output, trace_events)
    """
    input_text = test_case.get("input", "")
    if not input_text:
        raise ValueError(f"用例 '{test_case.get('id', '?')}' 没有 input 字段")

    # 构建 agent_command — 用例级 > defaults
    agent_command = (
        test_case.get("agent_command")
        or defaults.get("agent_command")
        or config.get("execution", {}).get("agent_command", "claude --print")
    )

    timeout = (
        test_case.get("timeout")
        or defaults.get("timeout")
        or config.get("execution", {}).get("timeout", 120)
    )

    # 构建环境变量
    env_extra = None
    if flag_overrides:
        env_extra = flag_overrides

    try:
        result = run_agent_cli(
            input_text=input_text,
            agent_command=agent_command,
            timeout=int(timeout),
            env_extra=env_extra,
            inject_trace=True,
        )
    except (TimeoutError, RuntimeError) as e:
        # 超时或 CLI 不可用
        return "", []

    raw_output = result.stdout
    trace = parse_trace_output(raw_output, result.stderr)

    return raw_output, trace


def run_regression(
    suite_file: str,
    config_file: str,
    scope: str = "all",
    enable_judge: bool | None = None,
    output_format: str = "markdown",
    output_file: str | None = None,
    flag_overrides: dict | None = None,
) -> dict:
    """运行完整回归测试。

    Args:
        suite_file: 测试套件 YAML 文件路径
        config_file: config.yaml 文件路径
        scope: "all" | "smoke" | 自定义分组名
        enable_judge: 强制启用/禁用 LLM 裁判（None=使用 config）
        output_format: "markdown" | "json"
        output_file: 输出文件路径（可选）
        flag_overrides: Flag 注入（用于 A/B 对比）

    Returns:
        {
            "summary": { ... },
            "cases": [ ... ],
            "baseline_comparison": { ... } | None,
        }
    """
    # 加载配置
    config = load_yaml_config(config_file)

    # 确定是否启用 LLM 裁判
    if enable_judge is None:
        llm_judge_cfg = config.get("llm_judge", {})
        enable_judge = llm_judge_cfg.get("enabled", False)

    # 加载断言
    verify_dir = os.path.dirname(config_file)
    assertions_file = os.path.join(verify_dir, "assertions.yaml")
    try:
        assertions = load_assertions(assertions_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"警告: 断言文件加载失败: {e}", file=sys.stderr)
        assertions = []

    # 加载套件
    suite = load_suite(suite_file)
    defaults = suite.get("defaults", {})
    test_cases = resolve_test_cases(suite, scope)

    if not test_cases:
        raise ValueError(f"没有匹配 scope='{scope}' 的测试用例")

    case_results: list[dict] = []
    total_assertions = 0
    passed_assertions = 0
    total_duration = 0
    total_steps = 0
    failed_details: list[dict] = []

    print(f"执行中: {len(test_cases)} 个测试用例...", file=sys.stderr)

    for idx, tc in enumerate(test_cases, 1):
        case_id = tc["id"]
        case_name = tc.get("name", case_id)
        print(f"  [{idx}/{len(test_cases)}] {case_id}...", file=sys.stderr)

        start_time = time.time()

        try:
            raw_output, trace = run_agent_with_case(tc, defaults, config, flag_overrides)
            duration_ms = int((time.time() - start_time) * 1000)
            steps = len(trace)

            # 执行断言检查
            case_overrides = tc.get("assertion_overrides")
            ar = check_assertions(trace, assertions, case_overrides)

            # 统计
            for r in ar:
                total_assertions += 1
                if r.pass_:
                    passed_assertions += 1
                else:
                    failed_details.append({
                        "case_id": case_id,
                        "assertion_id": r.assertion_id,
                        "reason": r.reason or "未知原因",
                    })

            # LLM 裁判（V1.0 启用）
            judge_scores = None
            if enable_judge:
                try:
                    from llm_judge import score_with_haiku
                    judge_result = score_with_haiku(
                        task=input_text,
                        agent_output=raw_output,
                        quality_criteria={},
                        n_runs=1,
                    )
                    judge_scores = judge_result.to_dict()["scores"]
                except Exception as e:
                    print(f"    警告: LLM 裁判评分失败: {e}", file=sys.stderr)

            case_result = CaseResult(
                case_id=case_id,
                case_name=case_name,
                raw_output=raw_output,
                trace=trace,
                assertion_results=[r.to_dict() for r in ar],
                judge_scores=judge_scores,
                duration_ms=duration_ms,
                steps=steps,
            )
            case_results.append(case_result.to_dict())

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            case_result = CaseResult(
                case_id=case_id,
                case_name=case_name,
                error=str(e),
                duration_ms=duration_ms,
            )
            case_results.append(case_result.to_dict())

        total_duration += duration_ms
        total_steps += steps if "steps" in locals() else 0

    # 计算摘要
    n_cases = len(case_results)
    n_passed = sum(
        1 for c in case_results
        if c.get("error") is None and
        all(r.get("pass_") for r in c.get("assertion_results", []))
    )
    n_failed = n_cases - n_passed
    assertion_pass_rate = passed_assertions / total_assertions if total_assertions > 0 else 1.0

    summary = {
        "suite_name": os.path.basename(suite_file),
        "total_cases": n_cases,
        "passed_cases": n_passed,
        "failed_cases": n_failed,
        "assertion_pass_rate": round(assertion_pass_rate, 4),
        "avg_duration_ms": round(total_duration / n_cases) if n_cases > 0 else 0,
        "avg_steps": round(total_steps / n_cases, 1) if n_cases > 0 else 0,
        "failed_details": failed_details,
        "flags": flag_overrides or {},
    }

    # 聚合 LLM 评分
    judge_dimensions: dict[str, list[float]] = {}
    for c in case_results:
        js = c.get("judge_scores")
        if js:
            for dim, data in js.items():
                if dim not in judge_dimensions:
                    judge_dimensions[dim] = []
                if isinstance(data, dict) and "mean" in data:
                    judge_dimensions[dim].append(data["mean"])
                elif isinstance(data, (int, float)):
                    judge_dimensions[dim].append(data)

    if judge_dimensions:
        llm_scores = {}
        for dim, values in judge_dimensions.items():
            if values:
                mean = sum(values) / len(values)
                llm_scores[dim] = {"mean": round(mean, 2)}
        summary["llm_scores"] = llm_scores

    # 基线对比（可选）
    baseline_comparison = None
    baselines_dir = os.path.join(verify_dir, BASELINE_DIR)
    latest_baseline = _find_latest_baseline(baselines_dir)
    if latest_baseline:
        try:
            baseline_data = load_baseline(latest_baseline)
            baseline_comparison = _compare_with_baseline(summary, baseline_data)
        except Exception as e:
            print(f"警告: 基线对比失败: {e}", file=sys.stderr)

    result = {
        "summary": summary,
        "cases": case_results,
        "baseline_comparison": baseline_comparison,
    }

    # 保存结果到文件
    if output_file:
        save_json(result, output_file)

    # 输出报告
    if output_format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        report = generate_regression_report(result, "markdown")
        print(report)

    return result


def _compare_with_baseline(
    summary: dict,
    baseline: dict,
) -> dict:
    """将当前结果与基线对比。"""
    base_summary = baseline.get("summary", {})
    diffs = []

    # 断言通过率
    current_rate = summary.get("assertion_pass_rate", 0)
    base_rate = base_summary.get("assertion_pass_rate", 0)
    change = round(current_rate - base_rate, 4)
    if change > 0.05:
        direction = "better"
    elif change < -0.05:
        direction = "worse"
    else:
        direction = "neutral"
    diffs.append({
        "dimension": "assertion_pass_rate",
        "base_value": base_rate,
        "current_value": current_rate,
        "change": change,
        "direction": direction,
        "significant": abs(change) > 0.05,
    })

    # 平均耗时
    current_dur = summary.get("avg_duration_ms", 0)
    base_dur = base_summary.get("avg_duration_ms", 0)
    dur_change = current_dur - base_dur
    if dur_change > 0 and dur_change / max(base_dur, 1) > 0.2:
        dur_dir = "worse"
    elif dur_change < 0:
        dur_dir = "better"
    else:
        dur_dir = "neutral"
    diffs.append({
        "dimension": "avg_duration_ms",
        "base_value": base_dur,
        "current_value": current_dur,
        "change": dur_change,
        "direction": dur_dir,
        "significant": abs(dur_change) > 500,
    })

    return {"baseline_name": baseline.get("meta", {}).get("name", "latest"), "diffs": diffs}


# ---------------------------------------------------------------------------
# 基线管理
# ---------------------------------------------------------------------------

def save_baseline(
    name: str,
    regression_result: dict,
    baselines_dir: str,
    git_commit: str | None = None,
) -> str:
    """保存基线快照 JSON 文件。返回文件路径。"""
    os.makedirs(baselines_dir, exist_ok=True)

    import hashlib
    import datetime

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d-%H%M%S")
    filename = f"{name}-{timestamp}.json"
    filepath = os.path.join(baselines_dir, filename)

    meta = {
        "name": name,
        "created": now.isoformat(),
        "suite": regression_result.get("summary", {}).get("suite_name", ""),
        "config_hash": compute_config_hash(regression_result),
        "git_commit": git_commit or "",
        "pass_rate": regression_result.get("summary", {}).get("assertion_pass_rate", 0),
    }

    snapshot = {
        "meta": meta,
        "summary": regression_result.get("summary", {}),
        "cases": regression_result.get("cases", []),
        "flags": regression_result.get("summary", {}).get("flags", {}),
    }

    save_json(snapshot, filepath)
    return filepath


def load_baseline(baseline_file: str) -> dict:
    """加载基线快照文件。"""
    return load_json(baseline_file)


def list_baselines(baselines_dir: str) -> list[dict]:
    """列出所有基线（仅元信息）。"""
    if not os.path.isdir(baselines_dir):
        return []

    baselines: list[dict] = []
    for fname in sorted(os.listdir(baselines_dir), reverse=True):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(baselines_dir, fname)
        try:
            data = load_json(fpath)
            meta = data.get("meta", {})
            baselines.append({
                "name": meta.get("name", fname),
                "file": fname,
                "path": fpath,
                "created": meta.get("created", ""),
                "config_hash": meta.get("config_hash", ""),
                "pass_rate": meta.get("pass_rate", 0),
                "suite": meta.get("suite", ""),
            })
        except Exception:
            continue

    return baselines


def compare_baselines(
    baseline1_file: str,
    baseline2_file: str,
) -> dict:
    """对比两个基线。"""
    b1 = load_baseline(baseline1_file)
    b2 = load_baseline(baseline2_file)

    b1_meta = b1.get("meta", {})
    b2_meta = b2.get("meta", {})
    b1_summary = b1.get("summary", {})
    b2_summary = b2.get("summary", {})

    diffs = []

    # 断言通过率
    rate1 = b1_summary.get("assertion_pass_rate", 0)
    rate2 = b2_summary.get("assertion_pass_rate", 0)
    change = round(rate2 - rate1, 4)
    if change > 0.05:
        direction = "better"
    elif change < -0.05:
        direction = "worse"
    else:
        direction = "neutral"
    diffs.append({
        "dimension": "assertion_pass_rate",
        "off_value": rate1,
        "on_value": rate2,
        "change": change,
        "direction": direction,
        "significant": abs(change) > 0.05,
    })

    # 耗时
    dur1 = b1_summary.get("avg_duration_ms", 0)
    dur2 = b2_summary.get("avg_duration_ms", 0)
    d_change = dur2 - dur1
    if d_change > 0 and d_change / max(dur1, 1) > 0.2:
        d_dir = "worse"
    elif d_change < 0:
        d_dir = "better"
    else:
        d_dir = "neutral"
    diffs.append({
        "dimension": "avg_duration_ms",
        "off_value": dur1,
        "on_value": dur2,
        "change": d_change,
        "direction": d_dir,
        "significant": abs(d_change) > 500,
    })

    return {
        "baseline1_name": b1_meta.get("name", os.path.basename(baseline1_file)),
        "baseline2_name": b2_meta.get("name", os.path.basename(baseline2_file)),
        "baseline1_meta": b1_meta,
        "baseline2_meta": b2_meta,
        "diffs": diffs,
    }


def _find_latest_baseline(baselines_dir: str) -> str | None:
    """找到最新的基线文件路径。"""
    baselines = list_baselines(baselines_dir)
    if not baselines:
        return None
    return baselines[0]["path"]


# ---------------------------------------------------------------------------
# 增量运行辅助（V1.0 存根）
# ---------------------------------------------------------------------------

def select_changed_cases(suite: dict, git_diff_files: list[str]) -> list[dict]:
    """基于 git diff 选择相关测试用例。
    TODO(V1.0): 实现智能用例选择。
    """
    # V1.0: 简单回退到 smoke 分组或全量
    if "groups" in suite and "smoke" in suite["groups"]:
        return resolve_test_cases(suite, "smoke")
    return resolve_test_cases(suite, "all")


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="agent-verify Skill — 回归测试编排器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n"
               "  python scripts/regression_runner.py --suite suites/suites.yaml --config config.yaml\n"
               "  python scripts/regression_runner.py --suite suites/suites.yaml --config config.yaml --scope smoke\n"
               "  python scripts/regression_runner.py --baseline-save baseline-001 --config config.yaml --suite suites/suites.yaml\n"
               "  python scripts/regression_runner.py --baseline-list\n",
    )

    # 运行模式
    parser.add_argument("--suite", help="测试套件 YAML 文件路径")
    parser.add_argument("--config", help="config.yaml 文件路径")
    parser.add_argument("--scope", default="all", help="测试范围: all, smoke, 分组名, 用例 ID")
    parser.add_argument("--enable-judge", action="store_true", default=None,
                        help="启用 LLM 裁判（覆盖配置）")
    parser.add_argument("--disable-judge", action="store_false", dest="enable_judge",
                        help="禁用 LLM 裁判（覆盖配置）")
    parser.add_argument("--output", help="输出结果 JSON 文件路径")

    # 基线管理
    parser.add_argument("--baseline-save", metavar="NAME", help="保存基线")
    parser.add_argument("--baseline-load", metavar="FILE", help="加载基线")
    parser.add_argument("--baseline-list", action="store_true", help="列出所有基线")
    # --compare 是符合 SKILL.md 文档的标准名；--baseline-compare 作为 deprecated alias 保留
    parser.add_argument("--compare", action="store_true",
                        help="与最新基线对比")
    parser.add_argument("--baseline-compare", nargs=2, metavar=("FILE1", "FILE2"),
                        help="对比两个基线（deprecated: 使用 --compare filename1 filename2）")

    args = parser.parse_args()

    # 基线列表模式
    if args.baseline_list:
        if not args.config:
            parser.error("--baseline-list 需要 --config 参数")
        verify_dir = os.path.dirname(args.config)
        baselines_dir = os.path.join(verify_dir, BASELINE_DIR)
        baselines = list_baselines(baselines_dir)
        if not baselines:
            print("无已保存的基线。")
            sys.exit(0)
        print(f"{'名称':<24} {'创建时间':<24} {'通过率':<10} {'套件':<20}")
        print("-" * 80)
        for b in baselines:
            rate = f"{b['pass_rate']:.1%}" if b['pass_rate'] else "N/A"
            print(f"{b['name']:<24} {b['created'][:19]:<24} {rate:<10} {b['suite']:<20}")
        sys.exit(0)

    # --compare 模式：与最新基线对比
    if args.compare:
        if not args.suite or not args.config:
            parser.error("--compare 模式需要 --suite 和 --config 参数")
        result = run_regression(
            suite_file=args.suite,
            config_file=args.config,
            scope=args.scope,
            enable_judge=args.enable_judge,
            output_file=args.output,
        )
        compare_info = result.get("baseline_comparison")
        if compare_info:
            from report_generator import generate_baseline_comparison_report
            report = generate_baseline_comparison_report(compare_info, "markdown")
            print(report)
        else:
            print("未找到可对比的基线。先运行 --baseline-save 保存一个基线。", file=sys.stderr)
        sys.exit(0)

    # 基线对比模式
    if args.baseline_compare:
        comparison = compare_baselines(args.baseline_compare[0], args.baseline_compare[1])
        from report_generator import generate_baseline_comparison_report
        report = generate_baseline_comparison_report(comparison, "markdown")
        print(report)
        sys.exit(0)

    # 运行回归
    if not args.suite or not args.config:
        parser.error("需要 --suite 和 --config 参数来运行回归测试")

    result = run_regression(
        suite_file=args.suite,
        config_file=args.config,
        scope=args.scope,
        enable_judge=args.enable_judge,
        output_file=args.output,
    )

    # 保存基线（如果指定）
    if args.baseline_save:
        verify_dir = os.path.dirname(args.config)
        baselines_dir = os.path.join(verify_dir, BASELINE_DIR)
        path = save_baseline(args.baseline_save, result, baselines_dir)
        print(f"\n基线已保存: {path}", file=sys.stderr)
