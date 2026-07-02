#!/usr/bin/env python3
"""agent-verify Skill — 断言引擎（核心）。

对应命令: /agent-verify:assert（断言执行部分）

MVP 实现 3 种断言类型: tool_call, tool_param, output_match。
V1.0 类型标注 TODO: path_sequence, timing, output_schema, custom_script。
"""

import json
import os
import re
import subprocess
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (
    load_yaml_config, parse_trace_output, validate_against_schema,
    TraceEvent, TRACE_EVENT_TYPES,
)


# ---------------------------------------------------------------------------
# 数据模型
# ---------------------------------------------------------------------------

class AssertionResult:
    """单条断言的结果。"""
    __slots__ = (
        "assertion_id", "assertion_name", "assertion_type",
        "pass_", "reason", "details", "severity",
    )

    def __init__(
        self,
        assertion_id: str,
        assertion_name: str,
        assertion_type: str,
        pass_: bool,
        reason: str | None = None,
        details: dict | None = None,
        severity: str = "error",
    ):
        self.assertion_id = assertion_id
        self.assertion_name = assertion_name
        self.assertion_type = assertion_type
        self.pass_ = pass_
        self.reason = reason
        self.details = details or {}
        self.severity = severity

    def to_dict(self) -> dict:
        return {s: getattr(self, s, None) for s in self.__slots__}


# ---------------------------------------------------------------------------
# 导出函数
# ---------------------------------------------------------------------------

def load_assertions(assertions_file: str) -> list[dict]:
    """加载 assertions.yaml 并返回断言定义列表。

    仅返回 enabled=true 的断言。
    验证每条断言的 target 和 condition 字段完整性。
    """
    data = load_yaml_config(assertions_file)

    if "assertions" not in data:
        raise ValueError(f"断言文件缺少 'assertions' 根键: {assertions_file}")

    raw_list = data["assertions"]
    if not isinstance(raw_list, list):
        raise ValueError(
            f"'assertions' 必须为列表，实际类型: {type(raw_list).__name__}"
        )

    validated: list[dict] = []
    for idx, assertion in enumerate(raw_list):
        if not isinstance(assertion, dict):
            raise ValueError(f"第 {idx} 条断言不是 dict 类型")
        if not assertion.get("enabled", True):
            continue
        _validate_assertion(assertion, idx)
        validated.append(assertion)

    return validated


def _validate_assertion(assertion: dict, idx: int) -> None:
    """验证单条断言定义。"""
    if "id" not in assertion:
        raise ValueError(f"第 {idx} 条断言缺少 'id' 字段")
    if "type" not in assertion:
        raise ValueError(f"断言 '{assertion['id']}' 缺少 'type' 字段")
    if "target" not in assertion:
        raise ValueError(f"断言 '{assertion['id']}' 缺少 'target' 字段")
    if "condition" not in assertion:
        raise ValueError(f"断言 '{assertion['id']}' 缺少 'condition' 字段")

    atype = assertion["type"]
    if atype not in CHECKER_MAP:
        raise ValueError(f"断言 '{assertion['id']}' 类型 '{atype}' 未知。支持的类型: {', '.join(CHECKER_MAP)}")


def check_assertions(
    trace: list,
    assertions: list[dict],
    case_level_overrides: dict | None = None,
) -> list[AssertionResult]:
    """对所有断言执行检查。

    Args:
        trace: list[TraceEvent]
        assertions: load_assertions() 返回的列表
        case_level_overrides: 用例级断言启用/禁用覆盖
            {"assertion_id": True|False}

    Returns:
        list[AssertionResult]
    """
    if case_level_overrides is None:
        case_level_overrides = {}

    results: list[AssertionResult] = []

    for assertion in assertions:
        aid = assertion["id"]

        # 检查用例级覆盖
        if aid in case_level_overrides:
            if not case_level_overrides[aid]:
                continue  # 被禁用

        try:
            result = check_single_assertion(trace, assertion)
        except Exception as e:
            result = AssertionResult(
                assertion_id=aid,
                assertion_name=assertion.get("name", aid),
                assertion_type=assertion["type"],
                pass_=False,
                reason=f"断言引擎异常: {e}",
                severity=assertion.get("severity", "error"),
            )

        results.append(result)

    return results


def check_single_assertion(
    trace: list,
    assertion: dict,
) -> AssertionResult:
    """对单条断言执行检查。"""
    atype = assertion["type"]
    target = assertion.get("target", {})
    condition = assertion.get("condition", {})
    severity = assertion.get("severity", "error")

    checker_class = CHECKER_MAP.get(atype)
    if checker_class is None:
        return AssertionResult(
            assertion_id=assertion["id"],
            assertion_name=assertion.get("name", assertion["id"]),
            assertion_type=atype,
            pass_=False,
            reason=f"未实现的断言类型: '{atype}' (V1.0 启用)",
            severity="error",
        )

    checker = checker_class()
    try:
        pass_, reason, details = checker.check(trace, target, condition)
    except Exception as e:
        return AssertionResult(
            assertion_id=assertion["id"],
            assertion_name=assertion.get("name", assertion["id"]),
            assertion_type=atype,
            pass_=False,
            reason=f"检查异常: {e}",
            severity="error",
        )

    return AssertionResult(
        assertion_id=assertion["id"],
        assertion_name=assertion.get("name", assertion["id"]),
        assertion_type=atype,
        pass_=pass_,
        reason=reason,
        details=details,
        severity=severity,
    )


# ---------------------------------------------------------------------------
# Checker 类
# ---------------------------------------------------------------------------

class ToolCallChecker:
    """检查 tool_call 事件。

    condition: min_count | max_count | exactly
    target: {"tool_name": "bash"}
    """

    def check(self, trace: list, target: dict, condition: dict) -> tuple[bool, str | None, dict]:
        tool_name = target.get("tool_name")
        if not tool_name:
            return False, "target 缺少 'tool_name'", {}

        # 统计匹配的 tool_call 事件
        count = sum(
            1 for e in trace
            if e.type == "tool_call" and e.tool_name == tool_name
        )

        details = {
            "tool_name": tool_name,
            "actual_count": count,
            "total_tool_calls": sum(1 for e in trace if e.type == "tool_call"),
        }

        # 检查各种条件
        if "exactly" in condition:
            expected = int(condition["exactly"])
            details["expected_exactly"] = expected
            if count != expected:
                return False, f"期望调用 {expected} 次，实际 {count} 次", details

        if "min_count" in condition:
            expected = int(condition["min_count"])
            details["min_count"] = expected
            if count < expected:
                return False, f"实际调用 {count} 次，低于最小值 {expected} 次", details

        if "max_count" in condition:
            expected = int(condition["max_count"])
            details["max_count"] = expected
            if count > expected:
                return False, f"实际调用 {count} 次，超过最大值 {expected} 次", details

        return True, None, details


class ToolParamChecker:
    """检查 tool_call 事件的 input 参数。

    condition: min_length | max_length | not_null | not_whitespace_only
              | pattern | allowed_values | forbidden_values
    target: {"tool_name": "bash", "param": "command"}
    """

    def check(self, trace: list, target: dict, condition: dict) -> tuple[bool, str | None, dict]:
        tool_name = target.get("tool_name")
        param = target.get("param")
        if not tool_name:
            return False, "target 缺少 'tool_name'", {}
        if not param:
            return False, "target 缺少 'param'", {}

        # 查找指定工具的调用
        relevant_events = [
            e for e in trace
            if e.type == "tool_call" and e.tool_name == tool_name
        ]

        if not relevant_events:
            return False, f"未找到对 '{tool_name}' 的调用", {
                "tool_name": tool_name, "param": param,
            }

        details = {"tool_name": tool_name, "param": param, "events_found": len(relevant_events)}
        all_pass = True
        reasons: list[str] = []

        for event in relevant_events:
            actual_input = event.input
            if isinstance(actual_input, str):
                try:
                    actual_input = json.loads(actual_input)
                except (json.JSONDecodeError, TypeError):
                    pass

            param_value = None
            if isinstance(actual_input, dict):
                param_value = actual_input.get(param)
            elif isinstance(actual_input, str):
                param_value = actual_input

            details.setdefault("param_values", [])
            details["param_values"].append(param_value)

            if param_value is None and "not_null" in condition:
                if condition["not_null"]:
                    all_pass = False
                    reasons.append(f"参数 '{param}' 在事件 seq={event.seq} 中为 null")

            if isinstance(param_value, str) and "not_whitespace_only" in condition:
                if condition["not_whitespace_only"] and param_value.strip() == "":
                    all_pass = False
                    reasons.append(f"参数 '{param}' 在事件 seq={event.seq} 中仅含空白字符")

            if isinstance(param_value, (str, list)):
                length = len(param_value)
                details.setdefault("lengths", [])
                details["lengths"].append(length)

                if "min_length" in condition:
                    expected = int(condition["min_length"])
                    if length < expected:
                        all_pass = False
                        reasons.append(f"参数 '{param}' 在事件 seq={event.seq} 中长度 {length} 低于最小值 {expected}")

                if "max_length" in condition:
                    expected = int(condition["max_length"])
                    if length > expected:
                        all_pass = False
                        reasons.append(f"参数 '{param}' 在事件 seq={event.seq} 中长度 {length} 超过最大值 {expected}")

            if isinstance(param_value, str) and "pattern" in condition:
                try:
                    if not re.search(condition["pattern"], param_value):
                        all_pass = False
                        reasons.append(f"参数 '{param}' 在事件 seq={event.seq} 中不匹配模式 '{condition['pattern']}'")
                except re.error as e:
                    all_pass = False
                    reasons.append(f"正则 '{condition['pattern']}' 错误: {e}")

            if isinstance(param_value, str) and "allowed_values" in condition:
                allowed = condition["allowed_values"]
                if isinstance(allowed, list) and param_value not in allowed:
                    all_pass = False
                    reasons.append(f"参数 '{param}' 值 '{param_value}' 不在允许值列表 {allowed} 中")

            if isinstance(param_value, str) and "forbidden_values" in condition:
                forbidden = condition["forbidden_values"]
                if isinstance(forbidden, list) and param_value in forbidden:
                    all_pass = False
                    reasons.append(f"参数 '{param}' 值 '{param_value}' 在禁止值列表中")

        if not all_pass:
            return False, "; ".join(reasons), details

        return True, None, details


class OutputMatchChecker:
    """对 final_output 执行正则匹配。

    condition: pattern | min_matches | case_sensitive
    target: 可选，当前仅使用单个 final_output
    """

    def check(self, trace: list, target: dict, condition: dict) -> tuple[bool, str | None, dict]:
        # 获取 final_output
        final_output = ""
        for e in trace:
            if e.type == "run_end" and e.final_output:
                final_output = e.final_output
                break
        # 尝试从 trace 最后几个事件中获取 final_output
        if not final_output:
            for e in reversed(trace):
                if e.final_output:
                    final_output = e.final_output
                    break

        pattern = condition.get("pattern", "")
        if not pattern:
            return False, "condition 缺少 'pattern'", {}

        flags = 0
        if not condition.get("case_sensitive", True):
            flags = re.IGNORECASE

        try:
            matches = list(re.finditer(pattern, final_output, flags))
        except re.error as e:
            return False, f"正则错误: {e}", {"pattern": pattern}

        match_count = len(matches)
        min_matches = int(condition.get("min_matches", 1))

        details = {
            "pattern": pattern,
            "match_count": match_count,
            "min_matches": min_matches,
            "case_sensitive": condition.get("case_sensitive", True),
            "output_length": len(final_output),
        }

        if match_count >= min_matches:
            return True, None, details
        else:
            return False, f"匹配次数 {match_count} 低于最小值 {min_matches}", details


# ---------------------------------------------------------------------------
# V1.0 Checker 存根（标注 TODO）
# ---------------------------------------------------------------------------

class PathSequenceChecker:
    """检查 llm_response 事件的 step 序列。
    TODO(V1.0): 实现路径顺序检查。
    """
    def check(self, trace: list, target: dict, condition: dict) -> tuple[bool, str | None, dict]:
        return False, "path_sequence 检查器 (V1.0 启用)", {}


class TimingChecker:
    """检查步骤耗时。
    TODO(V1.0): 实现计时检查。
    """
    def check(self, trace: list, target: dict, condition: dict) -> tuple[bool, str | None, dict]:
        return False, "timing 检查器 (V1.0 启用)", {}


class OutputSchemaChecker:
    """对 final_output 执行 JSON Schema 验证。
    TODO(V1.0): 实现 JSON Schema 验证。
    """
    def check(self, trace: list, target: dict, condition: dict) -> tuple[bool, str | None, dict]:
        return False, "output_schema 检查器 (V1.0 启用)", {}


class CustomScriptChecker:
    """调用外部脚本执行自定义检查。
    TODO(V1.0): 完善子进程调用。
    """
    def check(self, trace: list, target: dict, condition: dict) -> tuple[bool, str | None, dict]:
        script_path = target.get("script")
        if not script_path:
            return False, "target 缺少 'script' (自定义脚本路径)", {}

        try:
            result = subprocess.run(
                [sys.executable, script_path],
                input=json.dumps({"trace": [e.to_dict() for e in trace]}),
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode != 0:
                return False, f"自定义脚本退出码 {result.returncode}: {result.stderr.strip()}", {}
            output = json.loads(result.stdout)
            return output.get("pass", False), output.get("reason"), output.get("details", {})
        except subprocess.TimeoutExpired:
            return False, f"自定义脚本超时: {script_path}", {}
        except (json.JSONDecodeError, subprocess.SubprocessError) as e:
            return False, f"自定义脚本执行错误: {e}", {}


# ---------------------------------------------------------------------------
# Checker 注册表
# ---------------------------------------------------------------------------

CHECKER_MAP: dict[str, type] = {
    "tool_call": ToolCallChecker,
    "tool_param": ToolParamChecker,
    "output_match": OutputMatchChecker,
    "path_sequence": PathSequenceChecker,
    "timing": TimingChecker,
    "output_schema": OutputSchemaChecker,
    "custom_script": CustomScriptChecker,
}


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def _cli_check(args: Any) -> None:
    """--check 模式: 加载 trace + assertions 并执行断言检查。"""
    trace_file = args.trace
    assertions_file = args.assertions
    output_file = args.output

    # 加载 trace
    if not os.path.exists(trace_file):
        print(json.dumps({"error": f"Trace 文件不存在: {trace_file}"}), file=sys.stderr)
        sys.exit(1)

    from common import load_jsonl
    raw_records = load_jsonl(trace_file)
    # 从 jsonl dict 转 TraceEvent
    trace = [TraceEvent(**r) for r in raw_records]

    # 加载断言
    try:
        assertions = load_assertions(assertions_file)
    except (FileNotFoundError, ValueError) as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

    # 执行检查
    results = check_assertions(trace, assertions)

    output = {
        "total": len(results),
        "passed": sum(1 for r in results if r.pass_),
        "failed": sum(1 for r in results if not r.pass_),
        "results": [r.to_dict() for r in results],
    }

    output_json = json.dumps(output, ensure_ascii=False, indent=2)
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output_json)
            f.write("\n")
    else:
        print(output_json)


# ---------------------------------------------------------------------------
# --list / --remove / --run CLI 辅助
# ---------------------------------------------------------------------------

def _cli_list(args: Any) -> None:
    """--list 模式: 列出 assertions.yaml 中的所有断言。"""
    assertions_file = args.assertions
    if not assertions_file or not os.path.exists(assertions_file):
        print(json.dumps({"error": f"断言文件不存在: {assertions_file}"}), file=sys.stderr)
        sys.exit(1)

    from common import load_yaml_config
    data = load_yaml_config(assertions_file)
    raw_list = data.get("assertions", [])

    rows = []
    for a in raw_list:
        rows.append({
            "id": a.get("id", "?"),
            "name": a.get("name", ""),
            "type": a.get("type", "?"),
            "enabled": a.get("enabled", True),
            "target": str(a.get("target", {})),
        })

    print(json.dumps({"count": len(rows), "assertions": rows}, ensure_ascii=False, indent=2))


def _cli_remove(args: Any) -> None:
    """--remove 模式: 按 id 删除断言。"""
    assertions_file = args.assertions
    remove_id = args.remove
    if not assertions_file or not os.path.exists(assertions_file):
        print(json.dumps({"error": f"断言文件不存在: {assertions_file}"}), file=sys.stderr)
        sys.exit(1)

    from common import load_yaml_config
    data = load_yaml_config(assertions_file)
    raw_list = data.get("assertions", [])

    new_list = [a for a in raw_list if a.get("id") != remove_id]
    if len(new_list) == len(raw_list):
        print(json.dumps({"error": f"未找到 id 为 '{remove_id}' 的断言"}), file=sys.stderr)
        sys.exit(1)

    data["assertions"] = new_list
    import yaml
    with open(assertions_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(json.dumps({"removed": remove_id, "remaining": len(new_list)}, ensure_ascii=False, indent=2))


def _cli_run_single(args: Any) -> None:
    """--run 模式: 运行单个断言。"""
    trace_file = args.trace
    assertions_file = args.assertions
    run_id = args.run

    if not trace_file or not os.path.exists(trace_file):
        print(json.dumps({"error": f"Trace 文件不存在: {trace_file}"}), file=sys.stderr)
        sys.exit(1)
    if not assertions_file or not os.path.exists(assertions_file):
        print(json.dumps({"error": f"断言文件不存在: {assertions_file}"}), file=sys.stderr)
        sys.exit(1)

    from common import load_jsonl
    raw_records = load_jsonl(trace_file)
    trace = [TraceEvent(**r) for r in raw_records]

    try:
        assertions = load_assertions(assertions_file)
    except (FileNotFoundError, ValueError) as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

    # 按 id 筛选
    target = [a for a in assertions if a.get("id") == run_id]
    if not target:
        print(json.dumps({"error": f"未找到 id 为 '{run_id}' 的已启用断言"}), file=sys.stderr)
        sys.exit(1)

    result = check_single_assertion(trace, target[0])
    output = {"result": result.to_dict()}
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="agent-verify Skill — 断言引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n"
               "  python scripts/assertion_engine.py --check --trace trace.jsonl --assertions assertions.yaml\n"
               "  python scripts/assertion_engine.py --list --assertions assertions.yaml\n"
               "  python scripts/assertion_engine.py --remove <id> --assertions assertions.yaml\n"
               "  python scripts/assertion_engine.py --run <id> --trace trace.jsonl --assertions assertions.yaml\n",
    )
    parser.add_argument(
        "--check", action="store_true",
        help="执行断言检查模式",
    )
    parser.add_argument("--list", action="store_true",
                        help="列出当前 assertions.yaml 中的所有断言")
    parser.add_argument("--remove", metavar="ID",
                        help="按 id 删除断言")
    parser.add_argument("--run", metavar="ID",
                        help="运行单个断言（需 --trace 和 --assertions）")
    parser.add_argument("--trace", help="trace.jsonl 文件路径")
    parser.add_argument("--assertions", help="assertions.yaml 文件路径")
    parser.add_argument("--output", help="输出 JSON 文件路径（可选）")

    args = parser.parse_args()

    if args.check:
        if not args.trace or not args.assertions:
            parser.error("--check 模式需要 --trace 和 --assertions 参数")
        _cli_check(args)
    elif args.list:
        if not args.assertions:
            parser.error("--list 模式需要 --assertions 参数")
        _cli_list(args)
    elif args.remove:
        if not args.assertions:
            parser.error("--remove 模式需要 --assertions 参数")
        _cli_remove(args)
    elif args.run:
        if not args.trace or not args.assertions:
            parser.error("--run 模式需要 --trace 和 --assertions 参数")
        _cli_run_single(args)
    else:
        parser.print_help()
