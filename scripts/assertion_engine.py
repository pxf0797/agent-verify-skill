#!/usr/bin/env python3

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
"""agent-verify Skill — 断言引擎（核心）。

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
对应命令: /agent-verify:assert（断言执行部分）

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
MVP 实现 3 种断言类型: tool_call, tool_param, output_match。

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
V1.0 类型标注 TODO: path_sequence, timing, output_schema, custom_script。

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
"""

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
import json

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
import os

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
import re

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
import subprocess

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
import sys

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
from typing import Any

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
from common import (

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    load_yaml_config, parse_trace_output, validate_against_schema,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    TraceEvent, TRACE_EVENT_TYPES,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
# ---------------------------------------------------------------------------

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
# 数据模型

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
# ---------------------------------------------------------------------------

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
class AssertionResult:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """单条断言的结果。"""

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    __slots__ = (

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        "assertion_id", "assertion_name", "assertion_type",

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        "pass_", "reason", "details", "severity",

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    )

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    def __init__(

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        self,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        assertion_id: str,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        assertion_name: str,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        assertion_type: str,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        pass_: bool,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        reason: str | None = None,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        details: dict | None = None,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        severity: str = "error",

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    ):

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        self.assertion_id = assertion_id

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        self.assertion_name = assertion_name

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        self.assertion_type = assertion_type

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        self.pass_ = pass_

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        self.reason = reason

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        self.details = details or {}

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        self.severity = severity

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    def to_dict(self) -> dict:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        return {s: getattr(self, s, None) for s in self.__slots__}

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
# ---------------------------------------------------------------------------

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
# 导出函数

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
# ---------------------------------------------------------------------------

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
def load_assertions(assertions_file: str) -> list[dict]:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """加载 assertions.yaml 并返回断言定义列表。

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    仅返回 enabled=true 的断言。

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    验证每条断言的 target 和 condition 字段完整性。

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    data = load_yaml_config(assertions_file)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    if "assertions" not in data:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        raise ValueError(f"断言文件缺少 'assertions' 根键: {assertions_file}")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    raw_list = data["assertions"]

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    if not isinstance(raw_list, list):

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        raise ValueError(

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            f"'assertions' 必须为列表，实际类型: {type(raw_list).__name__}"

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        )

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    validated: list[dict] = []

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    for idx, assertion in enumerate(raw_list):

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        if not isinstance(assertion, dict):

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            raise ValueError(f"第 {idx} 条断言不是 dict 类型")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        if not assertion.get("enabled", True):

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            continue

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        _validate_assertion(assertion, idx)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        validated.append(assertion)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    return validated

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
def _validate_assertion(assertion: dict, idx: int) -> None:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """验证单条断言定义。"""

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    if "id" not in assertion:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        raise ValueError(f"第 {idx} 条断言缺少 'id' 字段")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    if "type" not in assertion:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        raise ValueError(f"断言 '{assertion['id']}' 缺少 'type' 字段")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    if "target" not in assertion:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        raise ValueError(f"断言 '{assertion['id']}' 缺少 'target' 字段")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    if "condition" not in assertion:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        raise ValueError(f"断言 '{assertion['id']}' 缺少 'condition' 字段")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    atype = assertion["type"]

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    if atype not in CHECKER_MAP:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        raise ValueError(f"断言 '{assertion['id']}' 类型 '{atype}' 未知。支持的类型: {', '.join(CHECKER_MAP)}")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
def check_assertions(

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    trace: list,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    assertions: list[dict],

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    case_level_overrides: dict | None = None,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
) -> list[AssertionResult]:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """对所有断言执行检查。

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    Args:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        trace: list[TraceEvent]

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        assertions: load_assertions() 返回的列表

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        case_level_overrides: 用例级断言启用/禁用覆盖

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            {"assertion_id": True|False}

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    Returns:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        list[AssertionResult]

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    if case_level_overrides is None:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        case_level_overrides = {}

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    results: list[AssertionResult] = []

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    for assertion in assertions:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        aid = assertion["id"]

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        # 检查用例级覆盖

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        if aid in case_level_overrides:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            if not case_level_overrides[aid]:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                continue  # 被禁用

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        try:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            result = check_single_assertion(trace, assertion)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        except Exception as e:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            result = AssertionResult(

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                assertion_id=aid,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                assertion_name=assertion.get("name", aid),

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                assertion_type=assertion["type"],

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                pass_=False,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                reason=f"断言引擎异常: {e}",

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                severity=assertion.get("severity", "error"),

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            )

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        results.append(result)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    return results

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
def check_single_assertion(

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    trace: list,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    assertion: dict,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
) -> AssertionResult:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """对单条断言执行检查。"""

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    atype = assertion["type"]

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    target = assertion.get("target", {})

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    condition = assertion.get("condition", {})

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    severity = assertion.get("severity", "error")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    checker_class = CHECKER_MAP.get(atype)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    if checker_class is None:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        return AssertionResult(

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            assertion_id=assertion["id"],

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            assertion_name=assertion.get("name", assertion["id"]),

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            assertion_type=atype,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            pass_=False,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            reason=f"未实现的断言类型: '{atype}' (V1.0 启用)",

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            severity="error",

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        )

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    checker = checker_class()

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    try:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        pass_, reason, details = checker.check(trace, target, condition)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    except Exception as e:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        return AssertionResult(

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            assertion_id=assertion["id"],

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            assertion_name=assertion.get("name", assertion["id"]),

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            assertion_type=atype,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            pass_=False,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            reason=f"检查异常: {e}",

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            severity="error",

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        )

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    return AssertionResult(

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        assertion_id=assertion["id"],

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        assertion_name=assertion.get("name", assertion["id"]),

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        assertion_type=atype,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        pass_=pass_,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        reason=reason,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        details=details,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        severity=severity,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    )

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
# ---------------------------------------------------------------------------

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
# Checker 类

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
# ---------------------------------------------------------------------------

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
class ToolCallChecker:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """检查 tool_call 事件。

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    condition: min_count | max_count | exactly

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    target: {"tool_name": "bash"}

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    def check(self, trace: list, target: dict, condition: dict) -> tuple[bool, str | None, dict]:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        tool_name = target.get("tool_name")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        if not tool_name:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            return False, "target 缺少 'tool_name'", {}

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        # 统计匹配的 tool_call 事件

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        count = sum(

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            1 for e in trace

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            if e.type == "tool_call" and e.tool_name == tool_name

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        )

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        details = {

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            "tool_name": tool_name,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            "actual_count": count,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            "total_tool_calls": sum(1 for e in trace if e.type == "tool_call"),

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        }

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        # 检查各种条件

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        if "exactly" in condition:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            expected = int(condition["exactly"])

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            details["expected_exactly"] = expected

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            if count != expected:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                return False, f"期望调用 {expected} 次，实际 {count} 次", details

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        if "min_count" in condition:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            expected = int(condition["min_count"])

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            details["min_count"] = expected

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            if count < expected:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                return False, f"实际调用 {count} 次，低于最小值 {expected} 次", details

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        if "max_count" in condition:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            expected = int(condition["max_count"])

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            details["max_count"] = expected

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            if count > expected:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                return False, f"实际调用 {count} 次，超过最大值 {expected} 次", details

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        return True, None, details

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
class ToolParamChecker:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """检查 tool_call 事件的 input 参数。

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    condition: min_length | max_length | not_null | not_whitespace_only

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
              | pattern | allowed_values | forbidden_values

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    target: {"tool_name": "bash", "param": "command"}

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    def check(self, trace: list, target: dict, condition: dict) -> tuple[bool, str | None, dict]:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        tool_name = target.get("tool_name")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        param = target.get("param") or target.get("param_path")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        if not tool_name:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            return False, "target 缺少 'tool_name'", {}

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        if not param:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            return False, "target 缺少 'param'", {}

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        # 查找指定工具的调用

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        relevant_events = [

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            e for e in trace

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            if e.type == "tool_call" and e.tool_name == tool_name

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        ]

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        if not relevant_events:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            return False, f"未找到对 '{tool_name}' 的调用", {

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                "tool_name": tool_name, "param": param,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            }

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        details = {"tool_name": tool_name, "param": param, "events_found": len(relevant_events)}

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        all_pass = True

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        reasons: list[str] = []

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        for event in relevant_events:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            actual_input = event.input

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            if isinstance(actual_input, str):

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                try:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                    actual_input = json.loads(actual_input)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                except (json.JSONDecodeError, TypeError):

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                    pass

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            param_value = None

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            if isinstance(actual_input, dict):

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                param_value = actual_input.get(param)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            elif isinstance(actual_input, str):

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                param_value = actual_input

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            details.setdefault("param_values", [])

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            details["param_values"].append(param_value)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            if param_value is None and "not_null" in condition:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                if condition["not_null"]:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                    all_pass = False

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                    reasons.append(f"参数 '{param}' 在事件 seq={event.seq} 中为 null")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            if isinstance(param_value, str) and "not_whitespace_only" in condition:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                if condition["not_whitespace_only"] and param_value.strip() == "":

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                    all_pass = False

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                    reasons.append(f"参数 '{param}' 在事件 seq={event.seq} 中仅含空白字符")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            if isinstance(param_value, (str, list)):

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                length = len(param_value)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                details.setdefault("lengths", [])

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                details["lengths"].append(length)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                if "min_length" in condition:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                    expected = int(condition["min_length"])

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                    if length < expected:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                        all_pass = False

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                        reasons.append(f"参数 '{param}' 在事件 seq={event.seq} 中长度 {length} 低于最小值 {expected}")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                if "max_length" in condition:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                    expected = int(condition["max_length"])

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                    if length > expected:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                        all_pass = False

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                        reasons.append(f"参数 '{param}' 在事件 seq={event.seq} 中长度 {length} 超过最大值 {expected}")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            if isinstance(param_value, str) and "pattern" in condition:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                try:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                    if not re.search(condition["pattern"], param_value):

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                        all_pass = False

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                        reasons.append(f"参数 '{param}' 在事件 seq={event.seq} 中不匹配模式 '{condition['pattern']}'")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                except re.error as e:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                    all_pass = False

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                    reasons.append(f"正则 '{condition['pattern']}' 错误: {e}")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            if isinstance(param_value, str) and "allowed_values" in condition:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                allowed = condition["allowed_values"]

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                if isinstance(allowed, list) and param_value not in allowed:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                    all_pass = False

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                    reasons.append(f"参数 '{param}' 值 '{param_value}' 不在允许值列表 {allowed} 中")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            if isinstance(param_value, str) and "forbidden_values" in condition:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                forbidden = condition["forbidden_values"]

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                if isinstance(forbidden, list) and param_value in forbidden:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                    all_pass = False

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                    reasons.append(f"参数 '{param}' 值 '{param_value}' 在禁止值列表中")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        if not all_pass:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            return False, "; ".join(reasons), details

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        return True, None, details

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
class OutputMatchChecker:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """对 final_output 执行正则匹配。

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    condition: pattern | min_matches | case_sensitive

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    target: 可选，当前仅使用单个 final_output

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    def check(self, trace: list, target: dict, condition: dict) -> tuple[bool, str | None, dict]:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        # 获取 final_output

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        final_output = ""

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        for e in trace:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            if e.type == "run_end" and e.final_output:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                final_output = e.final_output

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                break

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        # 尝试从 trace 最后几个事件中获取 final_output

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        if not final_output:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            for e in reversed(trace):

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                if e.final_output:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                    final_output = e.final_output

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                    break

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        pattern = condition.get("pattern", "")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        if not pattern:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            return False, "condition 缺少 'pattern'", {}

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        flags = 0

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        if not condition.get("case_sensitive", True):

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            flags = re.IGNORECASE

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        try:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            matches = list(re.finditer(pattern, final_output, flags))

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        except re.error as e:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            return False, f"正则错误: {e}", {"pattern": pattern}

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        match_count = len(matches)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        min_matches = int(condition.get("min_matches", 1))

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        details = {

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            "pattern": pattern,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            "match_count": match_count,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            "min_matches": min_matches,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            "case_sensitive": condition.get("case_sensitive", True),

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            "output_length": len(final_output),

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        }

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        match_behavior = condition.get("match_behavior", "must_match")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        if match_behavior == "must_not_match":

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            if match_count > 0:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                return False, f"不应匹配但发现了 {match_count} 次匹配", details

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            else:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                return True, None, details

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        # 默认: must_match

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        if match_count >= min_matches:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            return True, None, details

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        else:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            return False, f"匹配次数 {match_count} 低于最小值 {min_matches}", details

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
# ---------------------------------------------------------------------------

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
# V1.0 Checker 存根（标注 TODO）

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
# ---------------------------------------------------------------------------

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
class PathSequenceChecker:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """检查 llm_response 事件的 step 序列。

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    TODO(V1.0): 实现路径顺序检查。

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    def check(self, trace: list, target: dict, condition: dict) -> tuple[bool, str | None, dict]:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        return False, "path_sequence 检查器 (V1.0 启用)", {"not_implemented": True}

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
class TimingChecker:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """检查步骤耗时。

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    TODO(V1.0): 实现计时检查。

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    def check(self, trace: list, target: dict, condition: dict) -> tuple[bool, str | None, dict]:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        return False, "timing 检查器 (V1.0 启用)", {"not_implemented": True}

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
class OutputSchemaChecker:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """对 final_output 执行 JSON Schema 验证。

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    TODO(V1.0): 实现 JSON Schema 验证。

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    def check(self, trace: list, target: dict, condition: dict) -> tuple[bool, str | None, dict]:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        return False, "output_schema 检查器 (V1.0 启用)", {"not_implemented": True}

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
class CustomScriptChecker:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """调用外部脚本执行自定义检查。

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    TODO(V1.0): 完善子进程调用。

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    def check(self, trace: list, target: dict, condition: dict) -> tuple[bool, str | None, dict]:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        script_path = target.get("script")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        if not script_path:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            return False, "target 缺少 'script' (自定义脚本路径)", {}

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        try:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            result = subprocess.run(

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                [sys.executable, script_path],

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                input=json.dumps({"trace": [e.to_dict() for e in trace]}),

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                capture_output=True, text=True, timeout=30,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            )

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            if result.returncode != 0:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                return False, f"自定义脚本退出码 {result.returncode}: {result.stderr.strip()}", {}

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            output = json.loads(result.stdout)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            return output.get("pass", False), output.get("reason"), output.get("details", {})

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        except subprocess.TimeoutExpired:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            return False, f"自定义脚本超时: {script_path}", {}

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        except (json.JSONDecodeError, subprocess.SubprocessError) as e:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            return False, f"自定义脚本执行错误: {e}", {}

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
# ---------------------------------------------------------------------------

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
# Checker 注册表

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
# ---------------------------------------------------------------------------

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
CHECKER_MAP: dict[str, type] = {

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    "tool_call": ToolCallChecker,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    "tool_param": ToolParamChecker,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    "output_match": OutputMatchChecker,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    "path_sequence": PathSequenceChecker,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    "timing": TimingChecker,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    "output_schema": OutputSchemaChecker,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    "custom_script": CustomScriptChecker,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
}

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
# ---------------------------------------------------------------------------

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
# CLI 入口

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
# ---------------------------------------------------------------------------

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
def _cli_check(args: Any) -> None:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """--check 模式: 加载 trace + assertions 并执行断言检查。"""

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    trace_file = args.trace

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    assertions_file = args.assertions

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    output_file = args.output

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    # 加载 trace

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    if not os.path.exists(trace_file):

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        print(json.dumps({"error": f"Trace 文件不存在: {trace_file}"}), file=sys.stderr)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        sys.exit(1)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    from common import load_jsonl

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    raw_records = load_jsonl(trace_file)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    # 从 jsonl dict 转 TraceEvent

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    trace = [TraceEvent(**r) for r in raw_records]

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    # 加载断言

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    try:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        assertions = load_assertions(assertions_file)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    except (FileNotFoundError, ValueError) as e:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        print(json.dumps({"error": str(e)}), file=sys.stderr)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        sys.exit(1)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    # 执行检查

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    results = check_assertions(trace, assertions)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    output = {

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        "total": len(results),

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        "passed": sum(1 for r in results if r.pass_),

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        "failed": sum(1 for r in results if not r.pass_),

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        "results": [r.to_dict() for r in results],

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    }

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    output_json = json.dumps(output, ensure_ascii=False, indent=2)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    if output_file:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        with open(output_file, "w", encoding="utf-8") as f:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            f.write(output_json)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            f.write("\n")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    else:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        print(output_json)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
# ---------------------------------------------------------------------------

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
# --list / --remove / --run CLI 辅助

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
# ---------------------------------------------------------------------------

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
def _cli_list(args: Any) -> None:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """--list 模式: 列出 assertions.yaml 中的所有断言。"""

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    assertions_file = args.assertions

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    if not assertions_file or not os.path.exists(assertions_file):

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        print(json.dumps({"error": f"断言文件不存在: {assertions_file}"}), file=sys.stderr)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        sys.exit(1)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    from common import load_yaml_config

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    data = load_yaml_config(assertions_file)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    raw_list = data.get("assertions", [])

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    rows = []

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    for a in raw_list:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        rows.append({

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            "id": a.get("id", "?"),

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            "name": a.get("name", ""),

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            "type": a.get("type", "?"),

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            "enabled": a.get("enabled", True),

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            "target": str(a.get("target", {})),

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        })

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    print(json.dumps({"count": len(rows), "assertions": rows}, ensure_ascii=False, indent=2))

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
def _cli_remove(args: Any) -> None:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """--remove 模式: 按 id 删除断言。"""

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    assertions_file = args.assertions

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    remove_id = args.remove

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    if not assertions_file or not os.path.exists(assertions_file):

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        print(json.dumps({"error": f"断言文件不存在: {assertions_file}"}), file=sys.stderr)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        sys.exit(1)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    from common import load_yaml_config

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    data = load_yaml_config(assertions_file)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    raw_list = data.get("assertions", [])

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    new_list = [a for a in raw_list if a.get("id") != remove_id]

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    if len(new_list) == len(raw_list):

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        print(json.dumps({"error": f"未找到 id 为 '{remove_id}' 的断言"}), file=sys.stderr)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        sys.exit(1)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    data["assertions"] = new_list

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    import yaml

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    with open(assertions_file, "w", encoding="utf-8") as f:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    print(json.dumps({"removed": remove_id, "remaining": len(new_list)}, ensure_ascii=False, indent=2))

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
def _cli_run_single(args: Any) -> None:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    """--run 模式: 运行单个断言。"""

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    trace_file = args.trace

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    assertions_file = args.assertions

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    run_id = args.run

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    if not trace_file or not os.path.exists(trace_file):

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        print(json.dumps({"error": f"Trace 文件不存在: {trace_file}"}), file=sys.stderr)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        sys.exit(1)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    if not assertions_file or not os.path.exists(assertions_file):

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        print(json.dumps({"error": f"断言文件不存在: {assertions_file}"}), file=sys.stderr)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        sys.exit(1)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    from common import load_jsonl

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    raw_records = load_jsonl(trace_file)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    trace = [TraceEvent(**r) for r in raw_records]

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    try:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        assertions = load_assertions(assertions_file)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    except (FileNotFoundError, ValueError) as e:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        print(json.dumps({"error": str(e)}), file=sys.stderr)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        sys.exit(1)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    # 按 id 筛选

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    target = [a for a in assertions if a.get("id") == run_id]

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    if not target:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        print(json.dumps({"error": f"未找到 id 为 '{run_id}' 的已启用断言"}), file=sys.stderr)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        sys.exit(1)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    result = check_single_assertion(trace, target[0])

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    output = {"result": result.to_dict()}

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    print(json.dumps(output, ensure_ascii=False, indent=2))

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
if __name__ == "__main__":

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    import argparse

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    parser = argparse.ArgumentParser(

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        description="agent-verify Skill — 断言引擎",

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        formatter_class=argparse.RawDescriptionHelpFormatter,

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        epilog="示例:\n"

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
               "  python scripts/assertion_engine.py --check --trace trace.jsonl --assertions assertions.yaml\n"

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
               "  python scripts/assertion_engine.py --list --assertions assertions.yaml\n"

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
               "  python scripts/assertion_engine.py --remove <id> --assertions assertions.yaml\n"

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
               "  python scripts/assertion_engine.py --run <id> --trace trace.jsonl --assertions assertions.yaml\n",

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    )

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    parser.add_argument(

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        "--check", action="store_true",

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        help="执行断言检查模式",

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    )

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    parser.add_argument("--list", action="store_true",

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                        help="列出当前 assertions.yaml 中的所有断言")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    parser.add_argument("--remove", metavar="ID",

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                        help="按 id 删除断言")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    parser.add_argument("--run", metavar="ID",

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
                        help="运行单个断言（需 --trace 和 --assertions）")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    parser.add_argument("--trace", help="trace.jsonl 文件路径")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    parser.add_argument("--assertions", help="assertions.yaml 文件路径")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    parser.add_argument("--output", help="输出 JSON 文件路径（可选）")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    args = parser.parse_args()

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}


        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    if args.check:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        if not args.trace or not args.assertions:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            parser.error("--check 模式需要 --trace 和 --assertions 参数")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        _cli_check(args)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    elif args.list:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        if not args.assertions:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            parser.error("--list 模式需要 --assertions 参数")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        _cli_list(args)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    elif args.remove:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        if not args.assertions:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            parser.error("--remove 模式需要 --assertions 参数")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        _cli_remove(args)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    elif args.run:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        if not args.trace or not args.assertions:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
            parser.error("--run 模式需要 --trace 和 --assertions 参数")

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        _cli_run_single(args)

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
    else:

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
        parser.print_help()

        # 安全检查: 禁止路径遍历
        if ".." in script_path:
            return False, f"脚本路径不安全 (含 '..'): {script_path}", {}
        if not os.path.exists(script_path):
            return False, f"自定义脚本不存在: {script_path}", {}
        if not os.access(script_path, os.X_OK):
            return False, f"自定义脚本不可执行: {script_path}", {}
