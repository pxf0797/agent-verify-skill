# Workflows

> 本文档定义 agent-verify Skill 的三大工作流。每个工作流包含步骤编号、命令、预期输出和验证点。

---

## 工作流 1: 首次使用 (First-Time Onboarding)

目标：从零开始为你的 Agent/Skill 项目建立验证体系。预计用时 4 分钟。

### 步骤 1: 初始化项目目录

```bash
# 在项目根目录执行
claude --skill agent-verify --cmd "/agent-verify:init --target my-agent"
```

**命令**: `/agent-verify:init --target my-agent`

**预期输出**:
```
[agent-verify] Initializing verification for: my-agent
  Created: agent-verify/config.yaml
  Created: agent-verify/assertions.yaml
  Created: agent-verify/suites/suites.yaml
  Created: agent-verify/baselines/
  Created: agent-verify/reports/

Next steps:
  1. Review agent-verify/config.yaml (adjust timeouts, agent_command)
  2. Add your first assertion → /agent-verify:assert --add
  3. Run regression → /agent-verify:regression
```

**验证点**: `ls agent-verify/` 应包含 `config.yaml`、`assertions.yaml`、`suites/`、`baselines/`、`reports/`。

### 步骤 2: 添加第一条断言

```bash
claude --skill agent-verify --cmd "/agent-verify:assert --add"
```

**命令**: `/agent-verify:assert --add`

**交互流程**:
1. Skill 提示选择断言类型（输入编号或回车默认 `tool_call`）
2. 输入工具名称（如 `web_search`）
3. 选择条件类型（`min_count`、`max_count`、`exactly`）
4. 输入条件值（如 `1`）
5. 确认后写入 `assertions.yaml`

**预期输出**:
```
[agent-verify] Assertion added:
  id: tool-call-web-search-001
  type: tool_call
  target: web_search
  condition: min_count: 1
  severity: error
  enabled: true

Run this assertion now? (y/N): y
  Result: PASS (web_search called 3 times ≥ 1)
```

**验证点**: `cat agent-verify/assertions.yaml` 应显示新添加的断言。

### 步骤 3: 运行回归测试

```bash
claude --skill agent-verify --cmd "/agent-verify:regression"
```

**命令**: `/agent-verify:regression`

**预期输出**:
```
[agent-verify] Running regression: search-suite
  [1/3] search-simple-001  → PASS (3/3 assertions passed)
  [2/3] search-empty-001   → PASS (2/2 assertions passed)
  [3/3] search-complex-001 → FAIL (1/2 assertions passed)
    - at-least-one-search: PASS
    - result-count-in-range: FAIL (expected ≤ 10, got 15)

Results:
  Passed: 2/3
  Assertion pass rate: 83.3%
  Avg duration: 45.2s
```

**验证点**: 
- `agent-verify/reports/` 下应有 `.md` 报告文件
- `agent-verify/baselines/` 下应有基线快照文件
- 失败的断言有明确的 `reason` 说明

---

## 工作流 2: 日常开发循环 (Daily Development Loop)

目标：在修改 Agent 的行为（修改 prompts、tools 或 logic）后，快速验证改动的效果。

### 判断矩阵

| 改动类型 | 建议 scope | 是否需要 baseline |
|----------|-----------|-----------------|
| 修改 prompt 模板 | `all` | 是 |
| 新增工具 | `all` + 新增工具相关断言 | 是 |
| 修改工具行为 | `changed`（自动检测） | 是 |
| 修改 Agent 逻辑 | `all` | 是 |
| 调整参数/配置 | `smoke`（快检） | 建议 |
| 仅修改文档/测试 | 无需运行 | 否 |

### 步骤 1: 运行回归（按判断矩阵选择 scope）

```bash
# 快速检查（smoke 分组，3-5 条用例，~2 分钟）
claude --skill agent-verify --cmd "/agent-verify:regression --scope smoke"

# 完整回归（所有用例）
claude --skill agent-verify --cmd "/agent-verify:regression --scope all"

# 自动选择变更相关用例（依赖 git diff）
claude --skill agent-verify --cmd "/agent-verify:regression --scope changed"
```

### 步骤 2: 查看基线对比

运行回归后自动与最新基线对比（若 `compare_on_run: true`）。对比报告包含：

- **断言通过率变化**: +5.2%（改进）/ -3.1%（退化）
- **新出现的失败**: 之前通过、现在失败的断言列表
- **已修复的失败**: 之前失败、现在通过的断言列表
- **性能变化**: 平均耗时变化（±X%）
- **LLM 评分变化**: 各维度分数变化（如启用 judge）

### 步骤 3: 决定后续行动

| 对比结果 | 行动 |
|---------|------|
| 通过率不降、无退化 | 确认改动安全，可提交 |
| 通过率上升 | 确认改进了质量，建议更新基线 |
| 有退化但预期内 | 审查退化原因，确认合理后更新基线 |
| 有意外退化 | 回滚或修复，在修复前不更新基线 |

### 步骤 4: 更新基线（可选）

```bash
claude --skill agent-verify --cmd "/agent-verify:baseline --save post-fix-v2"
```

### 步骤 5: 生成报告

```bash
claude --skill agent-verify --cmd "/agent-verify:report --format markdown"
```

**命令**: `/agent-verify:report --format markdown`

**预期输出**: 生成的 Markdown 报告包含断言结果汇总表、每用例详细结果、基线对比信息。

---

## 工作流 3: 质量改进 (Quality Improvement Cycle)

目标：通过周期性运行验证和分析，系统性提升 Agent 质量。

### 阶段 1: 运行全面回归

```bash
claude --skill agent-verify --cmd "/agent-verify:regression --scope all --judge"
```

**命令**: `/agent-verify:regression --scope all --judge`

**预期输出**:
```
[agent-verify] Running full regression with LLM judge...
  [1/10] search-simple-001  → PASS | score: 8.5/10
  [2/10] search-empty-001   → PASS | score: 7.2/10
  ...
```

### 阶段 2: 分析失败模式

查看 `failed_details` 识别常见失败模式：

| 失败模式 | 典型原因 | 改进方向 |
|---------|---------|---------|
| 工具调用次数不足 | Agent 决策过早，未充分搜索 | 优化 prompt 中"搜索更多"指令 |
| 参数为空/过短 | Agent 未生成有效参数 | 添加参数验证和默认值 |
| 输出缺失关键信息 | Agent 遗漏了步骤 | 添加输出格式模板 |
| 执行超时 | Agent 陷入循环或过度搜索 | 设置 step limit 或 timeout |

### 阶段 3: 添加针对性断言

根据阶段 2 的分析结果，添加覆盖率断言：

```bash
# 添加超时断言
claude --skill agent-verify --cmd "/agent-verify:assert --add --type timing"

# 添加输出 schema 断言（V1.0）
claude --skill agent-verify --cmd "/agent-verify:assert --add --type output_schema"
```

### 阶段 4: A/B 对比测试（V1.0）

```bash
# 对 Feature Flag 开启前后的质量做对比
claude --skill agent-verify --cmd "/agent-verify:compare --flag NEW_SEARCH_ALGORITHM"
```

### 阶段 5: 建立质量基线

```bash
# 保存为里程碑基线
claude --skill agent-verify --cmd "/agent-verify:baseline --save v2-release-candidate"

# 后续回归自动对比这个基线
claude --skill agent-verify --cmd "/agent-verify:regression"
```

定期（如每两周）重复阶段 1-5，追踪质量趋势：

| 维度 | 基线 v1 | 基线 v2 | 变化 |
|------|---------|---------|------|
| 断言通过率 | 85% | 92% | +7% |
| 平均 LLM 评分 | 7.2 / 10 | 8.1 / 10 | +0.9 |
| 平均执行时间 | 52s | 45s | -13% |
| 失败用例数 | 3 | 1 | -2 |

---

## 命令速查表

| 命令 | 常用参数 | 说明 |
|------|---------|------|
| `/agent-verify:init` | `--target <name>`, `--template minimal` | 初始化验证项目 |
| `/agent-verify:assert` | `--add`, `--list`, `--remove <id>`, `--run`, `--type tool_call` | 管理断言 |
| `/agent-verify:regression` | `--scope all/smoke/changed`, `--judge`, `--output json` | 运行回归测试 |
| `/agent-verify:compare` | `--flag <name>`, `--suite <file>` | A/B 对比（V1.0） |
| `/agent-verify:baseline` | `--save <name>`, `--list`, `--compare <a> <b>` | 管理基线 |
| `/agent-verify:suite` | `--add`, `--list`, `--generate` | 管理测试套件 |
| `/agent-verify:report` | `--format markdown/json`, `--output <path>` | 生成报告 |
