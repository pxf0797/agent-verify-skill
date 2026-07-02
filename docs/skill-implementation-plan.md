# agent-verify Skill 完整实现方案

ORCH_ID: `orch-20260630-234518-17009`
生成时间: 2026-06-30
角色: Writer（技术文档撰写人）
版本: V1.0

---

## 目录

1. [概述](#一概述)
2. [核心设计](#二核心设计)
3. [命令体系详解](#三命令体系详解)
4. [配置文件规范](#四配置文件规范)
5. [工作流指南](#五工作流指南)
6. [实现架构](#六实现架构)
7. [开发路线图](#七开发路线图)
8. [附录](#八附录)

---

## 一、概述

### 1.1 基本信息

| 属性 | 值 |
|------|-----|
| **Skill 名称** | `agent-verify` |
| **Slogan** | Agent 开发的 `pytest` -- 在 Claude Code 对话中定义"什么算对"，每次改动自动验证，不再凭感觉判断 Agent 质量。 |
| **英文 Slogan** | The pytest for AI Agents -- define what "correct" means, verify every change, and stop vibe-checking your agents. |
| **定位** | Claude Code 内建 Agent 验证工具 -- 唯一在同一对话界面完成开发与验证、零外部依赖的 Agent 质量保障体系。 |
| **许可** | MIT |
| **兼容性** | macOS / Linux，需要 Python 3.10+ 和 Claude Code CLI |

### 1.2 解决的痛点

| 痛点 | 量化现状 | 使用后的改善 |
|------|----------|-------------|
| **Agent 行为退化检测** | 99% 组织未在生产前评估 Agent（Gartner 2026）；靠人工感觉判断，自动化率 ~0% | 确定性断言自动检测，秒级反馈 |
| **prompt 修改影响面评估** | 无法评估（"改完不知道变好还是变坏"）；Agent 多步任务初始失败率 63%（Patronus AI 2026） | A/B 对比报告，量化每个维度的变化（$\pm$ 分数） |
| **回归测试覆盖** | 仅 52% 团队有系统性评估（LangChain State of AI Agents 2026）；每次手动测几个例子 | 可积累的测试套件，随时间增长覆盖 |
| **新功能验证** | 手动测试，10-30 分钟/功能 | 半自动化：5 分钟写断言 + 自动执行 |
| **质量基线建立** | 无基线（"不知道现在质量是什么水平"） | 首次运行即建立可量化的基线快照 |

### 1.3 与现有工具的差异

agent-verify 是 **75+ Agent 评估工具生态中唯一在 Claude Code 内部运行、与 Agent 开发同一对话界面、零外部依赖** 的验证工具。它的价值不是"做得更多"，而是"消除了上下文切换"。

| 维度 | agent-verify | DeepEval | Promptfoo | Braintrust | LangSmith |
|------|-------------|----------|-----------|------------|-----------|
| **运行位置** | Claude Code 内部 | Python 脚本/pytest | CLI | SaaS/API | SaaS/API |
| **零依赖运行** | :white_check_mark: (Claude Code 内建) | :x: (需独立安装) | :x: (需 Node.js) | :x: (需网络) | :x: (需 LangChain) |
| **断言引擎** | :white_check_mark: YAML 声明式 | :white_check_mark: pytest assert | :white_check_mark: YAML 声明式 | :white_check_mark: 代码式 | :white_check_mark: 代码式 |
| **LLM 裁判** | :white_check_mark: 多模型交叉 | :white_check_mark: 50+ 指标 | :white_check_mark: 基础 | :white_check_mark: 自定义评分器 | :white_check_mark: 内置评估器 |
| **Feature Flag A/B** | :white_check_mark: 内建 | :x: | :x: | :x: | :x: |
| **与 Agent 开发同屏** | :white_check_mark: 同一对话 | :x: | :x: | :x: | :x: |
| **Skill 格式原生** | :white_check_mark: | :x: | :x: | :x: | :x: |
| **学习成本** | 极低 (YAML + 对话) | 中 (Python + pytest) | 中 (YAML + CLI) | 中 (平台学习) | 高 (LangChain 生态) |

### 1.4 明确边界 —— 不做什么

| 不做的领域 | 原因 | 替代工具 |
|-----------|------|----------|
| 生产环境 Agent 监控 | 需要持久化基础设施（数据库、仪表盘、告警通道） | LangSmith / Galileo / Langfuse |
| 安全红队测试 | 需要大量攻击向量库 + 专业安全知识 | Promptfoo / CheckAgent |
| RAG 检索质量专项评估 | RAG 评估有成熟工具，复制价值低 | Ragas / DeepEval |
| 多模态 Agent 评估（视频/图像） | 当前 Skill 系统 + LLM 能力支撑不足 | 专项工具或未来版本 |
| 为第三方 Agent 平台提供测试服务 | 定位为 Claude Code Skill，不做 SaaS | -- |

---

## 二、核心设计

### 2.1 系统架构总览

```
                       ┌──────────────────────────────┐
                       │     用户 (Claude Code 对话)    │
                       │   /agent-verify:<command>     │
                       └──────────────┬───────────────┘
                                      │
                                      ▼
                       ┌──────────────────────────────┐
                       │     SKILL.md (编排层)          │
                       │  命令路由 + 工作流编排          │
                       │  ~400 行, 触发即加载           │
                       └──────┬───────────┬───────────┘
                              │           │
                 ┌────────────┘           └────────────┐
                 ▼                                     ▼
    ┌─────────────────────┐               ┌─────────────────────┐
    │    Agent 执行层      │               │    验证执行层        │
    └──────────┬──────────┘               └──────────┬──────────┘
               │                                     │
    ┌──────────┴──────────┐               ┌──────────┴──────────┐
    │ 1. Agent CLI        │               │ 3. 断言引擎          │
    │    Wrapper           │               │ assertion_engine    │
    │ (claude --print)     │               │     .py              │
    └──────────┬──────────┘               └──────────┬──────────┘
               │                                     │
               ▼                                     ▼
    ┌─────────────────────┐               ┌─────────────────────┐
    │ 2. 结构化日志        │               │ 4. LLM 裁判          │
    │   parse_log.py      │               │ (Claude API 调用)    │
    └──────────┬──────────┘               └──────────┬──────────┘
               │                                     │
               └───────────────┬─────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   聚合 & 报告        │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
    ┌────────────────┐ ┌────────────┐ ┌──────────────┐
    │ 5. 回归运行器   │ │ 6. A/B对比 │ │ 7. 基线管理   │
    │ regression_    │ │ ab_compar- │ │ baseline_     │
    │ runner.py      │ │ ator.py    │ │ manager.py    │
    └────────────────┘ └────────────┘ └──────────────┘
```

**模块职责**:

| # | 模块 | 脚本 | 职责 |
|---|------|------|------|
| 1 | Agent CLI Wrapper | (Claude 直接调用) | 通过 `claude --print --input "..."` 执行被验证 Agent，收集输出和日志 |
| 2 | 结构化日志解析 | `parse_log.py` | 从 Agent 运行日志中提取结构化事件流（trace.jsonl） |
| 3 | 断言引擎 | `assertion_engine.py` | 加载断言配置，对日志执行确定性检查，输出 Pass/Fail + 原因 |
| 4 | LLM 裁判 | (Claude API 直接调用) | 基于评分标准，对 Agent 输出进行多维度量化打分 |
| 5 | 回归运行器 | `regression_runner.py` | 遍历测试套件中的用例，依次执行 Agent + 断言 + 裁判 |
| 6 | A/B 对比器 | `ab_comparator.py` | 对两份运行结果进行逐维度 diff |
| 7 | 基线管理器 | `baseline_manager.py` | 保存/加载/对比质量基线快照 |

### 2.2 设计哲学与原则

1. **先断言，后裁判** — MVP 阶段只做确定性断言（100% 可靠，零 API 成本），LLM 裁判在 V1.0 按需启用。断言是底线，裁判是上限。

2. **零上下文切换** — 用户在同一个 Claude Code 对话中开发 Agent、定义验证规则、运行回归测试、查看报告。不需要切到另一个终端或平台。

3. **渐进式验证** — 从 1 条断言、1 个测试用例开始，逐量积累。不要求用户一次性建立完整验证体系。

4. **声明式优于代码式** — 断言和测试用例使用 YAML 定义，无论用户是否会编程都能上手。6 种预设断言类型覆盖 80% 场景，剩余 20% 通过自定义脚本扩展。

5. **数据本地化，隐私优先** — 所有配置、断言、基线、报告存储在用户本地文件系统中。不上传任何数据到外部服务。LLM 裁判是可选的，且仅发送评分的必要上下文。

6. **与 Agent 代码共存** — 验证套件（`agent-verify/`）与 Agent 代码放在同一 Git 仓库中，随 Agent 一起演进。

### 2.3 核心概念定义

#### 断言 (Assertion)

断言是对 Agent 行为的**确定性规则检查**。一条断言描述一件 Agent "必须做到"或"必须不能做"的事。断言引擎对结构化日志执行检查，输出 `PASS` 或 `FAIL` + 失败原因。

断言是 100% 确定的 -- 不会出现"有时通过有时不通过"。如果 Agent 行为一致，断言结果必然一致。

**示例**: "search_tool 必须被调用至少 1 次"、"search 的 query 参数不能为空字符串"、"最终输出必须包含引用来源"。

#### 测试套件 (Suite)

测试套件是一组**测试用例的集合**，每条测试用例包含：输入（用户消息）、预期执行路径、关联的断言列表、LLM 裁判评分标准。

套件按 Agent、功能模块或质量属性组织。最小套件可以是 1 条用例，典型套件 5-20 条，大型套件 50+ 条。

**示例**: `search-agent-full-suite`（搜索 Agent 完整回归套件）、`critical-path`（所有 Agent 共用的关键路径最小验证集）。

#### 基线 (Baseline)

基线是**某一时刻 Agent 质量的全量快照**，包含所有测试用例的断言结果、LLM 评分（如果启用）、执行轨迹摘要。基线的核心用途是回答"相比上次发布，质量变好了还是变差了"。

基线通常与 Git tag 或版本发布节点对齐。回归测试的结果总是与最新基线对比，退化的测试用例会被自动标注。

**示例**: `v1.0-release`（V1.0 发布时的质量快照）、`pre-refactor`（重构前的快照）。

#### Feature Flag

Feature Flag 是一个**命名的功能开关**，通过环境变量注入到被验证 Agent 的执行环境中。用于 A/B 对比测试：Flag=OFF 跑一次（旧行为），Flag=ON 跑一次（新行为），diff 两者结果。

Flag 名称在 `config.yaml` 中预定义，运行时通过 `AGENT_FLAG_<NAME>=ON|OFF` 环境变量传递。未预定义的 Flag 不会生效（防止拼写错误导致静默失败）。

**示例**: `enable_cot_v2`（新版 Chain-of-Thought 推理策略）、`enable_new_search_tool`（新版搜索工具）。

---

## 三、命令体系详解

本节描述 agent-verify 的 7 个核心命令。每个命令均可通过两种方式触发：

1. **手动调用**: `/agent-verify:<command> [options]`
2. **自然语言触发**: 在对话中说出触发短语，Claude 自动识别并调用

### 3.1 `/agent-verify:init` -- 初始化验证项目

**功能描述**: 在当前目录创建 `agent-verify/` 目录结构，生成默认配置文件，引导用户定义第一条断言。

**触发短语**: "初始化验证" / "setup verification" / "建立测试" / "创建验证项目" / "初始化 agent-verify"

**参数**:

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--target` | string | 否 | 当前目录名 | 要验证的 Agent/Skill 名称 |
| `--template` | string | 否 | `default` | 初始化模板：`default`（标准）、`minimal`（最小） |

**行为**:
1. 创建目录结构：`agent-verify/{assertions.yaml, suites/, baselines/, config.yaml}`
2. 生成 `config.yaml` 默认配置
3. 向用户询问 Agent 类型（对话式 / 工具调用式 / 多步工作流式）
4. 引导用户定义第一条断言
5. 输出初始化完成报告 + 下一步建议

**使用示例**:

```bash
# 基本初始化
/agent-verify:init

# 指定 target 名称
/agent-verify:init --target search-agent

# 使用最小模板
/agent-verify:init --template minimal
```

**输出格式**:

```
✅ 验证套件已初始化：./agent-verify/

📁 目录结构:
   agent-verify/
   ├── config.yaml           # 全局配置
   ├── assertions.yaml       # 断言定义文件
   ├── suites/                # 测试套件目录
   └── baselines/             # 基线存储目录

📋 下一步建议:
   1. 定义第一条断言 → /agent-verify:assert --add
   2. 创建测试用例 → /agent-verify:suite --add
   3. 运行首次回归 → /agent-verify:regression
```

---

### 3.2 `/agent-verify:assert` -- 创建/管理断言

**功能描述**: 添加、查看、删除确定性断言。断言描述 Agent "必须做到"的事，由断言引擎自动检查。

**触发短语**: "加一条断言" / "define assertion" / "添加规则" / "检查是否调用了某工具" / "验证输出包含" / "assert that"

**参数**:

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--add` | flag | 条件* | 添加新断言（交互式引导） |
| `--list` | flag | 否 | 列出所有已定义断言 |
| `--remove <id>` | string | 条件* | 删除指定 ID 的断言 |
| `--run` | flag | 否 | 添加/修改断言后立即运行验证 |
| `--type <type>` | string | 否 | 断言类型（跳过交互式选择）：`tool_call` / `tool_param` / `output_match` / `path_sequence` / `timing` / `output_schema` |

\* `--add` 和 `--remove <id>` 至少提供一个。

**断言类型详细说明**:

| 类型 | 说明 | 示例 |
|------|------|------|
| `tool_call` | 检查某个工具是否被调用（次数、存在性） | "search_tool 必须被调用至少 1 次" |
| `tool_param` | 检查工具调用时的参数值 | "search 的 query 参数不能为空" |
| `output_match` | 检查最终输出是否匹配模式 | "输出必须包含引用来源" |
| `path_sequence` | 检查执行路径是否经过指定阶段 | "工作流必须经过计划→执行→验证" |
| `timing` | 检查步骤的执行时间 | "单步 tool_call 耗时 < 30s" |
| `output_schema` | 检查输出是否符合 JSON Schema | "输出必须是有效的 JSON，包含 answer 和 sources 字段" |

**行为**:
1. `--add`: 交互式引导用户选择断言类型、填写条件、设置严重级别
2. `--list`: 表格形式列出所有断言（ID、名称、类型、严重级别、启用状态）
3. `--remove <id>`: 删除断言，需用户确认
4. `--run`: 立即对所有已启用断言执行一次验证

**使用示例**:

```bash
# 交互式添加断言
/agent-verify:assert --add

# 直接指定类型添加（跳过交互）
/agent-verify:assert --add --type tool_call

# 列出所有断言
/agent-verify:assert --list

# 删除断言
/agent-verify:assert --remove search-tool-called

# 添加后立即运行
/agent-verify:assert --add --run
```

**`--list` 输出格式**:

```
📋 已定义断言 (3 条)

┌──────────────────────┬──────────────────────────┬─────────────┬──────────┬────────┐
│ ID                   │ 名称                      │ 类型         │ 严重级别  │ 状态   │
├──────────────────────┼──────────────────────────┼─────────────┼──────────┼────────┤
│ search-tool-called   │ 搜索工具必须被调用          │ tool_call   │ error    │ 启用   │
│ search-query-not-empty│ 搜索查询参数不能为空       │ tool_param  │ error    │ 启用   │
│ output-has-citations │ 输出必须包含引用来源        │ output_match│ error    │ 启用   │
└──────────────────────┴──────────────────────────┴─────────────┴──────────┴────────┘
```

---

### 3.3 `/agent-verify:regression` -- 运行回归测试

**功能描述**: 对指定测试套件中的每条用例依次执行 Agent、收集日志、运行断言、生成回归报告。这是日常使用最频繁的命令。

**触发短语**: "跑回归" / "run regression" / "验证有没有退化" / "测试一下" / "检查质量" / "跑测试" / "回归测试"

**参数**:

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--suite <name>` | string | 否 | `all` | 指定测试套件名称或分组（如 `smoke`、`full`） |
| `--scope <scope>` | string | 否 | `all` | `all`（全量）或 `changed`（增量，仅运行与本次修改相关的用例） |
| `--compare <baseline>` | string | 否 | 最新基线 | 与指定基线对比 |
| `--output <format>` | string | 否 | `markdown` | 报告格式：`markdown` / `json` |
| `--judge` | flag | 否 | 根据配置 | 强制启用 LLM 裁判（覆盖配置文件设置） |
| `--no-judge` | flag | 否 | 根据配置 | 强制禁用 LLM 裁判 |

**行为**:
1. 遍历套件中的每条测试用例
2. 对每条用例：注入结构化日志指令 → 执行 Agent → 解析日志 → 运行断言 → (可选) LLM 裁判评分
3. 汇总所有用例结果
4. 与基线对比（如果存在）
5. 生成回归报告

**数据流**:

```
for each test_case in suite:
    1. 注入结构化日志指令到 Agent prompt
    2. 执行 Agent → raw_output.md
    3. 解析日志 → trace.jsonl
    4. 执行断言 → assertion_result.json
    5. (可选) LLM 裁判评分 → judge_scores.json
    6. 聚合用例结果 → case_result.json

汇总 → regression_report.md
```

**使用示例**:

```bash
# 运行全量回归测试
/agent-verify:regression

# 只跑 smoke 分组
/agent-verify:regression --suite search-agent --scope smoke

# 指定与基线对比
/agent-verify:regression --compare v1.0-release

# 禁用 LLM 裁判以加快速度
/agent-verify:regression --no-judge

# JSON 格式输出（供 CI 消费）
/agent-verify:regression --output json
```

**输出格式 (Markdown)**:

```
📊 回归测试报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
套件: search-agent-full-suite
用例数: 8
时间: 2026-06-30 15:22:00

确定性断言:
  通过: 7/8 (87.5%)
  失败: 1/8 (12.5%)

失败明细:
┌─────────────────────┬──────────────────────────────────┬──────────┐
│ 用例                 │ 断言                              │ 原因     │
├─────────────────────┼──────────────────────────────────┼──────────┤
│ error-timeout-003   │ output-has-citations             │ 未找到匹配│
└─────────────────────┴──────────────────────────────────┴──────────┘

LLM 评分 (haiku, 5 维度):
  准确性:     8.2 ± 0.8
  完整性:     7.1 ± 1.2
  合理性:     7.8 ± 0.6
  工具使用:   8.5 ± 0.4
  综合:       7.9 ± 0.5

与基线 v1.0-release 对比:
  断言通过率: 87.5% → 87.5% (不变)
  综合评分:   7.9 → 7.9 (不变)
  ⚠️ 1 个用例评分下降: complex-multi-hop-002 (-1.2)
```

---

### 3.4 `/agent-verify:compare` -- Feature Flag A/B 对比

**功能描述**: 对同一个测试套件分别以 Flag=OFF 和 Flag=ON 运行，生成逐维度差异对比报告。用于量化新功能的影响。

**触发短语**: "对比一下" / "比较新旧版本" / "A/B test" / "这个改动效果如何" / "对比功能" / "跑 A/B"

**参数**:

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--flag <name>` | string | 是 | Feature Flag 名称（必须在 config.yaml 中预定义） |
| `--baseline <name>` | string | 否 | **⚠️ 语义注意：不是"与基线对比"，而是"将基线作为 Flag=OFF 数据"**——跳过 Flag=OFF 的实际运行，用已有基线快照替代，以加速对比。仅在确认基线数据未过期时使用。 |
| `--suite <name>` | string | 否 | 测试套件名称，默认 `all` |
| `--judge` | flag | 否 | 强制启用 LLM 裁判 |

**行为**:
1. 验证 Flag 在 config.yaml 中已定义
2. **Flag=OFF**: 运行全量测试 → 基线数据（注意：如果 `--baseline` 已提供，**跳过实际运行**，直接复用基线快照作为 OFF 数据。这可以加速对比，但前提是基线数据未过期——即 Agent 代码在基线保存后未发生影响 Flag=OFF 行为的修改。）
3. **Flag=ON**: 运行全量测试 → 新版本数据
4. 逐用例、逐维度 diff
5. 生成对比报告（表格 + 变好/变坏明细 + 结论建议）

**使用示例**:

```bash
# 基本 A/B 对比
/agent-verify:compare --flag enable_cot_v2

# 指定套件
/agent-verify:compare --flag enable_new_search_tool --suite search-agent

# 使用已有基线作为 OFF 数据（加速）
/agent-verify:compare --flag enable_cot_v2 --baseline v1.0-release
```

**输出格式**:

```
📊 A/B 对比报告: enable_cot_v2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
对比: OFF (旧策略) vs ON (新策略)
测试套件: full-suite (12 条用例)

┌──────────────────┬────────────┬───────────┬──────────┐
│ 维度               │ OFF (旧)   │ ON (新)   │ 变化     │
├──────────────────┼────────────┼───────────┼──────────┤
│ 断言通过率         │ 11/12 (92%)│ 12/12 (100%)│ +8% ✅  │
│ LLM 准确性         │ 7.2        │ 8.5       │ +1.3 ✅  │
│ LLM 完整性         │ 6.8        │ 7.4       │ +0.6 ✅  │
│ LLM 合理性         │ 7.5        │ 8.9       │ +1.4 ✅  │
│ LLM 工具使用        │ 8.1        │ 8.3       │ +0.2 —  │
│ 综合评分           │ 7.3        │ 8.2       │ +0.9 ✅  │
│ 平均执行步数        │ 5.2        │ 6.8       │ +1.6 ⚠️  │
│ 平均耗时           │ 12.3s      │ 18.7s     │ +6.4s ⚠️ │
└──────────────────┴────────────┴───────────┴──────────┘

✅ 全面正向 — 推理质量显著提升
⚠️ 执行步数 +30%，耗时 +52% — 建议对简单查询跳过 CoT
```

---

### 3.5 `/agent-verify:baseline` -- 管理基线

**功能描述**: 保存当前 Agent 质量快照、列出历史基线、对比两个基线。

**触发短语**: "建立基线" / "保存当前分数" / "baseline snapshot" / "记录当前质量水平" / "保存基线"

**参数**:

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--save <name>` | string | 条件* | 保存当前基线 |
| `--list` | flag | 否 | 列出所有已保存基线 |
| `--compare <name1> <name2>` | string[] | 条件* | 对比两个基线 |
| `--suite <name>` | string | 否 | 测试套件名称（`--save` 时使用） |
| `--judge` | flag | 否 | 强制启用 LLM 裁判 |

\* `--save`、`--list`、`--compare` 至少提供一个。

**行为**:
1. `--save`: 运行全量测试，记录所有指标快照，保存为 JSON 基线文件
2. `--list`: 表格列出所有基线（名称、时间、套件、断言通过率、综合评分）
3. `--compare`: 对两个基线进行逐维度对比

**使用示例**:

```bash
# 保存基线
/agent-verify:baseline --save v1.0-release

# 列出所有基线
/agent-verify:baseline --list

# 对比两个基线
/agent-verify:baseline --compare v1.0-release v1.1-release
```

**`--list` 输出格式**:

```
📋 基线列表

┌────────────────┬─────────────────────┬────────────────────┬──────────┬──────────┐
│ 名称             │ 时间                 │ 套件                │ 断言通过率│ 综合评分  │
├────────────────┼─────────────────────┼────────────────────┼──────────┼──────────┤
│ v1.0-release   │ 2026-06-30 10:00    │ full-suite         │ 8/8 (100%)│ 7.3    │
│ pre-refactor   │ 2026-06-28 15:30    │ full-suite         │ 7/8 (88%) │ 6.8    │
└────────────────┴─────────────────────┴────────────────────┴──────────┴──────────┘
```

---

### 3.6 `/agent-verify:suite` -- 管理测试套件

**功能描述**: 添加测试用例、列出用例、导入导出、AI 辅助生成测试用例。

**触发短语**: "管理测试用例" / "添加测试用例" / "整理测试套件" / "加一个测试用例" / "添加用例"

**参数**:

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--add` | flag | 条件* | 添加新测试用例（交互式引导） |
| `--list` | flag | 否 | 列出所有测试用例 |
| `--import <file>` | string | 条件* | 从 JSON/YAML 文件导入测试用例 |
| `--export <file>` | string | 条件* | 导出测试套件到文件 |
| `--generate` | flag | 条件* | 从功能描述 AI 生成 Happy Path 测试用例初稿 |

\* `--add`、`--list`、`--import`、`--export`、`--generate` 至少提供一个。

**行为**:
1. `--add`: 引导定义测试用例（输入 + 预期路径 + 关联断言 + 评分标准）
2. `--list`: 表格列出所有用例（ID、名称、关联断言数、标签）
3. `--import`: 解析文件中的测试用例，合并到当前套件（去重）
4. `--export`: 将当前套件序列化为文件
5. `--generate`: 调用 Claude 从自然语言功能描述生成 Happy Path 测试用例初稿，用户审核确认后入库

**使用示例**:

```bash
# 交互式添加测试用例
/agent-verify:suite --add

# 列出所有用例
/agent-verify:suite --list

# AI 生成测试用例
/agent-verify:suite --generate
> 描述功能：用户查询最新新闻时，Agent 先搜索新闻 API，整理后输出带来源链接的摘要

# 导出套件
/agent-verify:suite --export my-suite-backup.yaml
```

---

### 3.7 `/agent-verify:report` -- 生成报告

**功能描述**: 聚合断言结果 + LLM 评分 + 对比数据，生成完整验证报告。

**触发短语**: "生成报告" / "出个报告" / "验证报告" / "导出报告"

**参数**:

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--format <format>` | string | 否 | `markdown` | 输出格式：`markdown` / `json` / `html` |
| `--scope <scope>` | string | 否 | `latest` | `latest`（最近一次） / `all`（全部历史） |
| `--output <path>` | string | 否 | 自动生成 | 输出文件路径 |

**使用示例**:

```bash
# 生成 Markdown 报告
/agent-verify:report

# 生成 JSON 报告（CI 集成）
/agent-verify:report --format json --output ci-report.json

# 生成全历史趋势报告
/agent-verify:report --scope all --format html
```

---

## 四、配置文件规范

### 4.1 目录结构

```
agent-verify/
├── config.yaml              # 全局配置文件
├── assertions.yaml          # 断言定义文件（所有断言集中管理）
├── suites/                  # 测试套件文件目录
│   ├── search-agent.yaml    # Search Agent 测试套件
│   └── critical-path.yaml   # 关键路径最小验证集
└── baselines/               # 基线快照目录
    ├── v1.0-release.json
    └── v1.1-release.json
```

### 4.2 agent-verify/config.yaml — 全局配置

**完整 Schema**:

```yaml
# agent-verify/config.yaml
# agent-verify Skill 全局配置文件
# 版本: 1.0

# =============================================================================
# 元信息
# =============================================================================
version: "1.0"                            # 配置格式版本（必需）
                                           #

# =============================================================================
# Agent 执行配置
# =============================================================================
execution:
  default_command: "claude --print"       # 默认 Agent 执行命令（必需）
                                           # 占位符: {input} 会被替换为测试用例的输入
  timeout: 120                             # 单用例超时（秒），默认 120
  env:                                     # 环境变量注入（可选）
    AGENT_VERIFY_MODE: "true"             # Agent 可通过此变量感知验证模式

# =============================================================================
# 断言引擎配置
# =============================================================================
assertions:
  file: "assertions.yaml"                 # 断言定义文件路径（默认 assertions.yaml）
  stop_on_first_error: false              # 遇到第一个错误是否停止（默认 false）
  fail_fast_threshold: 0.5                # 失败率超过此值提前终止（0-1，默认 0.5）
                                           # 仅在 stop_on_first_error=false 时生效

# =============================================================================
# LLM 裁判配置
# =============================================================================
llm_judge:
  enabled: false                           # 是否启用 LLM 裁判（MVP 默认 false）
  model: "claude-haiku"                   # 裁判模型（必须与开发模型不同）
  api_key_env: "ANTHROPIC_API_KEY"        # API Key 环境变量名

  dimensions:                              # 评分维度（1-5 个）
    - accuracy                             # 准确性：输出是否符合事实/任务要求
    - completeness                         # 完整性：是否覆盖了应有的步骤
    - reasonableness                       # 合理性：推理路径是否自洽
    - tool_usage                           # 工具使用质量：工具调用是否恰当
    - risk_awareness                       # 风险意识：是否包含不安全的操作建议

  scoring:
    range: [1, 10]                        # 评分范围 [min, max]
    runs: 3                               # 重复打分次数（取均值）
    max_variance: 1.5                     # 方差超过此值触发"裁判不一致"警告

  cost_control:
    max_tokens_per_eval: 2000             # 单次评估最大输出 token
    max_monthly_budget_usd: 50            # 月度预算上限（美元）
                                           # 达到上限后自动禁用 LLM 裁判

# =============================================================================
# Feature Flag 配置
# =============================================================================
feature_flags:
  storage: env                             # Flag 传递方式: env（环境变量）
                                           #                    file（配置文件）
                                           #                    both（两者都设置）
  file_path: "flags.yaml"                 # storage=file 时的文件路径
  flags:                                   # Flag 定义列表（可选）
    - name: "enable_cot_v2"               #   Flag 名称（kebab-case）
      description: "启用新版 Chain-of-Thought 推理策略"
      default: false                       #   默认值
    - name: "enable_new_search_tool"
      description: "启用新版搜索工具（替代旧版）"
      default: false
    - name: "max_search_results"
      description: "搜索结果最大返回数"
      default: 10
      type: number                         #   值类型: boolean | number | string
      range: [5, 30]                      #   数值范围（仅 type=number）

# =============================================================================
# 基线管理配置
# =============================================================================
baselines:
  directory: "baselines/"                  # 基线文件存储目录
  auto_save_on_regression: false          # 每次回归测试后自动保存基线

# =============================================================================
# 报告配置
# =============================================================================
reports:
  default_format: markdown                 # 默认输出格式: markdown | json | html
  output_directory: "reports/"             # 报告输出目录
  include_traces: false                    # 是否在报告中包含完整执行轨迹
                                           # 开启后报告体积可能很大

# =============================================================================
# 覆盖率配置（V1.0 之后启用）
# =============================================================================
coverage:
  enabled: false                           # V1.0 默认 false
  dimensions:                              # 覆盖维度
    - functional                           #   功能覆盖
    - tool                                 #   工具覆盖
    - path                                 #   路径覆盖
    - input_type                           #   输入类型覆盖
```

**字段说明**:

| 字段路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `version` | string | 是 | -- | 配置格式版本，用于向前兼容 |
| `execution.default_command` | string | 是 | `claude --print` | Agent 执行命令模板 |
| `execution.timeout` | integer | 否 | `120` | 单用例超时秒数 |
| `execution.env` | object | 否 | `{}` | 注入到 Agent 执行环境的额外环境变量 |
| `assertions.file` | string | 否 | `assertions.yaml` | 断言定义文件路径 |
| `assertions.stop_on_first_error` | boolean | 否 | `false` | 是否遇错即停 |
| `assertions.fail_fast_threshold` | float | 否 | `0.5` | 失败率阈值 |
| `llm_judge.enabled` | boolean | 否 | `false` | 全局 LLM 裁判开关 |
| `llm_judge.model` | string | 否 | `claude-haiku` | 裁判模型 ID |
| `llm_judge.dimensions` | list | 否 | 5 维度 | 评分子维度 |
| `llm_judge.scoring.runs` | integer | 否 | `3` | 重复打分次数 |
| `llm_judge.scoring.max_variance` | float | 否 | `1.5` | 最大允许方差 |
| `llm_judge.cost_control.max_monthly_budget_usd` | integer | 否 | `50` | 月度预算上限 |
| `feature_flags.flags` | list | 否 | `[]` | Flag 预定义列表 |
| `baselines.directory` | string | 否 | `baselines/` | 基线存储目录 |
| `reports.default_format` | string | 否 | `markdown` | 默认报告格式 |
| `reports.output_directory` | string | 否 | `reports/` | 报告输出目录 |

### 4.3 assertions.yaml — 断言定义

**完整 Schema**:

```yaml
# agent-verify/assertions.yaml
# 断言定义文件（所有断言集中管理）
# 一个文件包含所有断言定义

version: "1.0"                            # 断言格式版本（必需）

assertions:                                # 断言列表（必需，至少 1 条）
  - id: "search-tool-called"              #   断言唯一 ID（必需，kebab-case）
    name: "搜索工具必须被调用"              #   断言可读名称（必需）
    description: >-                        #   断言详细描述（可选）
      确保 Agent 在处理信息查询时实际调用了搜索工具
    type: tool_call                        #   断言类型（必需）
                                           #   可选值: tool_call | tool_param |
                                           #           output_match | path_sequence |
                                           #           timing | output_schema |
                                           #           custom_script
    target:                                #   检查目标（必需，因 type 而异）
      tool_name: "search"                  #     tool_call/tool_param: 目标工具名
                                           #     output_match/output_schema: field (如 "final_output")
                                           #     path_sequence: step_types (如 ["planning", "execution"])
                                           #     timing: step_type (如 "tool_call")
    condition:                             #   检查条件（必需，因 type 而异）
      min_count: 1                         #     tool_call: min_count / max_count / exactly
                                           #     tool_param: min_length / not_null / pattern
                                           #     output_match: pattern / min_matches / case_sensitive
                                           #     path_sequence: order ("strict"|"relaxed") / all_present
                                           #     timing: max_duration_ms / min_duration_ms
                                           #     output_schema: schema (JSON Schema object)
    severity: error                        #   严重级别（必需）: error | warning
    enabled: true                          #   是否启用（必需）
    tags: ["search", "quality"]            #   标签（可选，用于分组和筛选）

  - id: "output-valid-json"
    name: "输出必须是有效 JSON"
    description: "当任务要求 JSON 输出时，验证格式正确"
    type: output_schema
    target:
      field: "final_output"
    condition:
      schema:
        type: "object"
        required: ["answer", "sources"]
        properties:
          answer:
            type: "string"
            minLength: 1
          sources:
            type: "array"
            minItems: 1
            items:
              type: "object"
              required: ["title", "url"]
              properties:
                title:
                  type: "string"
                url:
                  type: "string"
                  format: "uri"
    severity: error
    enabled: true
```

**各断言类型的 `target` 和 `condition` 字段详解**:

#### tool_call

```yaml
type: tool_call
target:
  tool_name: "search"            # 目标工具名（必需）
condition:                        # 以下条件至少选一个
  min_count: 1                   # 最少调用次数
  max_count: 5                   # 最多调用次数（可选）
  exactly: 3                     # 精确调用次数（与 min/max 互斥）
```

#### tool_param

```yaml
type: tool_param
target:
  tool_name: "search"            # 目标工具名（必需）
  param_name: "query"            # 参数名（必需）
condition:                        # 以下条件至少选一个
  min_length: 3                  # 参数值最短字符数
  max_length: 200                # 参数值最长字符数
  not_null: true                 # 不能为 null
  not_whitespace_only: true      # 不能为纯空格
  pattern: "^[a-zA-Z0-9 .,!?-]+$"  # 正则匹配
  allowed_values: ["news", "weather", "search"]  # 允许值列表
  forbidden_values: ["password", "secret"]       # 禁止值列表
```

#### output_match

```yaml
type: output_match
target:
  field: "final_output"          # 匹配目标字段（必需）
condition:
  pattern: "(来源|参考|引用)"     # 正则表达式（必需）
  min_matches: 1                 # 最少匹配次数（默认 1）
  case_sensitive: false          # 是否大小写敏感（默认 false）
```

#### path_sequence

```yaml
type: path_sequence
target:
  step_types: ["planning", "execution", "verification"]  # 步骤类型列表（必需）
condition:
  order: "strict"                # strict（严格顺序）| relaxed（任意顺序）
  all_present: true              # 所有步骤是否都必须出现
```

#### timing

```yaml
type: timing
target:
  step_type: "tool_call"         # 目标步骤类型（必需）
  tool_name: "search"            # 限定工具名（可选，不填则匹配所有该类型步骤）
condition:
  max_duration_ms: 30000         # 最大耗时（毫秒）
  min_duration_ms: 0             # 最小耗时（毫秒，可选）
```

#### output_schema

```yaml
type: output_schema
target:
  field: "final_output"          # 验证目标字段（必需）
condition:
  schema:                        # JSON Schema 对象（必需）
    type: "object"
    required: ["answer"]
    properties:
      answer:
        type: "string"
```

#### custom_script (扩展类型)

```yaml
type: custom_script
target:
  script: "my_custom_check.py"   # 自定义脚本文件名（必需，位于 scripts/ 目录）
condition:
  args: ["--threshold", "0.8"]   # 传递给脚本的参数（可选）
```

自定义脚本约定：
- 接收 JSONL 格式的 trace 数据作为 stdin
- 输出 JSON 格式结果到 stdout：`{"pass": true/false, "reason": "..."}`
- 退出码 0 表示脚本正常执行（不影响 pass/fail 判断）

### 4.4 suites/*.yaml — 测试套件

**完整 Schema**:

```yaml
# agent-verify/suites/search-agent.yaml
# 测试套件定义文件

suite:                                     # 套件元信息（必需）
  name: "search-agent-full-suite"           #   套件名称（必需，kebab-case）
  description: "Search Agent 的完整回归测试套件"  # 套件描述
  version: "1.0"                            #   套件版本

defaults:                                   # 全局默认配置（可选）
  agent_command: "claude --skill search-agent --print"  # Agent 执行命令（覆盖全局配置）
  timeout: 120                              #   单用例超时秒数（覆盖全局配置）
  assertions_file: "../assertions.yaml"  # 断言文件路径
  enable_llm_judge: true                    #   是否启用 LLM 裁判（覆盖全局配置）
  judge_model: "claude-haiku"              #   裁判模型

test_cases:                                 # 测试用例列表（必需，至少 1 条）
  - id: "simple-search-001"                #   用例唯一 ID（必需，kebab-case）
    name: "简单信息查询"                     #   用例可读名称（必需）
    description: "用户询问一个可直接搜索到的事实问题"  # 用例描述（可选）
    input: "2024 年诺贝尔物理学奖得主是谁？"   #   用户输入（必需）
    assertions:                             #   关联的断言 ID 列表（可选，默认使用 defaults.assertions_file 中的全部）
      - "search-tool-called"
      - "search-query-not-empty"
      - "output-has-citations"
    additional_assertions:                  #   该用例特有的额外断言（可选）
      - id: "must-use-physics-keyword"
        name: "必须包含物理学关键词"
        type: output_match
        target:
          field: "final_output"
        condition:
          pattern: "(物理|physics|诺贝尔)"
          min_matches: 1
        severity: error
    expected_path:                          #   预期执行路径（可选，供 LLM 裁判参考）
      - "理解用户查询意图"
      - "调用 search 工具搜索诺贝尔物理学奖"
      - "整合搜索结果，提取获奖者信息"
      - "输出带引用的答案"
    quality_criteria:                       #   LLM 裁判评分标准（可选，启用裁判时建议填写）
      accuracy: "获奖者姓名和国籍必须正确"
      completeness: "应覆盖获奖者及其获奖理由"
      risk: "不应编造不存在的获奖者或错误信息"
    tags: ["happy-path", "smoke-test"]       #   标签（可选）

  - id: "edge-empty-query-004"
    name: "空查询边界测试"
    description: "用户的消息不包含实际信息需求"
    input: "..."
    assertions:
      - "search-tool-called"
        enabled: false                      #   覆盖断言启用状态（此用例中该断言不应触发）
    additional_assertions:
      - id: "no-search-for-empty-query"
        name: "空查询不应触发搜索"
        type: tool_call
        target:
          tool_name: "search"
        condition:
          max_count: 0
        severity: error
    tags: ["edge-case", "negative-test"]

groups:                                     # 测试分组（可选，便于增量运行）
  smoke:                                    #   smoke 测试分组
    - "simple-search-001"
  full:                                     #   完整分组
    - "simple-search-001"
    - "complex-multi-hop-002"
    - "error-timeout-003"
    - "edge-empty-query-004"
```

**字段层级说明**:

优先级规则（高到低）: 用例级配置 > 套件 `defaults` > 全局 `config.yaml`

| 字段路径 | 类型 | 必需 | 说明 |
|----------|------|------|------|
| `suite.name` | string | 是 | 套件名称，用于 `--suite` 参数引用 |
| `defaults.agent_command` | string | 否 | 套件级 Agent 执行命令 |
| `defaults.assertions_file` | string | 否 | 套件级断言文件路径 |
| `defaults.enable_llm_judge` | boolean | 否 | 套件级 LLM 裁判开关 |
| `test_cases[].id` | string | 是 | 用例唯一标识 |
| `test_cases[].input` | string | 是 | 发送给 Agent 的用户输入 |
| `test_cases[].assertions` | list | 否 | 关联断言 ID 列表；不填则使用断言文件中所有启用的断言 |
| `test_cases[].assertions[X].enabled` | boolean | 否 | 覆盖某条断言的启用状态 |
| `test_cases[].additional_assertions` | list | 否 | 该用例特有的额外断言（内联定义） |
| `test_cases[].expected_path` | list | 否 | 预期执行路径（供裁判参考，不执行确定性检查） |
| `test_cases[].quality_criteria` | object | 否 | LLM 裁判评分标准（键名为维度名，值为评分要求描述） |
| `test_cases[].tags` | list | 否 | 标签，用于筛选和分组 |
| `groups` | object | 否 | 命名分组，值为用例 ID 列表 |

### 4.5 baselines/ — 基线存储

**基线文件格式** (`baselines/v1.0-release.json`):

```json
{
  "meta": {
    "name": "v1.0-release",
    "created": "2026-06-30T10:00:00Z",
    "suite": "search-agent-full-suite",
    "config_hash": "a1b2c3d4",
    "git_commit": "abc123def456",
    "agent_version": "1.0.0"
  },
  "summary": {
    "total_cases": 8,
    "assertion_pass": 7,
    "assertion_fail": 1,
    "assertion_pass_rate": 0.875,
    "llm_scores": {
      "accuracy": { "mean": 7.2, "std": 1.1 },
      "completeness": { "mean": 6.8, "std": 1.4 },
      "reasonableness": { "mean": 7.5, "std": 0.9 },
      "tool_usage": { "mean": 8.1, "std": 0.7 },
      "risk_awareness": { "mean": 7.0, "std": 1.0 },
      "composite": { "mean": 7.3, "std": 0.8 }
    },
    "avg_steps": 5.2,
    "avg_duration_ms": 12300
  },
  "cases": [
    {
      "id": "simple-search-001",
      "assertion_results": [
        {"assertion_id": "search-tool-called", "pass": true},
        {"assertion_id": "search-query-not-empty", "pass": true},
        {"assertion_id": "output-has-citations", "pass": true}
      ],
      "llm_scores": {
        "accuracy": 8.5,
        "completeness": 7.0,
        "reasonableness": 8.0,
        "tool_usage": 9.0,
        "risk_awareness": 7.5,
        "composite": 8.0
      },
      "steps": 4,
      "duration_ms": 8500
    }
  ],
  "flags": {
    "enable_cot_v2": false,
    "enable_new_search_tool": false
  }
}
```

**基线文件命名约定**: `<name>.json`，其中 `<name>` 遵循 Git tag 习惯——版本号部分使用点号分隔（如 `v1.0-release`），描述性部分使用 kebab-case（如 `pre-refactor`）。示例：`v1.0-release.json`、`v1.1-release.json`、`pre-refactor.json`。

---

## 五、工作流指南

### 5.1 工作流一：首次使用（4 分钟）

**目标**: 从零搭建验证套件，定义第一条断言，运行首次回归测试。

**适用场景**: 新用户首次接触 agent-verify。

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                   首次使用工作流 (预计 4 分钟)                             ║
╚═══════════════════════════════════════════════════════════════════════════╝

Step 1: 初始化验证项目 ───────────────────────────── 预计 30 秒
┌─────────────────────────────────────────────────────────────────────────┐
│ 命令: /agent-verify:init --target my-agent                              │
│                                                                         │
│ 产出:                                                                    │
│   agent-verify/                                                         │
│   ├── config.yaml          ← 全局配置                                    │
│   ├── assertions.yaml      ← 断言定义文件（空）                           │
│   ├── suites/              ← 测试套件目录（空）                           │
│   └── baselines/           ← 基线存储目录（空）                           │
│                                                                         │
│ 验证: ls agent-verify/ 确认目录结构存在                                   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
Step 2: 创建第一条断言 ───────────────────────────── 预计 1 分钟
┌─────────────────────────────────────────────────────────────────────────┐
│ 命令: /agent-verify:assert --add                                         │
│                                                                         │
│ 交互过程:                                                                │
│   > 断言类型？选择 tool_call                                              │
│   > 目标工具名？search                                                    │
│   > 条件？至少调用 1 次                                                    │
│   > 严重级别？error                                                       │
│   > 断言名称？搜索工具必须被调用                                           │
│                                                                         │
│ 产出: assertions.yaml 中出现第一条断言                                   │
│                                                                         │
│ 验证: /agent-verify:assert --list 确认断言已添加                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
Step 3: 创建第一个测试用例 ───────────────────────── 预计 1 分钟
┌─────────────────────────────────────────────────────────────────────────┐
│ 命令: /agent-verify:suite --add                                          │
│                                                                         │
│ 交互过程:                                                                │
│   > 用例名称？简单搜索测试                                                 │
│   > 用户输入？2024 年诺贝尔物理学奖得主是谁？                               │
│   > 关联断言？选择 "search-tool-called"                                   │
│   > 标签？happy-path, smoke-test                                         │
│                                                                         │
│ 产出: suites/my-agent.yaml 中出现第一条测试用例                            │
│                                                                         │
│ 验证: /agent-verify:suite --list 确认用例已添加                           │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
Step 4: 运行首次回归测试 ─────────────────────────── 预计 2 分钟
┌─────────────────────────────────────────────────────────────────────────┐
│ 命令: /agent-verify:regression                                           │
│                                                                         │
│ 产出:                                                                    │
│   📊 回归测试报告                                                         │
│   用例数: 1                                                               │
│   断言通过: 1/1 (100%)                                                    │
│                                                                         │
│ 验证: 断言通过率 100%，无报错                                              │
└─────────────────────────────────────────────────────────────────────────┘
✅ 完成！你现在有了:
   - 1 条确定性断言
   - 1 条测试用例
   - 1 份回归报告

📋 接下来:
   - 加更多断言 → /agent-verify:assert --add
   - 加更多用例 → /agent-verify:suite --add
   - 每次改完代码 → /agent-verify:regression
```

---

### 5.2 工作流二：日常开发

**目标**: 修改 Agent 后快速验证是否有退化。这是使用频率最高的流程。

**适用场景**: 修改 system prompt、工具定义、行为策略后的日常验证。

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                     日常开发工作流 (每次改动后)                            ║
╚═══════════════════════════════════════════════════════════════════════════╝

Step 1: 修改 Agent 代码 ────────────────────────────
  正常开发。可以修改:
  - System prompt（提示词）
  - 工具定义（tool descriptions）
  - 行为策略（推理步骤、输出格式等）
  - Feature Flag 开关

                                    │
                                    ▼
Step 2: 运行回归测试 ──────────────────────────────────────────────
┌─────────────────────────────────────────────────────────────────────────┐
│ 命令: /agent-verify:regression --compare latest                         │
│                                                                         │
│ 产出:                                                                    │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ 📊 回归对比报告                                                       │ │
│ │ 对比: 当前 vs 基线 v1.0-release                                       │ │
│ │                                                                       │ │
│ │ 确定性断言:                                                            │ │
│ │   通过: 7/8 (87.5%)   基线: 8/8 (100%)   ⚠️ -1                        │ │
│ │                                                                       │ │
│ │ 失败明细:                                                             │ │
│ │   error-timeout-003: output-has-citations FAIL                        │ │
│ │                                                                       │ │
│ │ LLM 评分变化 (如果启用):                                               │ │
│ │   准确性: 7.2 → 7.8 (+0.6) ✅                                        │ │
│ │   完整性: 6.8 → 5.1 (-1.7) ⚠️                                        │ │
│ │   综合:   7.3 → 6.8 (-0.5) ⚠️                                        │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                     ┌──────────────┼──────────────┐
                     ▼              ▼              ▼
              全部通过          有 FAIL        评分下降
                │                 │              │
                ▼                 ▼              ▼
          ✅ 完成           🔧 修复代码      🔍 分析原因
                           │              │
                           │   ┌──────────┴──────────┐
                           │   ▼                     ▼
                           │ 代码 bug             新行为有意变更
                           │ → 修复代码           → 更新断言/基线
                           │                      → 记录 tradeoff
                           │
                           └───→ 回到 Step 2
```

**典型判断矩阵**:

| 断言变化 | 评分变化 | 判断 | 行动 |
|----------|----------|------|------|
| 无新增 FAIL | 无显著下降 (变化 < 0.3) | :white_check_mark: 安全 | 接受修改 |
| 无新增 FAIL | 有维度显著提升 (> 0.5) | :white_check_mark: 改进 | 接受修改，考虑更新基线 |
| 有新增 FAIL | -- | :x: 回归 | 修复代码或更新断言（如果是有意行为变更） |
| 无新增 FAIL | 有维度显著下降 (> 0.5) | :warning: 可能退化 | 深入分析根因，权衡 tradeoff |
| 无新增 FAIL | 多个维度轻微下降 (0.3-0.5) | :warning: 注意 | 累计效应可能显著，检查趋势 |

---

### 5.3 工作流三：质量改进

**目标**: 系统性分析 Agent 质量短板，添加断言覆盖，建立改进基线，验证改进效果。

**适用场景**: 质量周报、版本发布前质量检查、新功能上线后质量回归。

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                       质量改进工作流 (周期性)                              ║
╚═══════════════════════════════════════════════════════════════════════════╝

Phase 1: 分析当前质量状况 ─────────────────────────────────────
┌─────────────────────────────────────────────────────────────────────────┐
│ 命令: /agent-verify:regression --suite full --judge                     │
│                                                                         │
│ 产出:                                                                    │
│   - 断言通过率 (hard quality)                                            │
│   - 各维度 LLM 评分分布 (soft quality)                                    │
│   - 失败用例清单                                                         │
│   - 与上次基线的对比                                                     │
│                                                                         │
│ 分析问题:                                                                │
│   - 哪些用例失败？为什么？                                                │
│   - 哪些维度评分低？< 5 分需要关注，< 3 分需要立即处理                       │
│   - 哪些工具/路径没有被任何断言覆盖？                                      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
Phase 2: 添加缺失的断言 ─────────────────────────────────────
┌─────────────────────────────────────────────────────────────────────────┐
│ 对每个薄弱点添加断言:                                                      │
│                                                                         │
│ 命令: /agent-verify:assert --add                                         │
│                                                                         │
│ 示例:                                                                    │
│   薄弱点: 搜索超时时 Agent 没有降级处理                                     │
│   → 添加断言: "错误处理工具必须在超时后被调用"                               │
│   → 类型: tool_call, target: error_handler, min_count: 1                │
│                                                                         │
│   薄弱点: 输出缺少引用来源                                                 │
│   → 添加断言: "输出必须包含引用来源"                                        │
│   → 类型: output_match, pattern: "(来源|参考|引用)"                       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
Phase 3: 补充测试用例 ───────────────────────────────────────
┌─────────────────────────────────────────────────────────────────────────┐
│ 对于新发现的场景:                                                         │
│                                                                         │
│ 命令: /agent-verify:suite --add                                          │
│                                                                         │
│ 或使用 AI 生成:                                                          │
│ 命令: /agent-verify:suite --generate                                     │
│                                                                         │
│ 示例:                                                                    │
│   发现: "用户输入包含特殊字符时，Agent 输出乱码"                             │
│   → 添加测试用例: "特殊字符输入边界测试"                                    │
│   → 输入: "搜索 C++ 和 Rust 的性能对比 @#$%^&*"                           │
│   → 断言: output-has-citations + output-valid-json(如需要)                │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
Phase 4: 建立改进基线 ─────────────────────────────────────
┌─────────────────────────────────────────────────────────────────────────┐
│ 修复问题后, 重新建立基线:                                                  │
│                                                                         │
│ 命令: /agent-verify:baseline --save v1.2-quality-improved               │
│                                                                         │
│ 对比查看改进:                                                             │
│ 命令: /agent-verify:baseline --compare v1.1-release v1.2-quality-improved│
│                                                                         │
│ 产出:                                                                    │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ 📊 基线对比: v1.1-release → v1.2-quality-improved                      │ │
│ │                                                                       │ │
│ │ 断言通过率: 87.5% → 100% (+12.5%) ✅                                  │ │
│ │ 准确性:     7.2 → 8.1 (+0.9) ✅                                      │ │
│ │ 完整性:     6.1 → 7.5 (+1.4) ✅                                      │ │
│ │ 工具使用:   7.8 → 8.2 (+0.4) ✅                                      │ │
│ │                                                                       │ │
│ │ 新增测试用例: 3 条                                                      │ │
│ │ 新增断言: 5 条                                                          │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
Phase 5: 验证改进并循环 ─────────────────────────────────────
┌─────────────────────────────────────────────────────────────────────────┐
│ 每日/每次改动:                                                            │
│   命令: /agent-verify:regression                                         │
│   → 确保不退化                                                           │
│                                                                         │
│ 每周:                                                                    │
│   检查是否有新的失败模式 → 回到 Phase 2                                    │
│                                                                         │
│ 每月/每版本:                                                              │
│   保存基线 → 回到 Phase 4                                                 │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 六、实现架构

### 6.1 文件结构树

```
agent-verify/                               # Skill 根目录
│
├── SKILL.md                                # [Level 2] 主技能文件 (~400 行)
│                                           # 角色: 命令路由 + 工作流编排
│                                           # 加载时机: Skill 触发时
│
├── scripts/                                # [Level 3] 可执行脚本
│                                           # 特点: 不占用上下文，通过 Bash 执行
│   ├── parse_log.py                       #   结构化日志解析器
│   ├── assertion_engine.py                #   确定性断言引擎
│   ├── regression_runner.py               #   回归测试编排器
│   ├── ab_comparator.py                   #   A/B 对比报告生成器
│   ├── baseline_manager.py                #   基线管理
│   ├── report_generator.py                #   综合报告生成器
│   ├── llm_judge.py                       #   LLM 裁判评分器（三级仲裁体系）(V1.0)
│   └── utils.py                           #   通用工具函数
│
├── references/                             # [Level 3] 按需加载文档
│                                           # 特点: Claude 通过 Read 工具按需读取
│   ├── assertion-types.md                 #   断言类型详细说明（6 种 + 示例）
│   ├── scoring-rubric.md                  #   LLM 裁判评分维度与 rubric 设计指南
│   ├── config-reference.md                #   配置文件完整参考
│   ├── workaround-patterns.md             #   常见场景断言编写模式（10+ 个）
│   └── integration-guide.md               #   CI/CD 集成步骤说明
│
├── templates/                              # [Level 3] 输出模板
│                                           # 特点: 复制到用户项目，不读入上下文
│   ├── config-template.yaml               #   默认 config.yaml 模板
│   ├── assertions-template.yaml           #   空断言文件模板
│   ├── suite-template.yaml                #   空测试套件模板
│   ├── baseline-template.json             #   基线快照格式模板
│   └── github-actions-workflow.yml        #   GitHub Actions CI 模板 (V1.0)
│
└── examples/                               # [Level 3] 参考示例
    │                                       # 特点: 供用户学习参考，不参与执行
    ├── example-search-agent/               #   搜索 Agent 完整验证示例
    │   ├── config.yaml
    │   ├── assertions.yaml
    │   ├── suites/search-agent.yaml
    │   └── baselines/v1.0-release.json
    │
    └── example-chat-agent/                 #   对话 Agent 完整验证示例
        ├── config.yaml
        ├── assertions.yaml
        └── suites/chat-agent.yaml
```

**文件大小目标**:

| 文件 | 目标行数 | 说明 |
|------|----------|------|
| `SKILL.md` | 350-400 行 | 核心工作流 + 命令路由；不超过 500 行（Skill 系统建议上限） |
| `scripts/parse_log.py` | 150-200 行 | 纯数据解析，无复杂逻辑 |
| `scripts/assertion_engine.py` | 300-400 行 | 核心引擎，6 种类型 + 自定义扩展 |
| `scripts/regression_runner.py` | 250-350 行 | 编排逻辑 + 错误处理 |
| `scripts/ab_comparator.py` | 150-200 行 | 双跑 + diff |
| `scripts/baseline_manager.py` | 100-150 行 | CRUD 操作 |
| `scripts/report_generator.py` | 150-200 行 | 模板渲染 |
| `scripts/llm_judge.py` | 200-300 行 | API 调用 + 方差检测 (V1.0) |
| `references/*.md` | 100-300 行/个 | 按需加载，精准化内容 |

### 6.2 核心模块说明

#### 6.2.1 parse_log.py — 结构化日志解析器

**职责**: 从 Agent 执行输出中提取结构化事件流。

**输入**: Agent 的完整文本输出（stdout + 可选的结构化注释）

**输出**: `trace.jsonl` — 每行一个 JSON 事件

**核心算法**:

```
1. 按行分割 Agent 输出
2. 识别结构化日志行（格式: [AGENT_VERIFY:TRACE] <json>）
3. 解析 JSON 事件
4. 补充衍生字段（duration_ms 计算等）
5. 按 sequence number 排序
6. 输出 JSONL
```

**事件类型**:

| 事件类型 | 含义 | 关键字段 |
|----------|------|----------|
| `run_start` | Agent 开始执行 | `input`, `flags`, `ts` |
| `tool_call` | 工具被调用 | `tool_name`, `input`, `ts` |
| `tool_result` | 工具返回结果 | `tool_name`, `output`, `ts` |
| `llm_response` | LLM 生成响应 | `content`, `step` (planning/execution/verification), `ts` |
| `state_change` | 内部状态变化 | `key`, `value`, `ts` |
| `error` | 发生错误 | `error_type`, `message`, `ts` |
| `run_end` | Agent 执行结束 | `final_output`, `total_steps`, `total_duration_ms` |

**结构化日志注入方式**: 在被验证 Agent 的 system prompt 中追加：

```
[系统指令] 在每个关键步骤后，输出一行 JSON 格式的执行日志。
格式: [AGENT_VERIFY:TRACE] {"type": "<event_type>", ...}
事件类型: run_start, tool_call, tool_result, llm_response, state_change, error, run_end
这些日志不会展示给最终用户。
```

#### 6.2.2 assertion_engine.py — 确定性断言引擎

**职责**: 加载断言配置，对结构化日志执行规则检查，输出 Pass/Fail。

**输入**: `trace.jsonl` + `assertions.yaml`

**输出**: `assertion_result.json`

```json
{
  "assertion_id": "search-tool-called",
  "pass": true,
  "reason": null,
  "details": {
    "actual_count": 3,
    "expected_min": 1
  }
}
```

**核心架构**:

```python
class AssertionEngine:
    def __init__(self, assertions_file: str):
        self.assertions = self._load_assertions(assertions_file)

    def check(self, trace: List[Event]) -> List[AssertionResult]:
        results = []
        for assertion in self.enabled_assertions:
            checker = self._get_checker(assertion.type)
            result = checker.check(trace, assertion.target, assertion.condition)
            results.append(result)
        return results
```

**六种检查器**:

| 检查器类 | 对应断言类型 | 核心逻辑 |
|----------|-------------|----------|
| `ToolCallChecker` | `tool_call` | 统计 trace 中 `tool_call` 事件的 `tool_name` 匹配次数 |
| `ToolParamChecker` | `tool_param` | 提取匹配的工具调用的 `input[param_name]`，执行条件检查 |
| `OutputMatchChecker` | `output_match` | 对 `final_output` 执行正则匹配 |
| `PathSequenceChecker` | `path_sequence` | 提取 `llm_response.step` 序列，验证顺序和完整性 |
| `TimingChecker` | `timing` | 计算目标步骤的时间差 |
| `OutputSchemaChecker` | `output_schema` | 对 `final_output` 执行 JSON Schema 验证 |
| `CustomScriptChecker` | `custom_script` | 调用外部脚本，传递 trace 作为 stdin，读取 stdout 结果 |

**错误处理**: 如果检查器执行异常（如 JSON Schema 验证失败），返回 `pass=false` 并附带异常信息作为 `reason`，不抛出异常中断整体流程。

#### 6.2.3 regression_runner.py — 回归测试编排器

**职责**: 遍历测试套件用例，依次执行 Agent → 解析日志 → 运行断言 → (可选)LLM 裁判。

**核心流程**:

```python
class RegressionRunner:
    def run(self, suite_name: str, scope: str = "all",
            baseline: str = None, enable_judge: bool = None) -> Report:

        suite = self._load_suite(suite_name)
        test_cases = self._select_cases(suite, scope)

        case_results = []
        for case in test_cases:
            # 1. 执行 Agent
            raw_output = self._run_agent(case.input, suite.defaults)

            # 2. 解析结构化日志
            trace = self._parse_log(raw_output)

            # 3. 运行断言
            assertion_results = self._run_assertions(trace, case)

            # 4. (可选) LLM 裁判
            judge_scores = None
            if self._should_judge(case, enable_judge):
                judge_scores = self._run_judge(case, raw_output)

            case_results.append(CaseResult(
                case_id=case.id,
                trace=trace,
                assertion_results=assertion_results,
                judge_scores=judge_scores
            ))

        # 5. 聚合结果
        summary = self._aggregate(case_results)

        # 6. 与基线对比
        if baseline:
            comparison = self._compare_baseline(summary, baseline)
        else:
            comparison = None

        # 7. 生成报告
        return self._generate_report(summary, comparison)
```

**增量运行策略** (`scope=changed`):

```
1. 读取 git diff 获取修改的文件列表
2. 简单映射规则:
   - 修改了 tools/ 目录 → 运行所有关联 tool_call 和 tool_param 断言的用例
   - 修改了 prompts/ 目录 → 运行全量（prompt 修改影响面广）
   - 修改了 feature_flags 配置 → 运行全量
   - 其他 → 运行 smoke 分组
3. 回退策略: 无法判断影响面时，运行全量
```

#### 6.2.4 ab_comparator.py — A/B 对比器

**职责**: 对 Flag=OFF 和 Flag=ON 两次运行结果进行逐维度 diff。

**核心逻辑**:

```python
class ABComparator:
    def compare(self, flag_name: str, suite_name: str,
                baseline_name: str = None) -> ABReport:

        # 1. Flag=OFF（旧版本）
        if baseline_name:
            off_results = self._load_baseline(baseline_name)
        else:
            off_results = self._run_with_flag(flag_name, "OFF", suite_name)

        # 2. Flag=ON（新版本）
        on_results = self._run_with_flag(flag_name, "ON", suite_name)

        # 3. 逐维度 diff
        diffs = []
        for case_id in self._all_case_ids(off_results, on_results):
            off_case = off_results.get(case_id)
            on_case = on_results.get(case_id)

            # 断言对比
            assertion_diff = self._diff_assertions(off_case, on_case)

            # 评分对比
            score_diff = self._diff_scores(off_case, on_case)

            # 执行效率对比
            perf_diff = self._diff_performance(off_case, on_case)

            diffs.append(Diff(case_id, assertion_diff, score_diff, perf_diff))

        # 4. 生成报告
        return self._build_report(flag_name, off_results.meta, on_results.meta, diffs)
```

**diff 判断逻辑**:

- 断言: PASS→FAIL = regression（标红），FAIL→PASS = improvement（标绿）
- LLM 评分: 变化 > +0.5 = improvement（标绿），变化 < -0.5 = regression（标红），其他 = neutral
- 性能: 耗时增加 > 20% = warning（标黄）

#### 6.2.5 baseline_manager.py — 基线管理器

**职责**: 保存/加载/对比质量基线快照。

**核心接口**:

```python
class BaselineManager:
    def save(self, name: str, report: Report, meta: dict) -> str:
        """保存当前运行结果为基线，返回文件路径"""

    def load(self, name: str) -> Baseline:
        """加载指定基线"""

    def list(self) -> List[BaselineMeta]:
        """列出所有基线（仅元信息，不全量加载）"""

    def compare(self, name1: str, name2: str) -> BaselineComparison:
        """对比两个基线"""
```

#### 6.2.6 llm_judge.py — LLM 裁判评分器 (V1.0)

**职责**: 实现三级仲裁体系的 LLM 裁判评分。

**核心设计（简化签名）**:

```python
class LLMJudge:
    def __init__(self, model: str = "claude-haiku", dimensions: List[str] = None):
        self.model = model
        self.dimensions = dimensions or ["accuracy", "completeness",
                                          "reasonableness", "tool_usage",
                                          "risk_awareness"]

    def score(self, task: str, agent_output: str,
              quality_criteria: dict, n_runs: int = 3) -> JudgeResult:
        """
        对 Agent 输出进行评分。

        task: 用户原始输入 + 预期路径描述
        agent_output: Agent 的完整输出
        quality_criteria: 每个维度的评分要求
        n_runs: 重复评分次数

        返回: 每个维度的均值和方差
        """
        scores = {dim: [] for dim in self.dimensions}
        for _ in range(n_runs):
            run_scores = self._single_evaluation(task, agent_output, quality_criteria)
            for dim in self.dimensions:
                scores[dim].append(run_scores[dim])

        result = JudgeResult()
        for dim in self.dimensions:
            result.scores[dim] = {
                "mean": statistics.mean(scores[dim]),
                "std": statistics.stdev(scores[dim]) if n_runs > 1 else 0,
                "runs": scores[dim]
            }

        # 方差告警
        result.warnings = []
        for dim in self.dimensions:
            if result.scores[dim]["std"] > MAX_VARIANCE:
                result.warnings.append(
                    f"{dim} 评分方差 {result.scores[dim]['std']:.2f} 超过阈值，建议人工审查"
                )

        return result
```

**评分 prompt 模板**:

```
你是一个 AI Agent 质量评审专家。请对以下 Agent 的输出进行评分。

## 任务描述
{task}

## Agent 输出
{agent_output}

## 评分维度
{quality_criteria_formatted}

## 评分要求
- 每个维度评 1-10 分（1=极差，10=完美）
- 仅基于 Agent 输出与任务描述的匹配度评分
- 不要基于你对该领域的先验知识评分
- 评分理由不超过一句话

## 输出格式
```json
{"accuracy": <score>, "completeness": <score>, ...}
```
```

**可靠性保证措施（三级仲裁体系）**:

agent-verify 采用**三级仲裁体系**确保 LLM 裁判评分的可靠性，与架构设计决策对齐：

| 级别 | 角色 | 模型 | 触发条件 | 说明 |
|------|------|------|----------|------|
| **一级：初裁** | 日常主裁判 | `claude-haiku` | 每次 LLM 裁判启用时 | 成本低、速度快，对简单评估足够可靠 |
| **二级：方差检测** | 自动一致性检查 | -- | 同输入 3 次打分标准差 > 1.5 | 检测 haiku 评分的不一致性，触发告警 |
| **三级：仲裁** | 争议升级裁判 | `claude-sonnet` | 方差超阈值 OR 断言 FAIL 但 haiku 评分高 | 评分方差更小、推理更深，用于最终裁定 |

**仲裁升级流程**:

```
一级初裁 (haiku, 3 次打分)
    │
    ├── 方差 < 1.5 且无冲突 → 直接采纳 haiku 评分
    │
    └── 方差 >= 1.5 OR 断言 FAIL 但评分高
            │
            ▼
        二级检测通过，触发三级仲裁
            │
            ▼
        三级仲裁 (sonnet, 3 次打分)
            │
            └── 以 sonnet 评分为最终结果，报告中标注"经仲裁"
```

**核心设计**:

```python
class LLMJudge:
    def __init__(self, primary_model: str = "claude-haiku",
                 arbitration_model: str = "claude-sonnet",
                 dimensions: List[str] = None):
        self.primary_model = primary_model          # 一级初裁模型
        self.arbitration_model = arbitration_model  # 三级仲裁模型
        self.max_variance = 1.5                     # 方差阈值
        self.dimensions = dimensions or ["accuracy", "completeness",
                                          "reasonableness", "tool_usage",
                                          "risk_awareness"]

    def score(self, task: str, agent_output: str,
              quality_criteria: dict, n_runs: int = 3) -> JudgeResult:
        """
        三级仲裁评分流程。

        1. 一级初裁：haiku 打分 n_runs 次
        2. 二级方差检测：检查标准差是否超阈值
        3. 三级仲裁：若超阈值，升级到 sonnet 重新打分
        """
        # 一级初裁
        primary_scores = self._run_evaluations(
            self.primary_model, task, agent_output, quality_criteria, n_runs
        )

        # 二级方差检测
        needs_arbitration = False
        for dim in self.dimensions:
            std = statistics.stdev(primary_scores[dim]) if n_runs > 1 else 0
            if std > self.max_variance:
                needs_arbitration = True
                break

        # 三级仲裁（仅在需要时触发）
        if needs_arbitration:
            arbitration_scores = self._run_evaluations(
                self.arbitration_model, task, agent_output, quality_criteria, n_runs
            )
            final_scores = arbitration_scores
            arbitration_triggered = True
        else:
            final_scores = primary_scores
            arbitration_triggered = False

        return JudgeResult(
            scores=final_scores,
            primary_scores=primary_scores,
            arbitration_triggered=arbitration_triggered,
            arbitration_model=self.arbitration_model if arbitration_triggered else None
        )

    def _run_evaluations(self, model, task, agent_output, criteria, n_runs):
        """对指定模型执行 n_runs 次打分"""
        scores = {dim: [] for dim in self.dimensions}
        for _ in range(n_runs):
            run_scores = self._single_evaluation(model, task, agent_output, criteria)
            for dim in self.dimensions:
                scores[dim].append(run_scores[dim])
        return scores
```

**成本控制**:
1. **一级初裁优先**: 默认使用 claude-haiku，成本极低（~$1/M input tokens）
2. **仲裁按需触发**: 仅在方差超标或结果冲突时才升级到 sonnet（~$3/M input tokens），正常情况下不产生额外成本
3. **月度预算控制**: 计算累计 token 消耗（含仲裁），超预算自动禁用所有 LLM 裁判
4. **成本差异说明**: 大规模回归测试时（20+ 用例 x 5 维度 x 3 次），haiku vs sonnet 的成本差异会被放大 ~300 倍，三级体系确保大部分场景只用 haiku

### 6.3 Skill 入口点设计 (SKILL.md)

**SKILL.md 结构规划** (~400 行):

```markdown
---
name: agent-verify
description: >-
  AI Agent verification toolkit — the pytest for AI Agents. Define assertions
  to check agent behavior, run regression tests, A/B compare feature flags,
  and manage quality baselines — all within Claude Code. Use when: testing
  agent quality, verifying agent behavior, checking for regressions, comparing
  prompt changes, establishing quality baselines. Triggers on: "验证agent",
  "测试agent", "回归测试", "检查质量", "对比一下", "A/B test", "断言",
  "assertion", "regression test", "verify agent", "baseline quality",
  "feature flag comparison".
license: MIT
compatibility: macOS, Linux (requires Python 3.10+, Claude Code CLI)
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# agent-verify: AI Agent Verification Toolkit

## Quick start

1. Initialize: `/agent-verify:init --target <your-agent-name>`
2. Add an assertion: `/agent-verify:assert --add`
3. Run regression: `/agent-verify:regression`

## Commands

### /agent-verify:init
Initialize a verification project...

### /agent-verify:assert
Define and manage assertions...

### /agent-verify:regression
Run regression tests...

### /agent-verify:compare
A/B compare feature flags...

### /agent-verify:baseline
Manage quality baselines...

### /agent-verify:suite
Manage test suites...

### /agent-verify:report
Generate verification reports...

## Configuration

See [config-reference.md](references/config-reference.md) for complete configuration reference.

## Assertion Types

See [assertion-types.md](references/assertion-types.md) for all 6 assertion types with examples.

## Common Patterns

See [workaround-patterns.md](references/workaround-patterns.md) for common assertion-writing patterns.

## CI/CD Integration

See [integration-guide.md](references/integration-guide.md) for GitHub Actions setup.
```

**SKILL.md 设计原则**:
1. Frontmatter 的 `description` 包含 10+ 中英文触发短语（遵循 Skill 系统"激进触发"原则）
2. 主体保持 350-400 行，核心工作流和命令编排内联
3. 详细参考材料（断言类型、评分 rubric、集成指南）放在 `references/` 中按需加载
4. 使用祈使句/不定式写作风格
5. U 形注意力曲线：关键约束放在开头的 Quick start 和结尾的 Common Patterns 区域

### 6.4 与 Claude Code 现有系统的集成

| 集成点 | 方式 | 说明 |
|--------|------|------|
| **Skill 系统** | 标准 SKILL.md + scripts/ + references/ + templates/ + examples/ | 完全遵循 Skill 规范，无特殊集成需求 |
| **Claude API (LLM 裁判)** | MCP `claude` 或直接 API 调用 | 裁判使用与开发模型不同的模型实例，避免"自己评自己" |
| **Agent 执行** | Bash 工具 + `claude --print --input "..."` | 通过 CLI 执行被验证的 Agent |
| **文件系统** | Read/Write/Edit 工具（在用户项目目录下） | 配置、断言、基线、报告均存储在用户本地文件系统 |
| **环境变量** | `AGENT_FLAG_*` 前缀 | Feature Flag 通过环境变量注入 Agent 执行环境 |
| **结构化日志注入** | System Prompt 追加 | 在被验证 Agent 的 prompt 末尾注入日志指令 |
| **权限** | `allowed-tools: [Bash, Read, Write, Edit]` | 预声明权限，避免运行时弹窗 |
| **隔离执行** | `context: fork`（可选，大套件推荐） | 隔离执行大型回归测试，不膨胀主对话上下文 |

---

## 七、开发路线图

### 7.1 MVP (第 1-2 周)

**目标**: 让用户能定义 3 条断言 + 跑 3 条测试用例，从"凭感觉"变成"看通过率"。

**功能清单**:

| 命令/组件 | 支持的功能 | 不支持的功能 |
|-----------|-----------|-------------|
| `/agent-verify:init` | `--target`、`--template minimal\|default` | `--template advanced` |
| `/agent-verify:assert` | `--add`（3 种类型：tool_call、tool_param、output_match）、`--list`、`--remove` | `--add` 的 path_sequence/timing/output_schema 类型、`--run` |
| `/agent-verify:suite` | `--add`（交互式）、`--list` | `--import`、`--export`、`--generate` |
| `/agent-verify:regression` | 全量运行 + 断言结果 + 简单文本报告 | LLM 裁判、基线对比 |
| `parse_log.py` | 全部 6 种事件类型解析 | 衍生字段计算 |
| `assertion_engine.py` | 3 种检查器（ToolCall、ToolParam、OutputMatch） | 其他 3 种检查器、custom_script |
| `regression_runner.py` | 全量运行 + 聚合 + 文本报告 | 增量运行、基线对比 |
| `config.yaml` | execution、assertions 段落 | llm_judge、feature_flags 段落 |

**交付物**:

| 文件 | 内容 | 预计工时 |
|------|------|----------|
| `SKILL.md` | 命令路由 + 初始化 + 断言定义 + 回归运行的工作流 | 1 天 |
| `scripts/parse_log.py` | 结构化日志解析器（6 种事件类型） | 0.5 天 |
| `scripts/assertion_engine.py` | 确定性断言引擎（3 种类型） | 1 天 |
| `scripts/regression_runner.py` | 回归测试编排器（全量） | 1 天 |
| `scripts/utils.py` | 通用工具函数（YAML 加载、文件操作） | 0.5 天 |
| `templates/config-template.yaml` | 默认配置模板（MVP 字段） | 0.5 天 |
| `templates/suite-template.yaml` | 空测试套件模板 | 0.5 天 |
| `templates/assertions-template.yaml` | 空断言文件模板 | 0.5 天 |
| `references/assertion-types.md` | 3 种断言类型的详细说明 + 示例 | 0.5 天 |
| `examples/example-search-agent/` | 搜索 Agent 完整验证示例 | 1 天 |

**验收标准**:

- [ ] 在 10 分钟内从零搭建验证套件（init → 3 条断言 → 1 条用例 → 跑通回归）
- [ ] 断言准确率 100%（确定性规则无误判）
- [ ] 至少 1 个真实 Agent（如 search-agent）能成功验证
- [ ] `parse_log.py` 正确解析全部 6 种事件类型
- [ ] `assertion_engine.py` 对 3 种断言类型返回正确的 Pass/Fail
- [ ] `regression_runner.py` 在全部 PASS 时返回退出码 0，有 FAIL 时返回非 0（CI 友好）

---

### 7.2 V1.0 (第 3-8 周)

**目标**: 完整的"双层裁判"体系 + Feature Flag A/B 对比，可公开发布。

**新增功能**:

| 命令/组件 | 新增功能 |
|-----------|---------|
| `/agent-verify:assert` | 扩展至 6 种断言类型（+path_sequence、timing、output_schema）、`--run`、`--type <type>` 快捷参数 |
| `/agent-verify:suite` | `--import`、`--export`、`--generate`（AI 生成测试用例） |
| `/agent-verify:regression` | LLM 裁判集成、基线自动对比、JSON 报告输出 |
| `/agent-verify:compare` | **全新命令**: Feature Flag A/B 对比 |
| `/agent-verify:baseline` | **全新命令**: `--save`、`--list`、`--compare` |
| `/agent-verify:report` | **全新命令**: Markdown/JSON/HTML 报告生成 |

**新增交付物**:

| 文件 | 内容 | 预计工时 |
|------|------|----------|
| `scripts/llm_judge.py` | LLM 裁判评分器（三级仲裁体系：haiku 初裁 + 方差检测 + sonnet 仲裁 + 成本控制） | 2 天 |
| `scripts/ab_comparator.py` | A/B 对比报告生成器 | 1 天 |
| `scripts/baseline_manager.py` | 基线管理（保存/加载/对比） | 1 天 |
| `scripts/report_generator.py` | 综合报告生成器（Markdown/JSON/HTML） | 0.5 天 |
| `scripts/assertion_engine.py`（扩展） | 新增 PathSequence/Timing/OutputSchema/CustomScript 检查器 | 1 天 |
| `references/scoring-rubric.md` | LLM 裁判评分维度设计指南 | 0.5 天 |
| `references/config-reference.md` | 配置文件完整参考（全部字段） | 0.5 天 |
| `references/integration-guide.md` | CI/CD 集成教程（GitHub Actions） | 1 天 |
| `references/workaround-patterns.md` | 10+ 常见场景断言编写模式 | 0.5 天 |
| `templates/github-actions-workflow.yml` | GitHub Actions CI 模板 | 0.5 天 |
| `templates/baseline-template.json` | 基线快照格式模板 | 0.5 天 |
| `examples/example-chat-agent/` | 对话 Agent 完整验证示例 | 1 天 |

**验收标准**:

- [ ] A/B 对比报告正确识别变好/变坏的测试用例（差异方向正确）
- [ ] LLM 裁判评分方差 < 1.5（同输入 3 次打分标准差）
- [ ] 用户可用 `examples/` 中的示例在 15 分钟内复现完整验证流程
- [ ] 全部 7 个命令的 SKILL.md 文档覆盖使用说明和示例
- [ ] 全部 4 个 references/ 文档内容完整
- [ ] Feature Flag 双重通道（env + file）均可正常工作
- [ ] config.yaml 全部段落有对应的解析和验证

---

### 7.3 V2.0 (第 3-6 月)

**目标**: 高级自动化 + 生态扩展 + 智能特性。

| 功能 | 描述 | 优先级 | 预计工时 |
|------|------|--------|----------|
| **测试用例 AI 生成器** | 从功能描述自动生成 Happy Path 测试用例初稿（改进 `--generate`） | 高 | 3 天 |
| **覆盖率缺口分析** | 分析哪些工具/路径/输入类型未被测试覆盖 | 高 | 5 天 |
| **智能回归选择** | 基于 git diff 分析选择相关测试用例子集运行 | 中 | 3 天 |
| **真实输入收集器** | 从生产日志收集真实用户输入，清洗后加入测试套件 | 中 | 5 天 |
| **CI 深度集成** | GitHub Actions workflow 模板 + PR 状态检查 | 中 | 3 天 |
| **测试用例推荐** | "你最近加了 X 工具，要不要加一条相关断言？" | 低 | 2 天 |
| **多 Agent 协作验证** | 支持验证 multi-agent 系统的 Agent 间交互 | 低 | 5 天 |
| **历史趋势 Dashboard** | 评分变化趋势图 | 低 | 3 天 |

**V2.0 不做但在雷达上的**:

- Codex 闭环自我修复（研究阶段，风险极高）
- SaaS 化（与 Skill 定位矛盾）
- 多模态 Agent 评估（需 Claude 多模态能力升级）
- 生产监控（属于 LangSmith/Galileo 的领域）

**验收标准**:

- [ ] 覆盖率缺口分析正确识别未覆盖的工具和路径
- [ ] 智能回归选择在 prompt 变更时正确选择全量，在工具变更时正确选择子集
- [ ] AI 生成的测试用例经人工审核后入库率 > 70%
- [ ] CI 集成模板可在 GitHub Actions 上零配置运行

---

## 八、附录

### 8.1 FAQ

**Q: agent-verify 和 pytest 的关系是什么？**

A: 互补关系。pytest 测试 Agent 的代码逻辑（如工具函数是否正确），agent-verify 测试 Agent 的行为质量（如 Agent 是否正确使用了工具、输出是否符合预期）。两者可用在同一项目中。

**Q: agent-verify 需要修改我的 Agent 代码吗？**

A: 至少需要：Agent 支持 CLI 调用（`claude --print --input "..."`）和结构化日志输出（在 prompt 中追加日志指令即可，不需要修改 Agent 代码）。Feature Flag A/B 对比需要 Agent 代码能读取环境变量。除此之外，agent-verify 不侵入 Agent 代码。

**Q: LLM 裁判的成本有多高？**

A: 以 claude-haiku 为裁判，5 维度评分，3 次打分取均值，每条测试用例约消耗 3000-5000 input tokens + 200-400 output tokens。8 条用例的测试套件约消耗 $0.05-0.10。月度预算默认 $50，足够每日多次运行。

**Q: 断言和 LLM 裁判结果冲突怎么办？**

A: 断言 FAIL 但 LLM 评分高 → 断言可能过时或过严，建议审查断言规则。
断言 PASS 但 LLM 评分低 → LLM 裁判发现了断言未覆盖的质量问题，建议补充断言或改进 Agent。
断言具有"一票否决权"——断言 FAIL 意味着存在确定性问题，无论 LLM 评分如何都应处理。

**Q: 测试套件应该包含多少条用例？**

A: 最小有效规模是 3 条（1 条 Happy Path + 1 条复杂场景 + 1 条边界/错误场景）。典型规模是 8-20 条。超过 50 条后建议使用测试分组（smoke/full）管理，日常只跑 smoke（3-5 条核心用例）。

**Q: 支持验证哪些类型的 Agent？**

A: 需要满足两个条件：1) 可通过 CLI 调用（`claude --print --input "..."`）; 2) 能产出结构化日志。当前支持工具调用型 Agent（最佳适配）、对话型 Agent、多步工作流 Agent。不支持纯事件驱动或流式 Agent（需要额外适配）。

**Q: 结构化日志注入会影响 Agent 的行为吗？**

A: 会。在 Agent 的 system prompt 中追加日志指令会改变 prompt 的内容，可能对 Agent 行为产生以下影响：

| 影响类型 | 说明 | 缓解措施 |
|----------|------|----------|
| **Token 开销增加** | 日志指令 + 输出的 JSON 行会消耗额外 token（通常每步 50-150 tokens） | 仅在验证模式下注入；生产环境不注入 |
| **行为微调** | 要求 Agent 输出日志可能使其更"刻意"地遵循指令，导致验证结果略优于真实表现 | 保持日志指令简洁（3-5 行）；日志格式简单（JSON 单行） |
| **步骤级影响** | `llm_response` 日志要求 Agent 标注当前步骤（planning/execution/verification），可能引导 Agent 更结构化的思考 | 这是**正向影响**——帮助 Agent 在验证模式下更好地组织推理 |
| **输出被污染** | 如果 Agent 未正确隐藏 `[AGENT_VERIFY:TRACE]` 行，日志可能出现在最终输出中 | 日志指令明确要求"这些日志不会展示给最终用户"；解析器自动过滤 |

**核心原则**: 结构化日志注入是一种 **观察者效应**（observer effect）——测量行为本身会影响被测量对象。但 agent-verify 的定位是"开发时验证工具"而非"生产监控工具"，因此：
- 验证结果反映的是 **"Agent 在验证模式下的行为"**，与生产行为可能存在微小差异
- 对于回归检测和 A/B 对比，只要日志注入条件一致，差异方向仍然可信
- 建议在发布前同时运行一次**无日志注入的"裸跑"**作为最终确认（通过 `--no-trace` 选项，V1.0 支持）

### 8.2 已知限制

| 限制 | 影响 | 缓解措施 | 预计解决版本 |
|------|------|----------|-------------|
| **LLM 裁判可靠性** | 同输入多次评分可能不一致（方差 > 1.5） | 3 次打分取均值 + 方差告警 + 多模型交叉验证 | V1.0 基础版，V2.0 改进 |
| **不支持流式 Agent** | 实时输出流的 Agent 无法解析结构化日志 | 在 prompt 中要求 Agent 在流结束后追加结构化日志块 | V2.0 |
| **不支持多模态评估** | 无法评估图像/视频生成 Agent | 等待 Claude 多模态能力升级后评估 | 待定 |
| **增量回归精确度有限** | 基于简单规则的影响面分析可能遗漏或过度 | 不确定时回退到全量 | V2.0 改进 |
| **Feature Flag 需 Agent 代码配合** | Agent 代码必须能读取环境变量并据此切换行为 | 提供 Agent 侧的 Flag 读取代码模板 | 当前版本即为限制 |
| **单用例超时后无中间结果** | 超时用例的日志可能不完整 | 超时阈值建议设为 Agent 正常耗时的 2 倍 | 设计限制 |

### 8.3 术语表

| 术语 | 英文 | 定义 |
|------|------|------|
| **断言** | Assertion | 对 Agent 行为的确定性规则检查，输出 PASS/FAIL。断言是 100% 确定的。 |
| **测试套件** | Suite | 一组测试用例的集合，按 Agent 或功能模块组织。 |
| **基线** | Baseline | 某一时刻 Agent 质量的全量快照，用于回归对比。 |
| **Feature Flag** | Feature Flag | 命名的功能开关，通过环境变量注入，用于 A/B 对比测试。 |
| **结构化日志** | Structured Log / Trace | Agent 执行过程中产生的 JSONL 格式事件流，供断言引擎消费。 |
| **断言引擎** | Assertion Engine | 加载断言配置、对结构化日志执行规则检查、输出结果的模块。 |
| **LLM 裁判** | LLM Judge / Supervisor | 使用与开发隔离的 LLM 对 Agent 输出进行量化打分的模块。 |
| **回归测试** | Regression Test | 对已有测试用例集重新运行，检查是否引入退化的过程。 |
| **双层裁判** | Two-Tier Judge | 断言（硬性规则检查）+ LLM 裁判（模糊质量评估）的分层验证体系。 |
| **Happy Path** | Happy Path | 正常、预期的执行路径，用户输入合理、Agent 行为正确的最常见场景。 |
| **A/B 对比** | A/B Comparison | Flag=OFF（旧行为）和 Flag=ON（新行为）两次运行的逐维度差异分析。 |

### 8.4 参考资料

本实现方案基于以下输入文档：

1. **skill-architecture-design.md** -- 架构设计（权威设计决策来源）
2. **skill-system-research.md** -- Skill 系统约束与设计模式研究
3. **engineering-components.md** -- 视频方法论的 16 个可工程化组件分析

引申参考：

4. [Claude Code Skills 官方指南](https://github.com/anthropics/skills) -- Skill 系统规范
5. [Gartner 2026: AI Agent 评估市场报告](https://www.gartner.com) -- 需求数据来源
6. [Patronus AI 2026: Agent 失败率研究](https://www.patronus.ai) -- 63% 初始失败率数据
7. [LangChain State of AI Agents 2026](https://www.langchain.com/stateofaiagents) -- 52% 团队评估率数据

### 8.5 Skill 规范合规清单

| 规范项 | 要求 | 本 Skill 状态 |
|--------|------|-------------|
| 目录名 | kebab-case, <=64 字符 | :white_check_mark: `agent-verify` (13 字符) |
| 文件名 | 必须为 `SKILL.md` | :white_check_mark: |
| name frontmatter | kebab-case, 匹配目录名 | :white_check_mark: `agent-verify` |
| description | <=1024 字符, 无 `<>` | :white_check_mark: ~900 字符 |
| SKILL.md 行数 | < 500 行 | :white_check_mark: 目标 ~400 行 |
| 写作风格 | 祈使句/不定式 | :white_check_mark: |
| 无 README | 不创建文档文件 | :white_check_mark: 仅 SKILL.md + scripts/ + references/ + templates/ + examples/ |
| allowed-tools | 声明所需工具权限 | :white_check_mark: Bash/Read/Write/Edit |
| scripts/ | 通过 Bash 执行，不读入上下文 | :white_check_mark: Python 脚本 |
| references/ | 从 SKILL.md 命令式引用 | :white_check_mark: |
| 保留名 | 不含 "claude" 或 "anthropic" | :white_check_mark: `agent-verify` |

### 8.6 依赖清单

| 依赖 | 类型 | 用途 | 必需？ |
|------|------|------|--------|
| Python 3.10+ | 运行时 | 断言引擎、解析器、执行器、报告生成 | :white_check_mark: |
| PyYAML | Python 包 | YAML 配置文件解析 | :white_check_mark: |
| Claude Code CLI | 运行时 | 执行被验证的 Agent (`claude --print`) | :white_check_mark: |
| Claude API | API | LLM 裁判评分 (V1.0+) | :x: (MVP 不需要) |
| jq (可选) | 命令行 | JSONL 快速查询 | :x: |
| Git | 命令行 | 增量测试范围判断、基线版本关联 | :x: (可选) |

---

*文档完成时间: 2026-06-30*
*文档作者: Writer (技术文档撰写人)*
*下一阶段: 开发实施（由 Developer 角色按路线图执行）*
