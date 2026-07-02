#!/usr/bin/env python3
"""agent-verify Skill — 所有 T3 脚本的唯一内部依赖。

包含: 配置加载、JSON/YAML I/O、路径工具、Claude CLI 封装、
结构化日志解析、JSON Schema 验证、Feature Flag 环境变量、哈希工具。
"""

import json
import os
import re
import subprocess
import hashlib
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Constants — 约定字符串（与 T2/T4 对齐）
# ---------------------------------------------------------------------------

ASSERTION_TYPES = [
    "tool_call", "tool_param", "output_match", "path_sequence",
    "timing", "output_schema", "custom_script",
]

TOOL_CALL_CONDITIONS = ["min_count", "max_count", "exactly"]
TOOL_PARAM_CONDITIONS = [
    "min_length", "max_length", "not_null", "not_whitespace_only",
    "pattern", "allowed_values", "forbidden_values",
]
OUTPUT_MATCH_CONDITIONS = ["pattern", "min_matches", "case_sensitive", "match_behavior"]
PATH_SEQUENCE_CONDITIONS = ["order", "all_present"]  # order: "strict" | "relaxed"
TIMING_CONDITIONS = ["max_duration_ms", "min_duration_ms"]
OUTPUT_SCHEMA_CONDITIONS = ["schema"]

SEVERITY_LEVELS = ["error", "warning"]

PROJECT_DIR_NAME = "agent-verify"
SUITE_DIR = "suites"
BASELINE_DIR = "baselines"
REPORT_DIR = "reports"
CONFIG_FILENAME = "config.yaml"
ASSERTIONS_FILENAME = "assertions.yaml"

CONFIG_TOP_KEYS = [
    "version", "execution", "assertions", "llm_judge",
    "feature_flags", "baselines", "reports", "coverage",
]

FLAG_ENV_PREFIX = "AGENT_FLAG_"
TRACE_PREFIX = "[AGENT_VERIFY:TRACE]"
TRACE_EVENT_TYPES = [
    "run_start", "tool_call", "tool_result", "llm_response",
    "state_change", "error", "run_end",
]
AGENT_VERIFY_MODE = "AGENT_VERIFY_MODE"

# Template placeholders
PLACEHOLDER_TARGET_NAME = "{{TARGET_NAME}}"
PLACEHOLDER_CURRENT_DATE = "{{CURRENT_DATE}}"
PLACEHOLDER_SKILL_VERSION = "{{SKILL_VERSION}}"

SKILL_VERSION = "0.9.0"


# ---------------------------------------------------------------------------
# YAML / JSON I/O
# ---------------------------------------------------------------------------

def load_yaml_config(path: str) -> dict:
    """加载 YAML 配置文件，返回解析后的 dict。"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"配置文件不存在: {path}")
    try:
        import yaml
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            raise ValueError(f"YAML 文件根层级必须为 dict，实际类型: {type(data).__name__}")
        return data
    except yaml.YAMLError as e:
        raise ValueError(f"YAML 解析失败: {e}") from e


def save_yaml_config(data: dict, path: str) -> None:
    """保存 dict 为 YAML 文件。"""
    import yaml
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def load_json(path: str) -> dict | list:
    """加载 JSON 文件。"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"JSON 文件不存在: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 解析失败: {e}") from e


def save_json(data: dict | list, path: str, indent: int = 2) -> None:
    """保存 JSON 文件（UTF-8，compact=False）。"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
        f.flush()


def load_jsonl(path: str) -> list[dict]:
    """加载 JSONL 文件，返回 dict 列表。忽略空行。"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"JSONL 文件不存在: {path}")
    records: list[dict] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                continue
            try:
                records.append(json.loads(stripped))
            except json.JSONDecodeError as e:
                raise ValueError(f"JSONL 行解析失败: {e}") from e
    return records


def save_jsonl(records: list[dict], path: str) -> None:
    """保存 dict 列表为 JSONL 文件（每行一个 JSON 对象）。"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()


# ---------------------------------------------------------------------------
# 路径工具
# ---------------------------------------------------------------------------

def resolve_skill_root() -> str:
    """返回 agent-verify Skill 安装目录的绝对路径。

    查找逻辑: 从当前文件（common.py 所在目录）向上找到包含 SKILL.md 的目录。
    """
    current = Path(__file__).resolve().parent  # scripts/
    # 先检查 scripts/ 的父级
    parent = current.parent
    if (parent / "SKILL.md").exists():
        return str(parent)
    # 再逐级向上
    candidate = parent
    for _ in range(5):
        if (candidate / "SKILL.md").exists():
            return str(candidate)
        candidate = candidate.parent
    # fallback: 返回当前文件的父级（scripts/ 的父级）
    return str(parent)


def resolve_project_root() -> str | None:
    """返回用户项目的 agent-verify/ 目录的绝对路径。

    查找逻辑: 从 CWD 向上查找包含 config.yaml + assertions.yaml 的
    agent-verify/ 目录。若未找到返回 None。
    """
    cwd = Path.cwd().resolve()
    # 从 CWD 向上找
    for parent in [cwd] + list(cwd.parents):
        verify_dir = parent / "agent-verify"
        if not verify_dir.is_dir():
            continue
        config = verify_dir / "config.yaml"
        assertions = verify_dir / "assertions.yaml"
        if config.exists() and assertions.exists():
            return str(verify_dir)
    # 也直接检查 CWD 本身是否是 agent-verify
    if cwd.name == PROJECT_DIR_NAME:
        config = cwd / "config.yaml"
        assertions = cwd / "assertions.yaml"
        if config.exists() and assertions.exists():
            return str(cwd)
    return None


# ---------------------------------------------------------------------------
# Claude CLI 封装
# ---------------------------------------------------------------------------

def run_agent_cli(
    input_text: str,
    agent_command: str = "claude --print",
    timeout: int = 120,
    env_extra: dict | None = None,
    skill_name: str | None = None,
    inject_trace: bool = True,
) -> subprocess.CompletedProcess:
    """执行被验证的 Agent。

    Args:
        input_text: 用户输入（通过 stdin 传递）
        agent_command: 如 "claude --print" 或 "claude --skill search-agent --print"
        timeout: 超时秒数
        env_extra: 额外的环境变量（如 AGENT_FLAG_*）
        skill_name: 可选的 Skill 名称（若 agent_command 中未包含 --skill）
        inject_trace: 是否在 prompt 中注入结构化日志指令

    Returns:
        subprocess.CompletedProcess (包含 stdout, stderr, returncode)。
    """
    skill_path = resolve_skill_root()
    # 构建最终命令
    if skill_name and "--skill" not in agent_command:
        cmd = f"claude --skill {skill_name} --print"
    else:
        cmd = agent_command

    # 构建环境变量
    env = os.environ.copy()
    env[AGENT_VERIFY_MODE] = "true"
    if env_extra:
        env.update(env_extra)

    # 构建输入
    full_input = input_text
    if inject_trace:
        trace_injection = build_trace_injection_prompt()
        full_input = input_text + "\n\n" + trace_injection

    try:
        result = subprocess.run(
            cmd.split(),
            input=full_input,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
    except subprocess.TimeoutExpired:
        raise TimeoutError(f"Agent 执行超时 ({timeout}s): {input_text[:80]}...")
    except FileNotFoundError:
        raise RuntimeError(
            f"Claude CLI 未找到。请确保 'claude' 命令在 PATH 中可用。"
        )

    return result


def build_trace_injection_prompt() -> str:
    """生成结构化日志注入指令文本。

    返回一段追加到 Agent system prompt 末尾的指令字符串。
    格式与 parse_log 函数兼容。
    """
    return (
        f"\n\n[AGENT_VERIFY:TRACE] 请在本次回应的每一步关键操作（工具调用、LLM 响应、状态变更）"
        f"输出以 '{TRACE_PREFIX}' 为前缀的结构化日志行。"
        f"格式: {TRACE_PREFIX} {{\"seq\": 1, \"ts\": \"...\", \"type\": \"tool_call\", "
        f"\"tool_name\": \"...\"}}。支持的事件类型: {', '.join(TRACE_EVENT_TYPES)}。"
        f"请在每个事件的 JSON 对象前后各留一个换行。"
    )


# ---------------------------------------------------------------------------
# 结构化日志解析
# ---------------------------------------------------------------------------

class TraceEvent:
    """单个结构化日志事件的数据类。"""
    __slots__ = (
        "run_id", "seq", "ts", "type",
        "tool_name", "input", "output", "content",
        "step", "final_output", "total_steps", "total_duration_ms",
        "error_type", "message", "raw",
    )

    def __init__(self, **kwargs):
        self.run_id: str = kwargs.get("run_id", "")
        self.seq: int = int(kwargs.get("seq", 0))
        self.ts: str = kwargs.get("ts", "")
        self.type: str = kwargs.get("type", "")
        self.tool_name: str | None = kwargs.get("tool_name")
        self.input: dict | str | None = kwargs.get("input")
        self.output: dict | None = kwargs.get("output")
        self.content: str | None = kwargs.get("content")
        self.step: str | None = kwargs.get("step")
        self.final_output: str | None = kwargs.get("final_output")
        self.total_steps: int | None = kwargs.get("total_steps")
        self.total_duration_ms: int | None = kwargs.get("total_duration_ms")
        self.error_type: str | None = kwargs.get("error_type")
        self.message: str | None = kwargs.get("message")
        self.raw: dict | None = kwargs.get("raw")

    def to_dict(self) -> dict:
        return {s: getattr(self, s, None) for s in self.__slots__}


def parse_trace_output(raw_stdout: str, raw_stderr: str = "") -> list[TraceEvent]:
    """从 Agent 原始输出中解析结构化日志。

    识别 [AGENT_VERIFY:TRACE] 前缀行，解析为 TraceEvent 列表。
    按 seq 排序后返回。
    非结构化输出行被忽略（不报错）。
    """
    events: list[TraceEvent] = []
    # 使用更鲁棒的 JSON 提取: 先按行拆分, 对每行按前缀截取后尝试解析
    # 避免 .*? 在嵌套 JSON 中对第一个 } 提前终止的问题
    events: list[TraceEvent] = []
    for line in raw_stdout.splitlines():
        stripped = line.strip()
        if not stripped.startswith(TRACE_PREFIX):
            continue
        json_part = stripped[len(TRACE_PREFIX):].strip()
        if not json_part:
            continue
        try:
            data = json.loads(json_part)
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict):
            continue
        if "type" not in data or "seq" not in data:
            continue
        if data.get("type") not in TRACE_EVENT_TYPES:
            continue
        data["raw"] = data.copy()
        events.append(TraceEvent(**data))

    events.sort(key=lambda e: e.seq)
    return events


# ---------------------------------------------------------------------------
# JSON Schema 验证
# ---------------------------------------------------------------------------

def validate_against_schema(data: dict, schema: dict) -> tuple[bool, str | None]:
    """对 data 执行 JSON Schema 验证。

    返回 (pass, error_message)。
    使用 jsonschema 库（轻量回退）。
    """
    try:
        import jsonschema
        jsonschema.validate(instance=data, schema=schema)
        return True, None
    except ImportError:
        # 轻量回退: 仅检查 type 和 required
        return _lightweight_schema_check(data, schema)
    except jsonschema.exceptions.ValidationError as e:
        return False, str(e.message)


def _lightweight_schema_check(data: dict, schema: dict) -> tuple[bool, str | None]:
    """jsonschema 库不可用时的极简回退验证。"""
    if "type" in schema:
        expected_type = schema["type"]
        type_map = {"object": dict, "array": list, "string": str, "integer": int,
                     "number": (int, float), "boolean": bool}
        if expected_type in type_map:
            if not isinstance(data, type_map[expected_type]):
                return False, f"预期类型 {expected_type}，实际 {type(data).__name__}"
    if "required" in schema and isinstance(data, dict):
        for field in schema["required"]:
            if field not in data:
                return False, f"缺少必需字段: {field}"
    if "properties" in schema and isinstance(data, dict):
        for key, prop in schema["properties"].items():
            if key in data and "type" in prop:
                val = data[key]
                type_map = {"object": dict, "array": list, "string": str, "integer": int,
                             "number": (int, float), "boolean": bool}
                if prop["type"] in type_map:
                    if not isinstance(val, type_map[prop["type"]]):
                        return False, f"字段 '{key}' 预期类型 {prop['type']}，实际 {type(val).__name__}"
    return True, None


# ---------------------------------------------------------------------------
# Feature Flag 环境变量
# ---------------------------------------------------------------------------

def build_flag_env(flag_name: str, flag_value: str) -> dict:
    """构建单个 Flag 的环境变量 dict。

    flag_value 为 "ON" 或 "OFF"。
    返回 {"AGENT_FLAG_<NAME>": flag_value}。
    """
    env_key = f"{FLAG_ENV_PREFIX}{flag_name.upper()}"
    return {env_key: flag_value}


def build_all_flag_env(flags: dict[str, str]) -> dict:
    """构建多个 Flag 的环境变量 dict。

    flags: {"flag_name": "ON|OFF", ...}
    """
    result: dict[str, str] = {}
    for name, value in flags.items():
        result.update(build_flag_env(name, value))
    return result


# ---------------------------------------------------------------------------
# 哈希/校验
# ---------------------------------------------------------------------------

def compute_config_hash(config: dict) -> str:
    """计算配置 dict 的内容哈希（用于基线中的 config_hash 字段）。

    使用 SHA256，标准化 JSON 序列化后取前 8 位。
    """
    normalized = json.dumps(config, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:8]


# ---------------------------------------------------------------------------
# CLI 入口（供调试用）
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="common.py — 工具函数库（调试入口）")
    parser.add_argument("--resolve-skill-root", action="store_true", help="输出 Skill 根目录路径")
    parser.add_argument("--resolve-project-root", action="store_true", help="输出项目根目录路径")
    args = parser.parse_args()

    if args.resolve_skill_root:
        print(resolve_skill_root())
    elif args.resolve_project_root:
        root = resolve_project_root()
        print(root if root else "(none)")
    else:
        parser.print_help()
