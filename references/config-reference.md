# Configuration Reference

> 本文档是 agent-verify Skill 全部配置文件的完整字段参考，包括 `config.yaml`、`assertions.yaml`、`suites.yaml` 和 `baselines/` 目录结构。

---

## 1. config.yaml 完整字段参考

配置文件位于用户项目根下的 `agent-verify/config.yaml`。所有字段均为可选（有合理的默认值），但建议显式配置。

### 顶层字段

| 字段 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| `version` | string | `"1"` | 否 | 配置文件版本，用于未来兼容性检查 |
| `execution` | object | `{}` | 否 | 执行配置（见下方） |
| `assertions` | object | `{}` | 否 | 断言引擎配置（见下方） |
| `llm_judge` | object | `{}` | 否 | LLM 裁判配置（见下方） |
| `feature_flags` | object | `{}` | 否 | Feature Flag 定义（见下方） |
| `baselines` | object | `{}` | 否 | 基线管理配置（见下方） |
| `reports` | object | `{}` | 否 | 报告生成配置（见下方） |
| `coverage` | object | `{}` | 否 | 覆盖率追踪配置（见下方） |

### execution 字段

控制回归测试的执行行为。

| 字段 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| `mode` | string | `"sequential"` | 否 | 执行模式。`sequential`（串行，推荐）或 `parallel`（并行，V1.0） |
| `timeout` | integer | `120` | 否 | 每个测试用例的超时时间（秒） |
| `stop_on_first_error` | boolean | `false` | 否 | 首个断言失败时立即停止当前用例的后续断言检查 |
| `fail_fast` | boolean | `false` | 否 | 首个用例失败时立即停止整个回归测试 |
| `fail_fast_threshold` | integer | `3` | 否 | 连续失败多少个用例后停止。仅在 `fail_fast=false` 时生效 |
| `max_retries` | integer | `1` | 否 | 用例失败时的最大重试次数（V1.0）。`1` 表示不重试 |
| `retry_delay_ms` | integer | `1000` | 否 | 重试间隔（毫秒）（V1.0） |
| `agent_command` | string | `"claude --print"` | 否 | 执行 Agent 的 CLI 命令模板 |

**字段间依赖关系**:
- `fail_fast_threshold` 仅在 `fail_fast=false` 时生效
- `max_retries` 仅在 V1.0 启用

### assertions 字段

控制断言引擎的全局行为。

| 字段 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| `default_severity` | string | `"error"` | 否 | 断言未指定 `severity` 时的默认严重级别。`error` 或 `warning` |
| `file` | string | `"assertions.yaml"` | 否 | 断言定义文件路径（相对于 `agent-verify/` 目录） |
| `fail_on_warning` | boolean | `false` | 否 | 是否将 `warning` 级别的断言失败视为整体失败 |
| `allow_custom_script` | boolean | `false` | 否 | 是否允许执行 `custom_script` 断言。为 `true` 时需谨慎 |
| `custom_script_dir` | string | `"scripts/custom_checks"` | 否 | 自定义检查脚本的搜索目录 |

### llm_judge 字段

LLM 裁判评分器配置（V1.0 功能，MVP 阶段可忽略）。

| 字段 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| `enabled` | boolean | `false` | 否 | 是否默认启用 LLM 裁判 |
| `api_key` | string | `null` | 否 | Anthropic API Key。若为 null 则使用 `ANTHROPIC_API_KEY` 环境变量 |
| `primary_model` | string | `"claude-haiku"` | 否 | 一级初裁模型 |
| `arbitration_model` | string | `"claude-sonnet"` | 否 | 三级仲裁模型 |
| `n_runs` | integer | `3` | 否 | 每个维度的评分次数。取均值作为最终分 |
| `max_variance` | float | `1.5` | 否 | 方差阈值，超过则触发升级仲裁 |
| `max_budget_usd` | float | `50.0` | 否 | 月度最大预算（USD） |
| `quality_criteria` | object | `{}` | 否 | 评分维度定义。键为维度名，值为评分要求描述。默认包含 `accuracy`、`completeness`、`reasonableness` |

### feature_flags 字段

Feature Flag 定义和默认状态（V1.0 功能，MVP 阶段可忽略）。

| 字段 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| `flags` | list[object] | `[]` | 否 | Flag 定义列表（见下方每个 Flag 对象的字段） |
| `default_state` | string | `"OFF"` | 否 | 未明确指定的 Flag 的默认状态。`ON` 或 `OFF` |

每个 Flag 对象的字段：

| 字段 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| `name` | string | — | 是 | Flag 名称。会映射为环境变量 `AGENT_FLAG_<NAME>` |
| `description` | string | `""` | 否 | Flag 功能描述 |
| `default` | string | `"OFF"` | 否 | 默认状态。`ON` 或 `OFF` |

### baselines 字段

基线管理配置。

| 字段 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| `enabled` | boolean | `true` | 否 | 是否在回归测试后自动保存基线 |
| `dir` | string | `"baselines"` | 否 | 基线文件存储目录（相对于 `agent-verify/`） |
| `auto_save` | boolean | `true` | 否 | 回归测试完成后是否自动保存基线 |
| `max_kept` | integer | `20` | 否 | 最多保留的基线数量，超限时删除最旧的 |
| `compare_on_run` | boolean | `true` | 否 | 回归测试后是否自动与最新基线对比 |

### reports 字段

报告生成配置。

| 字段 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| `default_format` | string | `"markdown"` | 否 | 默认报告格式。`markdown`、`json` 或 `html`（V1.0） |
| `dir` | string | `"reports"` | 否 | 报告输出目录（相对于 `agent-verify/`） |
| `include_passed` | boolean | `true` | 否 | 报告中是否包含通过的断言详细结果 |

### coverage 字段

覆盖率追踪配置（V1.0）。

| 字段 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| `track_tools` | boolean | `false` | 否 | 是否追踪工具的覆盖率 |
| `track_prompts` | boolean | `false` | 否 | 是否追踪 prompt 模板 |
| `min_tool_coverage` | float | `0.0` | 否 | 工具最小覆盖率要求。如 `0.8` 表示需覆盖 80% 的工具 |

### 最小配置示例

```yaml
version: "1"
execution:
  timeout: 120
  agent_command: "claude --print"
assertions:
  file: assertions.yaml
baselines:
  enabled: true
reports:
  default_format: markdown
```

### 完整配置示例

```yaml
version: "1"
execution:
  mode: sequential
  timeout: 120
  stop_on_first_error: false
  fail_fast: false
  fail_fast_threshold: 3
  agent_command: "claude --print"
assertions:
  default_severity: error
  file: assertions.yaml
  fail_on_warning: false
  allow_custom_script: false
  custom_script_dir: scripts/custom_checks
llm_judge:
  enabled: false
  primary_model: claude-haiku
  arbitration_model: claude-sonnet
  n_runs: 3
  max_variance: 1.5
  max_budget_usd: 50.0
  quality_criteria:
    accuracy: "事实正确性：回答中的事实信息是否正确"
    completeness: "信息完整性：回答是否覆盖了问题的所有方面"
    reasonableness: "推理合理性：推理过程是否合乎逻辑"
feature_flags:
  default_state: OFF
  flags:
    - name: NEW_SEARCH_ALGORITHM
      description: "使用新版搜索算法"
      default: OFF
    - name: ENABLE_CACHE
      description: "启用结果缓存"
      default: ON
baselines:
  enabled: true
  dir: baselines
  auto_save: true
  max_kept: 20
  compare_on_run: true
reports:
  default_format: markdown
  dir: reports
  include_passed: true
coverage:
  track_tools: false
  track_prompts: false
  min_tool_coverage: 0.0
```

---

## 2. assertions.yaml 完整字段参考

断言定义文件的每条断言的完整字段说明。

### 顶层结构

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `assertions` | list[object] | 是 | 断言定义列表（文件根级数组） |

### 每条断言的字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 唯一标识，`kebab-case` 格式。在同一个文件中不可重复 |
| `name` | string | 是 | 人类可读的名称，显示在报告中 |
| `type` | string | 是 | 断言类型。可选值：`tool_call`、`tool_param`、`output_match`、`path_sequence`、`timing`、`output_schema`、`custom_script` |
| `target` | object | 是 | 断言目标，按类型有不同的字段（见下方） |
| `condition` | object | 是 | 断言条件，按类型有不同的字段（见下方） |
| `severity` | string | 否 | 严重级别。`error` 或 `warning`。默认使用全局 `default_severity` |
| `enabled` | boolean | 否 | 是否启用。设为 `false` 时引擎跳过此断言。默认 `true` |

### target 和 condition 字段按类型分类

参见 [assertions-guide.md](assertions-guide.md) 各类型的表格。

### 完整配置示例

参见 [assets/assertions.yaml.template](../assets/assertions.yaml.template)。

---

## 3. suites.yaml 完整字段参考

测试套件定义文件的完整字段说明。

### 顶层结构

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `version` | string | 否 | 套件文件版本。默认 `"1"` |
| `name` | string | 是 | 套件名称 |
| `description` | string | 否 | 套件描述 |
| `defaults` | object | 是 | 测试用例的默认配置（见下方） |
| `test_cases` | list[object] | 是 | 测试用例定义列表（至少 1 条） |
| `groups` | object | 否 | 分组定义（见下方） |

### defaults 字段

提供所有测试用例的默认值，可以在单个用例中覆盖。

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `agent_command` | string | 否 | Agent CLI 调用命令。默认使用 `config.yaml` 中的 `execution.agent_command` |
| `timeout` | integer | 否 | 用例级别超时（秒）。覆盖 `config.yaml` 中的全局值 |
| `assertions` | list[string] | 否 | 默认启用的断言 ID 列表。为空时运行全部启用断言 |
| `input_prefix` | string | 否 | 在用户输入前追加的上下文文本 |
| `tags` | list[string] | 否 | 默认标签 |
| `env` | object | 否 | 环境变量覆盖。键值对格式 |

### test_cases 字段

每一条测试用例的字段。

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 用例唯一标识，`kebab-case` 格式 |
| `name` | string | 是 | 人类可读的用例名称 |
| `description` | string | 否 | 用例描述 |
| `input` | string | 是 | 用户输入文本（Agent 的 stdin） |
| `expected` | string | 否 | 期望输出描述（供 LLM 裁判参考，不影响确定性断言） |
| `assertions` | list[string] | 否 | 此用例启用的断言 ID 列表。覆盖 `defaults.assertions` |
| `disabled_assertions` | list[string] | 否 | 此用例禁用的断言 ID 列表 |
| `tags` | list[string] | 否 | 标签列表。与 `defaults.tags` 合并 |
| `timeout` | integer | 否 | 用例级别超时（秒） |
| `input_prefix` | string | 否 | 在 `input` 前追加的上下文 |
| `env` | object | 否 | 用例级环境变量覆盖 |

### groups 字段

分组定义，用于 `--scope` 参数选择运行的用例子集。

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `<group_name>` | object | — | 分组名称。每个分组包含 `cases` 字段 |
| `<group_name>.description` | string | 否 | 分组描述 |
| `<group_name>.cases` | list[string] | 是 | 属于此分组的用例 ID 列表 |

预定义分组名及其语义：

| 分组名 | 语义 |
|--------|------|
| `smoke` | 冒烟测试（最关键的 3-5 条用例，快速验证基本功能） |
| `full` | 完整回归（所有用例） |
| 自定义 | 用户定义的任意分组 |

### 完整配置示例

参见 [assets/suites.yaml.template](../assets/suites.yaml.template)。

---

## 4. baselines/ 目录结构

基线快照存储目录（`agent-verify/baselines/`）的结构说明。

### 目录结构

```
agent-verify/baselines/
├── latest.json                     # 指向最新基线的符号链接（或内容文件）
├── baseline-2026-07-01T10-30-00.json
├── baseline-2026-07-01T14-15-00.json
├── baseline-2026-07-02T09-00-00.json
└── ...
```

### 基线文件格式

每个基线文件是 JSON 格式的 `BaselineSnapshot`：

```json
{
  "meta": {
    "name": "baseline-2026-07-01T10-30-00",
    "created": "2026-07-01T10:30:00Z",
    "suite": "search-suite",
    "config_hash": "a1b2c3d4",
    "git_commit": "abc123def456",
    "flags": {}
  },
  "summary": {
    "suite_name": "search-suite",
    "total_cases": 5,
    "passed_cases": 4,
    "failed_cases": 1,
    "assertion_pass_rate": 0.92,
    "llm_scores": {
      "accuracy": { "mean": 8.5, "std": 0.3 },
      "completeness": { "mean": 7.8, "std": 0.5 }
    },
    "avg_duration_ms": 45200,
    "avg_steps": 12.4,
    "failed_details": [
      {
        "case_id": "search-complex-001",
        "assertion_id": "at-least-one-search",
        "reason": "Tool \"web_search\" was called 0 times"
      }
    ],
    "flags": {}
  },
  "cases": [
    {
      "case_id": "search-simple-001",
      "assertion_results": [
        {
          "assertion_id": "at-least-one-search",
          "pass": true,
          "reason": null,
          "details": { "call_count": 3 }
        }
      ],
      "duration_ms": 32100,
      "steps": 8
    }
  ]
}
```

### 基线管理操作

| 操作 | 命令 | 说明 |
|------|------|------|
| 保存 | `--baseline-save <name>` | 保存当前回归结果为基线 |
| 列表 | `--baseline-list` | 列出所有基线（仅元信息） |
| 加载 | `--baseline-compare <name1> <name2>` | 对比两个基线 |
| 自动 | `auto_save: true` | 回归测试后自动保存基线 |
| 容量 | `max_kept: 20` | 自动删除超出数量的旧基线 |
