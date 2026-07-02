#!/usr/bin/env python3
"""agent-verify Skill — 初始化命令实现。

对应命令: /agent-verify:init [--target <name>] [--template <type>]

行为:
    1. 在 target_dir 下创建 agent-verify/ 目录
    2. 创建子目录: suites/, baselines/, reports/
    3. 从 assets/ 复制模板文件（含变量替换: target_name）
    4. 根据 template_type 决定复制哪些文件:
       - "default": 全部 3 个模板
       - "minimal": 仅 config.yaml.template + assertions.yaml.template
    5. 输出初始化报告
"""

import os
import shutil
import sys
from datetime import date
from pathlib import Path

# 添加 scripts/ 到 path 以支持直接运行
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (
    resolve_skill_root,
    PROJECT_DIR_NAME, SUITE_DIR, BASELINE_DIR, REPORT_DIR,
    CONFIG_FILENAME, ASSERTIONS_FILENAME,
    PLACEHOLDER_TARGET_NAME, PLACEHOLDER_CURRENT_DATE, PLACEHOLDER_SKILL_VERSION,
    SKILL_VERSION,
)


TEMPLATE_FILES = {
    "config.yaml.template": CONFIG_FILENAME,
    "assertions.yaml.template": ASSERTIONS_FILENAME,
    "suites.yaml.template": f"{SUITE_DIR}/suites.yaml",
}

SUB_DIRS = [SUITE_DIR, BASELINE_DIR, REPORT_DIR]


def init_project(
    target_dir: str,
    target_name: str | None = None,
    template_type: str = "default",
) -> dict:
    """初始化验证项目。

    Args:
        target_dir: 目标目录（绝对路径）
        target_name: Agent/Skill 名称，None 时使用目录名
        template_type: "default" | "minimal"

    Returns:
        {
            "status": "success" | "error",
            "message": "人类可读的初始化报告",
            "created_files": ["path1", "path2", ...],
            "next_steps": ["建议1", "建议2", ...],
        }
    """
    if template_type not in ("default", "minimal"):
        return {
            "status": "error",
            "message": f"不支持的模板类型: '{template_type}'。可选: 'default', 'minimal'。",
            "created_files": [],
            "next_steps": [],
        }

    if not os.path.isdir(target_dir):
        return {
            "status": "error",
            "message": f"目标目录不存在: {target_dir}",
            "created_files": [],
            "next_steps": [],
        }

    # 确定目标名称
    if target_name is None:
        target_name = os.path.basename(os.path.normpath(target_dir))

    # 创建 agent-verify/ 目录
    verify_dir = os.path.join(target_dir, PROJECT_DIR_NAME)
    os.makedirs(verify_dir, exist_ok=True)

    created_files: list[str] = []

    # 创建子目录
    for sub in SUB_DIRS:
        sub_path = os.path.join(verify_dir, sub)
        os.makedirs(sub_path, exist_ok=True)

    # 确定要复制的模板
    if template_type == "minimal":
        templates_to_copy = ["config.yaml.template", "assertions.yaml.template"]
    else:
        templates_to_copy = list(TEMPLATE_FILES.keys())

    # 从 assets/ 复制模板
    skill_root = resolve_skill_root()
    assets_dir = os.path.join(skill_root, "assets")

    if not os.path.isdir(assets_dir):
        # assets/ 不存在，创建基本模板文件
        _write_default_templates(verify_dir, templates_to_copy, target_name)
        for t in templates_to_copy:
            dest_name = TEMPLATE_FILES.get(t, t)
            created_files.append(os.path.join(verify_dir, dest_name))
    else:
        for template_name in templates_to_copy:
            src = os.path.join(assets_dir, template_name)
            dest_rel = TEMPLATE_FILES.get(template_name, template_name)
            dest = os.path.join(verify_dir, dest_rel)

            if os.path.exists(src):
                # 复制并进行变量替换
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(src, "r", encoding="utf-8") as f:
                    content = f.read()
                content = content.replace(PLACEHOLDER_TARGET_NAME, target_name)
                content = content.replace(PLACEHOLDER_CURRENT_DATE, date.today().isoformat())
                content = content.replace(PLACEHOLDER_SKILL_VERSION, SKILL_VERSION)
                with open(dest, "w", encoding="utf-8") as f:
                    f.write(content)
                created_files.append(dest)
            else:
                # 模板文件不存在，写入默认内容
                _write_default_template(dest, template_name, target_name)
                created_files.append(dest)

    next_steps = _get_next_steps(created_files, template_type)

    return {
        "status": "success",
        "message": f"Agent 验证项目 '{target_name}' 初始化完成。",
        "created_files": created_files,
        "next_steps": next_steps,
    }


def _write_default_templates(verify_dir: str, templates: list[str], target_name: str) -> None:
    """当 assets/ 目录不存在时，写入默认模板内容。"""
    for t in templates:
        dest_rel = TEMPLATE_FILES.get(t, t)
        dest = os.path.join(verify_dir, dest_rel)
        _write_default_template(dest, t, target_name)


def _write_default_template(dest: str, template_name: str, target_name: str) -> None:
    """写入单个默认模板文件。"""
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    content = _get_default_content(template_name, target_name)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(content)


def _get_default_content(template_name: str, target_name: str) -> str:
    """根据模板名称返回默认内容。"""
    today = date.today().isoformat()

    if template_name == "config.yaml.template":
        return f"""# agent-verify 配置 (Skill v{SKILL_VERSION})
# 完整参考: references/config-reference.md
version: "{SKILL_VERSION}"

execution:
  agent_command: "claude --print"
  timeout: 120
  stop_on_first_error: false
  fail_fast_threshold: 3

assertions:
  default_severity: "error"

# (V1.0) llm_judge:
# (V1.0)   enabled: false

# (V1.0) feature_flags:
# (V1.0)   flags: []

baselines:
  max_stored: 20

reports:
  default_format: "markdown"

coverage:
  min_assertion_rate: 0.0
"""
    elif template_name == "assertions.yaml.template":
        return f"""# assertions.yaml — {target_name} 的断言定义
# 完整参考: references/assertions-guide.md
assertions:
  # 示例 1: 验证工具调用次数
  - id: "example-tool-call-001"
    name: "示例: 验证工具调用次数"
    type: "tool_call"
    enabled: false
    severity: "error"
    target:
      tool_name: "bash"
    condition:
      min_count: 1
      max_count: 10

  # 示例 2: 验证输出包含特定内容
  - id: "example-output-001"
    name: "示例: 验证输出内容"
    type: "output_match"
    enabled: false
    severity: "warning"
    target: {{}}
    condition:
      pattern: "成功|完成|done"
      min_matches: 1
"""
    elif template_name == "suites.yaml.template":
        return f"""# suites.yaml — {target_name} 的测试套件定义
version: "{SKILL_VERSION}"

defaults:
  agent_command: "claude --print"
  timeout: 120

groups:
  smoke:
    - "simple-search-001"

test_cases:
  - id: "simple-search-001"
    name: "简单搜索测试"
    input: "搜索关于 Python 编程语言的基本信息并返回摘要。"
    expected_path:
      - "planning"
      - "execution"
      - "verification"
"""
    return ""


def _get_next_steps(created_files: list[str], template_type: str) -> list[str]:
    """生成下一步建议。"""
    steps = [
        "编辑 config.yaml 配置你的 Agent/Skill 设置",
        "编辑 assertions.yaml 添加你的第一条断言",
    ]
    if template_type == "default":
        steps.append("编辑 suites/suites.yaml 添加测试用例")
    steps.extend([
        "运行 /agent-verify:regression 执行首次回归测试",
        "运行 /agent-verify:baseline --save baseline-001 保存基线",
    ])
    return steps


def generate_init_report(result: dict) -> str:
    """将 init_project 的返回 dict 渲染为 Markdown 报告。"""
    lines = []
    lines.append("# agent-verify 初始化报告\n")

    if result["status"] == "error":
        lines.append(f"**状态**: ❌ 失败\n")
        lines.append(f"**错误信息**: {result['message']}\n")
        return "\n".join(lines)

    lines.append(f"**状态**: ✅ 成功\n")
    lines.append(f"**消息**: {result['message']}\n")

    lines.append("## 创建的文件\n")
    if result["created_files"]:
        for f in result["created_files"]:
            lines.append(f"- `{f}`")
    else:
        lines.append("（无文件创建）")

    lines.append("\n## 目录结构\n")
    lines.append("```")
    lines.append("agent-verify/")
    lines.append("├── config.yaml")
    lines.append("├── assertions.yaml")
    lines.append("├── suites/")
    lines.append("├── baselines/")
    lines.append("└── reports/")
    lines.append("```")

    lines.append("\n## 下一步\n")
    for i, step in enumerate(result["next_steps"], 1):
        lines.append(f"{i}. {step}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="agent-verify Skill — 项目初始化",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n  python scripts/init_verify.py --target-dir /path/to/project --target-name my-agent\n"
               "  python scripts/init_verify.py --target-dir . --template minimal",
    )
    parser.add_argument(
        "--target-dir", required=True,
        help="目标项目目录（绝对路径）",
    )
    parser.add_argument(
        "--target-name", default=None,
        help="Agent/Skill 名称（默认使用目录名）",
    )
    parser.add_argument(
        "--template", default="default", choices=["default", "minimal"],
        help="模板类型（default=全部，minimal=仅配置+断言）",
    )

    args = parser.parse_args()
    result = init_project(args.target_dir, args.target_name, args.template)

    if result["status"] == "success":
        print(generate_init_report(result))
        sys.exit(0)
    else:
        print(generate_init_report(result), file=sys.stderr)
        sys.exit(1)
