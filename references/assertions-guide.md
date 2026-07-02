# Assertions Guide

> 本文档是 agent-verify Skill 的断言系统完整参考。6 种断言类型 + `custom_script` 扩展的详细说明、YAML 配置示例、适用场景和最佳实践。

- **MVP (3 种)**: `tool_call`, `tool_param`, `output_match` — 必须实现
- **V1.0 (3 种)**: `path_sequence`, `timing`, `output_schema` — 接口定义完整，引擎可 stub
- **扩展**: `custom_script` — 通用扩展点，MVP/V1.0 均支持

---

## 断言通用结构

每条断言在 `assertions.yaml` 中遵循以下结构：

```yaml
- id: <kebab-case-id>       # 唯一标识，如 "search-tool-called"
  name: <human-readable>    # 人类可读名称，显示在报告中
  type: <assertion_type>    # 断言类型，见下方各节
  target:                   # 断言目标
    <field>: <value>        # 按类型不同
  condition:                # 断言条件
    <field>: <value>        # 按类型不同
  severity: <error|warning> # 可选，默认 error
  enabled: <true|false>     # 可选，默认 true
```

---

## 1. `tool_call` — 工具调用计数断言 (MVP)

### 功能描述

统计 Agent 运行过程中指定工具被调用的次数，与预期次数比较。用于验证 Agent 是否在合适的时机调用了正确的工具。

### 适用场景

- 验证搜索类 Agent 至少调用了 1 次 `web_search` 工具
- 验证代码生成 Agent 恰好调用了 1 次 `write_file` 工具
- 验证复杂工作流中某个工具没有被过度调用（不超过 N 次）

### target / condition 字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `target.tool_name` | string | 是 | 要统计的工具名称，精确匹配 |
| `condition.min_count` | integer | 否 | 最小调用次数。实际次数 >= min_count 则通过 |
| `condition.max_count` | integer | 否 | 最大调用次数。实际次数 <= max_count 则通过 |
| `condition.exactly` | integer | 否 | 精确调用次数。实际次数 == exactly 则通过。与 min/max_count 互斥 |

### YAML 配置示例

```yaml
# 示例 1: 验证搜索工具至少被调用了 1 次
- id: at-least-one-search
  name: "Search tool was called at least once"
  type: tool_call
  target:
    tool_name: web_search
  condition:
    min_count: 1
  severity: error

# 示例 2: 验证写文件工具只被调用了 1 次
- id: write-file-exactly-once
  name: "Write file called exactly once"
  type: tool_call
  target:
    tool_name: write_file
  condition:
    exactly: 1

# 示例 3: 验证某个昂贵的工具没有被过度调用
- id: expensive-tool-cap
  name: "Expensive tool not called too many times"
  type: tool_call
  target:
    tool_name: web_scrape
  condition:
    max_count: 3
  severity: warning
```

### 最佳实践

- `min_count: 1` 是最常用模式，用于验证关键工具被调用
- `exactly` 适用于确定性工作流（如"只写一次文件"）
- `max_count` 适用于成本控制（如限制昂贵的 API 调用）
- 对非关键约束使用 `severity: warning`，避免回归测试中误判为失败

### 边界情况

- `trace` 中没有 `tool_call` 事件：实际调用次数为 0
- 工具名称不存在（`target.tool_name` 拼写错误）：0 匹配，断言失败
- `min_count: 0`：始终通过（等价于不检查）
- `condition` 同时设置了 `min_count` 和 `exactly`：引擎应报配置验证错误

---

## 2. `tool_param` — 工具调用参数断言 (MVP)

### 功能描述

检查 Agent 调用指定工具时，传入参数是否满足特定约束。用于验证 Agent 生成正确、合法、安全的工具参数。

### 适用场景

- 验证搜索工具的查询参数不为空
- 验证搜索查询的最小长度
- 验证工具参数符合预期格式（正则匹配）
- 验证参数值在允许的取值范围内
- 验证参数不会包含禁止值（安全约束）

### target / condition 字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `target.tool_name` | string | 是 | 工具名称 |
| `target.param_path` | string | 是 | 参数路径，点号分隔。如 `query`, `input.text`, `options.max_tokens` |
| `condition.min_length` | integer | 否 | 参数值（字符串）的最小长度 |
| `condition.max_length` | integer | 否 | 参数值（字符串）的最大长度 |
| `condition.not_null` | boolean | 否 | 设为 `true` 时参数值不能为 null/None |
| `condition.not_whitespace_only` | boolean | 否 | 设为 `true` 时参数值不能仅为空白字符 |
| `condition.pattern` | string | 否 | 参数值必须匹配的正则表达式 |
| `condition.allowed_values` | list[string] | 否 | 参数值必须在此列表中 |
| `condition.forbidden_values` | list[string] | 否 | 参数值不能在此列表中 |

### YAML 配置示例

```yaml
# 示例 1: 搜索查询不为空且有意义长度
- id: search-query-not-empty
  name: "Search query is not empty"
  type: tool_param
  target:
    tool_name: web_search
    param_path: query
  condition:
    not_null: true
    not_whitespace_only: true
    min_length: 3

# 示例 2: 工具参数值在允许的范围内
- id: search-result-count-allowed
  name: "Result count within allowed values"
  type: tool_param
  target:
    tool_name: web_search
    param_path: max_results
  condition:
    allowed_values:
      - "5"
      - "10"
      - "20"

# 示例 3: 防止危险的工具参数
- id: no-dangerous-commands
  name: "No dangerous shell commands"
  type: tool_param
  target:
    tool_name: run_shell
    param_path: command
  condition:
    forbidden_values:
      - "rm -rf /"
      - "sudo rm -rf /"
    pattern: "^(?!.*rm -rf).*$"
```

### 最佳实践

- `not_null` + `not_whitespace_only` + `min_length` 三件套是最常用的非空组合
- `allowed_values` 适用于枚举型参数（语言选择、结果数量等）
- `forbidden_values` 适用于安全检查（禁止的命令、禁止的域名等）
- `param_path` 使用点号表示嵌套路径：`input.arg1.option.sub_option`

### 边界情况

- 参数路径不存在：如果工具被调用但未提供该参数，视为参数值为 null
- 多个工具调用：引擎对每次工具调用的参数逐个检查，任一满足则通过
- 参数值为非字符串类型（如数字、数组）：`min_length` `/` `max_length` 对非字符串无效，应标记为配置警告

---

## 3. `output_match` — 输出匹配断言 (MVP)

### 功能描述

对 Agent 的 `final_output` 执行正则匹配。用于验证 Agent 的输出是否包含（或不包含）特定内容。

### 适用场景

- 验证输出包含预期格式（如 JSON 结构、代码块）
- 验证输出包含关键信息片段（如获奖者姓名）
- 验证输出不包含不安全内容（如 PII、错误信息）
- 验证输出符合结构化格式要求

### target / condition 字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `target.field` | string | 否 | 可选。默认检查 `final_output`。可指定检查特定字段如 `tool_result` |
| `condition.pattern` | string | 是 | 要匹配的正则表达式 |
| `condition.min_matches` | integer | 否 | 最少匹配次数。默认 1。设为 0 时表示"不应匹配"（负向断言） |
| `condition.case_sensitive` | boolean | 否 | 是否大小写敏感。默认 `true` |

### YAML 配置示例

```yaml
# 示例 1: 验证输出包含代码块
- id: contains-code-block
  name: "Output contains a code block"
  type: output_match
  target:
    field: final_output
  condition:
    pattern: '```[\s\S]*?```'
    min_matches: 1

# 示例 2: 验证输出包含指定名称（大小写不敏感）
- id: contains-expected-name
  name: "Output contains expected name"
  type: output_match
  condition:
    pattern: "Geoffrey Hinton"
    case_sensitive: false

# 示例 3: 验证输出不包含错误信息（负向断言）
- id: no-error-message
  name: "Output does not contain error message"
  type: output_match
  condition:
    pattern: "Error|Exception|Traceback|FAILED"
    min_matches: 0
    case_sensitive: false

# 示例 4: 验证输出包含 URL
- id: contains-source-url
  name: "Output contains a source URL"
  type: output_match
  condition:
    pattern: 'https?://[^\s\)\]]+'
    min_matches: 1
```

### 最佳实践

- 正向断言（`min_matches: 1` 或更多）用于验证必要内容
- 负向断言（`min_matches: 0`）用于验证不应出现的内容
- 非英语场景务必设置 `case_sensitive: false`
- 正则表达式使用 raw string 语法（YAML 字符串中无需额外转义 `\`）
- 复杂正则建议先单独测试再写入断言

### 边界情况

- 输出为空字符串：正则匹配结果为空，`min_matches: 1` 的断言失败
- `target.field` 在 Agent 输出中不存在：视为该字段不存在，匹配结果为 0
- 正则语法错误：引擎应报配置错误，不静默失败
- `pattern` 包含 YAML 特殊字符时需要用引号包裹：`"pattern: 'value'"`

---

## 4. `path_sequence` — 执行路径顺序断言 (V1.0)

### 功能描述

验证 Agent 的 `llm_response` 事件的 `step` 字段是否按预期顺序执行。用于测试 Agent 是否遵循了预期的工作流阶段序列。

### 适用场景

- 验证搜索 Agent 的"规划→搜索→回答"三阶段流程
- 验证复杂工作流中的阶段顺序
- 验证错误处理流程中的降级路径

### target / condition 字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `target.steps` | list[string] | 是 | 预期步骤序列。如 `[planning, execution, verification]` |
| `target.source` | string | 否 | 步骤来源字段。默认 `step`，也可以检查其他字段 |
| `condition.order` | string | 是 | 顺序匹配模式：`strict` 或 `relaxed` |
| `condition.all_present` | boolean | 否 | 是否要求所有指定步骤都至少出现一次。默认 `true` |

### YAML 配置示例

```yaml
# 示例 1: 严格顺序匹配
- id: strict-search-flow
  name: "Search flow follows strict order"
  type: path_sequence
  target:
    steps:
      - planning
      - execution
      - verification
  condition:
    order: strict
    all_present: true

# 示例 2: 宽松顺序匹配（允许中间插入其他步骤）
- id: relaxed-report-flow
  name: "Report flow in relaxed order"
  type: path_sequence
  target:
    steps:
      - planning
      - execution
  condition:
    order: relaxed
```

### 最佳实践

- `strict` 模式要求 Agent 的步骤序列完全匹配且不能有额外步骤插入
- `relaxed` 模式只要求指定步骤按顺序出现，允许中间有其他步骤
- 优先使用 `relaxed` 模式，它对 Agent 行为变化有更好的容错性

### 边界情况

- trace 中没有 `llm_response` 事件：步骤序列为空，断言失败
- 目标步骤未出现：`all_present: true` 时失败，`all_present: false` 时跳过
- Agent 的 step 字段缺失：引擎应将其视为未知步骤，不影响已知步骤的顺序检查

---

## 5. `timing` — 执行时间断言 (V1.0)

### 功能描述

检查 Agent 运行过程中特定阶段或整体执行的耗时。用于确保 Agent 在合理的时间范围内完成工作。

### 适用场景

- 验证搜索 Agent 在 N 秒内完成
- 验证关键工具调用不应超过 N 毫秒
- 验证整体执行时间满足 SLA 要求

### target / condition 字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `target.phase` | string | 否 | 要检查的阶段。`total`（整体）、`<tool_name>`（特定工具调用耗时）、`<step_name>`（特定步骤耗时）。默认 `total` |
| `condition.max_duration_ms` | integer | 否 | 最大允许耗时（毫秒） |
| `condition.min_duration_ms` | integer | 否 | 最小要求耗时。很少使用，可用于确保 Agent 没有"跳过"工作 |

### YAML 配置示例

```yaml
# 示例 1: 整体执行时间不超过 60 秒
- id: total-time-limit
  name: "Total execution under 60s"
  type: timing
  target:
    phase: total
  condition:
    max_duration_ms: 60000

# 示例 2: 特定工具的调用耗时不超过 10 秒
- id: search-tool-fast
  name: "Search tool response under 10s"
  type: timing
  target:
    phase: web_search
  condition:
    max_duration_ms: 10000
```

### 最佳实践

- `max_duration_ms` 是主要使用模式，用于 SLA 验证
- `phase` 为 `total` 时检查 Agent 从开始到结束的整体耗时
- `phase` 为工具名称时，检查该工具所有调用的平均耗时
- 首次设置阈值时，建议先运行 3-5 次取 P95 作为基准值

### 边界情况

- trace 中没有 `run_end` 事件：无法计算总耗时，断言失败
- 指定的 `phase` 工具未出现在 trace 中：无法计算耗时，断言失败
- 多工具调用取平均值，而非最大值

---

## 6. `output_schema` — 输出 Schema 断言 (V1.0)

### 功能描述

验证 Agent 的 `final_output` 是否符合指定的 JSON Schema。用于强制结构化输出格式。

### 适用场景

- 验证 JSON 格式输出符合预定义的 schema
- 验证 Markdown 报告包含所有必需章节
- 验证结构化数据的字段类型和约束

### target / condition 字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `target.field` | string | 否 | 要验证的输出字段。默认 `final_output` |
| `condition.schema` | object (JSON Schema) | 是 | JSON Schema 定义，遵循 JSON Schema Draft-07 |

### YAML 配置示例

```yaml
# 示例 1: 验证 JSON 输出结构
- id: valid-json-structure
  name: "Output matches expected JSON schema"
  type: output_schema
  target:
    field: final_output
  condition:
    schema:
      type: object
      required:
        - answer
        - sources
      properties:
        answer:
          type: string
          minLength: 1
        sources:
          type: array
          minItems: 1
          items:
            type: object
            required:
              - title
              - url
            properties:
              title:
                type: string
              url:
                type: string
                format: uri
```

### 最佳实践

- schema 定义应尽量精确（指定 `required`、`minLength`、`type` 等）
- 输出非 JSON 格式时，引擎尝试转换为 JSON 失败则断言失败
- JSON Schema Draft-07 是标准参考

### 边界情况

- `final_output` 不是 JSON 格式：尝试 `json.loads` 失败则断言失败
- schema 语法错误：引擎报配置错误，不静默失败
- 额外字段：默认不禁止额外字段，如需禁止需显式设置 `additionalProperties: false`

---

## 扩展: `custom_script` — 自定义检查脚本 (MVP/V1.0)

### 功能描述

当内置断言类型无法满足需求时，可以通过 `custom_script` 编写任意 Python 脚本来执行自定义检查。引擎通过子进程调用外部脚本，读取其 JSON 格式的 stdout 输出作为检查结果。

### 适用场景

- 需要调用外部 API 验证数据
- 需要复杂的跨工具推理逻辑
- 需要读取文件系统状态
- 需要集成第三方验证工具

### YAML 配置示例

```yaml
- id: custom-file-check
  name: "Custom file existence check"
  type: custom_script
  target:
    script_path: scripts/custom_checks/check_file_created.py
    script_args: "--output-dir /tmp/test-outputs"
    timeout: 30
  condition:
    # custom_script 的 condition 会通过 --condition 参数传给脚本
    expected_file: "result.csv"
```

### 脚本契约

自定义脚本必须遵循以下接口：

**输入**:
- `sys.stdin`: 完整 trace.jsonl 内容
- `--target`: JSON 字符串，对应 YAML 中的 `target` 字段
- `--condition`: JSON 字符串，对应 YAML 中的 `condition` 字段

**输出** (stdout, JSON):
```json
{
  "pass": true,
  "reason": null,
  "details": {
    "checked_file": "result.csv",
    "exists": true,
    "file_size_bytes": 1234
  }
}
```

**退出码**: 0（即使检查失败也返回 0，非 0 表示脚本本身执行异常）

### 最佳实践

- 脚本路径相对于 `scripts/custom_checks/` 目录解析
- 设置合理的 `timeout`（默认 30 秒），防止脚本挂起
- 自定义脚本应充分测试后再集成到断言套件中
- stdout 只输出最终结果 JSON，调试日志输出到 stderr

---

## 断言结果解读

每条断言执行后返回以下结构化结果：

```json
{
  "assertion_id": "at-least-one-search",
  "assertion_name": "Search tool was called at least once",
  "assertion_type": "tool_call",
  "pass": true,
  "reason": null,
  "details": {
    "actual": 3,
    "expected": {"min_count": 1},
    "tool_name": "web_search",
    "call_count": 3
  },
  "severity": "error"
}
```

失败时的 `reason` 字段示例：

| 断言类型 | 失败原因示例 |
|----------|-------------|
| `tool_call` | `Tool "web_search" was called 0 times, expected at least 1` |
| `tool_param` | `Parameter "query" for tool "web_search" is null` |
| `output_match` | `Pattern "Geoffrey Hinton" not found in final_output` |
| `path_sequence` | `Step "verification" missing, expected step order: planning → execution → verification` |
| `timing` | `Total execution time 85342ms exceeds max 60000ms` |
| `output_schema` | `Validation error: 'answer' is a required property` |
| `custom_script` | 由自定义脚本的 `reason` 字段指定 |

---

## 常见错误

| 错误 | 说明 | 修正 |
|------|------|------|
| 字段名拼写 | `max_count` 误写为 `max_countss` | 检查约定字符串清单 |
| 断言 ID 重复 | 同一文件中有两条 `id` 相同的断言 | 使用 `kebab-case` 加序号后缀 |
| 条件冲突 | 同时设置 `min_count: 1` 和 `exactly: 0` | 条件互斥时只在 YAML 中保留一个 |
| 正则未转义 | 在 YAML 字符串中未正确使用转义 | YAML 字符串用单引号包裹，正则中的反斜杠不需额外转义 |
| 大小写敏感 | `pattern: "hinton"` 未匹配 "Hinton" | 添加 `case_sensitive: false` |
