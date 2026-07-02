# Claude Code Skill System: 深度研究报告

ORCH_ID: `orch-20260630-234518-17009`
生成时间: 2026-06-30

---

## 目录

1. Skill 系统概述
2. 文件结构规范
3. 触发机制
4. 权限模型
5. 设计模式
6. 约束清单
7. 示例分析
8. 参考来源

---

## 1. Skill 系统概述

### 1.1 什么是 Skill

Skill 是 Claude Code 的扩展机制。一个 Skill 是一个自包含的目录，以 `SKILL.md` 为核心文件，打包了专门知识、工作流和工具集成。它将 Claude 从通用 Agent 转变为特定领域的专家 Agent。

**Skill vs MCP vs Plugin 的定位差异：**

| 维度 | Skill | MCP Server | Plugin |
|------|-------|------------|--------|
| 本质 | 指南/知识/程序性知识 | 工具/数据源 | 深度集成 |
| 作用 | "教 Claude 怎么做" | "让 Claude 能做什么" | 扩展平台能力 |
| 上下文 | 占用 prompt 上下文 | 独立进程运行 | 平台级 |
| 传递方式 | SKILL.md + 资源目录 | MCP 协议 | 安装/配置 |

来源: [skill-creator/SKILL.md] / [skywork.ai blog]

### 1.2 Skill 的核心价值

- **专门化工作流**: 针对特定领域的多步流程
- **工具集成**: 操作特定文件格式或 API 的指令
- **领域知识**: 公司特有知识、模式、业务逻辑
- **打包资源**: 脚本、参考资料、模板等可复用资产

来源: [skill-creator/SKILL.md §11-24]

### 1.3 三层渐进加载 (Progressive Disclosure)

Skill 使用三级加载系统来管理上下文窗口效率：

```
Level 1: name + description (始终在上下文中，~100 tokens)
Level 2: SKILL.md 正文 (Skill 触发时加载，<5000 words)
Level 3: 打包资源 (按需加载，无上限——脚本可通过执行而非读入上下文)
```

**关键设计理念**: 上下文窗口是公共资源。每段信息都应问"Claude 真的需要这个解释吗？"和"这段文字值得它的 token 成本吗？"

来源: [skill-creator/SKILL.md §28-34][§115-125]

---

## 2. 文件结构规范

### 2.1 标准目录结构

```
skill-name/
├── SKILL.md            # 必需 — 主技能文件
│   ├── YAML frontmatter (必需)
│   └── Markdown body (必需)
├── scripts/            # 可选 — 可执行代码 (Python/Bash/etc.)
├── references/         # 可选 — 按需加载的文档
└── assets/             # 可选 — 输出中使用的文件 (模板/图标/字体)
```

来源: [skill-creator/SKILL.md §49-63]

### 2.2 SKILL.md 要求

**文件名大小写敏感**: 必须精确为 `SKILL.md`（非 `skill.md` 或 `Skill.md`）。

**YAML Frontmatter 格式**:

```yaml
---
name: skill-name              # 必需 — kebab-case，匹配目录名
description: >-               # 必需 — 包含触发短语，最长 1024 字符
  [做什么]. Invoke whenever task involves
  [domain] — [trigger phrases].
license: MIT                  # 可选
compatibility: macOS          # 可选，1-500 字符
metadata:                     # 可选 — 自定义键值对
  author: name
  version: 1.0.0
disable-model-invocation: true  # 可选 — true=仅用户调用
user-invocable: false           # 可选 — false=仅Claude使用
allowed-tools:                  # 可选 — 免权限提示的工具列表
  - Bash
  - Read
allowed-tools:
  - Bash
argument-hint: "<ticker>"      # 可选 — 参数提示
model: sonnet                  # 可选 — 模型覆盖
context: fork                  # 可选 — 在隔离子Agent中运行
agent: general-purpose         # 可选 — context: fork时的子Agent类型
---
```

**允许的 Frontmatter 字段** (来源: skill-creator/scripts/quick_validate.py):

- `name` — 必需，kebab-case，仅小写字母、数字、连字符
- `description` — 必需，不能含尖括号 `<>`，最长 1024 字符
- `license` — 可选
- `allowed-tools` — 可选
- `metadata` — 可选
- `compatibility` — 可选，最长 500 字符

**Body 规范**:
- 使用祈使句/不定式形式写作
- 推荐 < 500 行，以最小化上下文膨胀
- 核心约束应放在 SKILL.md 的开头 20%（首因区）和结尾 20%（近因区）
- U 形注意力曲线: 开头和结尾的指令遵循率最高

来源: [skill-creator/SKILL.md §305-320] / [skill-creator/scripts/quick_validate.py] / [skywork.ai blog]

### 2.3 Bundled Resources 最佳实践

#### scripts/

**何时使用**: 同一段代码被反复重写，或需要确定性执行路径。
**注意事项**: 脚本仍需被读取以适应环境调整。脚本应被实际运行测试。

#### references/

**何时使用**: Claude 在工作中需要查阅的文档。
**内容建议**: 数据库 Schema、API 文档、领域知识、公司政策、详细工作流指南。

**设计原则**:
- `scripts/`、`references/` 和 `assets/` 三者选有必要的一方，删掉不需要的示例文件
- 如果一个 `references/` 文件包含详尽的模式、配置值、命令参数表，在 SKILL.md 中包含 grep 搜索模式的建议而非复制所有内容
- 引用文件使用深度嵌套（仅从 SKILL.md 直接引用一层）
- 长引用文件（>100 行）在顶部包含目录以便 Claude 预览范围

#### assets/

**何时使用**: 需要被复制或修改的文件（模板、图标、字体、样本文档）。
**注意事项**: 不读入上下文，仅用作输出素材。

来源: [skill-creator/SKILL.md §74-112][§200-202]

### 2.4 不应包含的文件

Skill 目录不应包含 README.md、INSTALLATION_GUIDE.md、QUICK_REFERENCE.md、CHANGELOG.md 等文档文件。这些只会增加杂乱和混淆。Skill 只应包含 AI Agent 完成任务所需的信息。

来源: [skill-creator/SKILL.md §103-113]

---

## 3. 触发机制

### 3.1 触发层级

Skill 的触发有一个渐进链:

```
1. Claude 读取所有技能的前 100 tokens (name + description)
2. Claude 根据 description 判断当前任务是否匹配
3. 匹配 → 加载完整 SKILL.md
4. SKILL.md 中的指令 → 按需引用 references/ 文件
```

来源: [skill-creator/SKILL.md §115-125]

### 3.2 Description 字段的编写策略

description 是 Skill 是否触发的决定性因素。这是最常见的失败模式。

**最佳实践公式**: `[做什么] + [何时使用 — 广义领域声明 + 触发示例]`

**好的例子** (来自 skills/alphagbm-stock-analysis):
```yaml
description: >
  AI-powered stock analysis using AlphaGBM's Five Pillars framework (Fundamental,
  Technical, Sentiment, Flow, Valuation) with real market data. Returns a 1-10
  composite score with actionable signals. Use when: analyzing any stock ticker,
  evaluating buy/sell decisions, comparing stock fundamentals, assessing risk levels.
  Triggers on: "analyze AAPL", "what do you think about NVDA", "should I buy TSLA",
  "stock analysis for META", "is SPY overvalued", "risk assessment for GOOGL".
```

**好的例子** (来自 skills/video-to-md):
```yaml
description: Download a video's audio with yt-dlp, transcribe it to text with Whisper,
  and produce a well-structured markdown summary with chapter timestamps, core concepts,
  and comparison tables. Use when the user asks to organize, summarize, or extract content
  from a video into a markdown file. Triggers on requests like "帮我整理视频内容",
  "summarize this video", "extract content from this YouTube link", "视频转文字整理",
  or similar.
```

**关键原则**:
- **广泛声明，然后列举具体**: "Invoke whenever task involves any interaction with X" 比窄泛措辞更优
- **适度"激进"**: Claude 有低估触发的倾向 — 列出比你认为必要的更多的触发上下文
- **每个 token 必须增加激活概率**: 无口号、无哲学、无填充

来源: [skill-creator/SKILL.md §307-313] / [skywork.ai blog]

### 3.3 触发可靠性数据

| 方法 | 成功率 |
|------|--------|
| 无 hook/仅简单指令 | ~20-50% |
| LLM 预评估 hook (API) | ~80% |
| 强制评估 hook (显式 YES/NO) | ~84-100% |
| 手动 `/skill-name` 调用 | 100% |

来源: [skywork.ai blog]

### 3.4 场景识别模式 (以 multi-agent-orchestrator 为例)

高级 Skill（如 orchestrator）会在 SKILL.md 中定义场景识别逻辑，根据用户输入的关键词判断应该使用哪种流程模板：

| 场景 | 触发关键词 | SOP 模板 |
|------|-----------|---------|
| `code_dev` | 实现/开发/重构/写代码/修bug | 软件开发 SOP |
| `deep_research` | 研究/调查/分析/报告/调研 | 研究报告 SOP |
| `general` | 其他所有情况 | 动态推断 |

来源: [multi-agent-orchestrator/SKILL.md §22-38]

### 3.5 带 globs 的文件自动关联

Skill 可以声明 glob 模式，使文件自动关联到该 Skill：

```yaml
globs:
  - "mock-data/*.json"
```

当用户操作匹配 glob 模式的文件时，相关 Skill 自动触发。

来源: [alphagbm-stock-analysis/SKILL.md]

---

## 4. 权限模型

### 4.1 allowed-tools 字段

Skill 可以声明 `allowed-tools` 来授予特定工具免权限提示使用权限：

```yaml
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
```

这与全局 settings.json 中的 permission 机制配合——对于已知安全的操作（如读取 config 文件、执行 docker ps），预先授权可以避免每次运行时弹出权限确认。

来源: [docker-manage/SKILL.md] / [gstack/qa/SKILL.md]

### 4.2 disable-model-invocation

当设为 `true` 时，Skill 仅能通过用户手动 `/skill-name` 调用，Claude 不会自动触发。适用于有副作用的操作（如管理命令）。

```yaml
disable-model-invocation: true
```

来源: [docker-manage/SKILL.md]

### 4.3 user-invocable

当设为 `false` 时，Skill 仅供 Claude 内部使用，用户无法手动调用。

### 4.4 context: fork

运行时在隔离的子 Agent 中执行 Skill 指令，不影响主会话上下文。适用于大型或独立的任务。

```yaml
context: fork
agent: general-purpose
```

### 4.5 脚本执行权限

`scripts/` 目录下的脚本无需读入上下文即可执行。脚本应该可执行（`chmod +x`），并在 SKILL.md 中明确说明如何调用。

来源: [skill-creator/SKILL.md §74-76]

---

## 5. 设计模式

### 5.1 模式一：高级指南 + 引用文件 (High-level Guide with References)

将核心工作流和选择指南保留在 SKILL.md 中，将变体特定细节（模式、示例、配置）移入独立的 references/ 文件。

```markdown
# PDF Processing

## Quick start
Extract text with pdfplumber:
[code example]

## Advanced features
- **Form filling**: See [FORMS.md](references/FORMS.md) for complete guide
- **API reference**: See [REFERENCE.md](references/REFERENCE.md)
```

来源: [skill-creator/SKILL.md §129-144]

### 5.2 模式二：按领域拆分 (Domain-specific Organization)

```markdown
bigquery-skill/
├── SKILL.md
└── reference/
    ├── finance.md
    ├── sales.md
    ├── product.md
    └── marketing.md
```

当用户询问销售指标时，Claude 仅读取 `sales.md`。

来源: [skill-creator/SKILL.md §149-155]

### 5.3 模式三：按框架/变体拆分 (Multi-variant Organization)

```markdown
cloud-deploy/
├── SKILL.md (workflow + provider selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

当用户选择 AWS 时，Claude 仅加载 aws.md。

来源: [skill-creator/SKILL.md §166-175]

### 5.4 模式四：条件展开 (Conditional Details)

```markdown
## Creating documents
Use docx-js for new documents. See [DOCX-JS.md](references/DOCX-JS.md).

## Editing documents
For simple edits, modify the XML directly.
**For tracked changes**: See [REDLINING.md](references/REDLINING.md)
```

来源: [skill-creator/SKILL.md §178-197]

### 5.5 模式五：参考文件的指令放置

对于 SKILL.md 中引用的文件，有两种放置读指令的方式：

1. **Skill 顶部**（简介后）— 尽早设定预期
2. **需要的步骤处** — 在正确时机触发加载

```markdown
# 糟糕 — 被动链接，可能被跳过
See [WORKFLOW.md](references/WORKFLOW.md) for the format.

# 好 — 命令式，指定时机
**Read [references/WORKFLOW.md](references/WORKFLOW.md) now** and follow its posting format exactly.
```

来源: [skywork.ai blog]

### 5.6 模式六：结构化数据格式选择

不同格式影响指令遵循准确率高达 16 个百分点：

| 格式 | 适用场景 |
|------|---------|
| **KV 列表** | 独立条目数据（路由表、工具参考、评分规则） |
| **Markdown 表格** | 仅用于真正的二维对比（决策矩阵） |
| **编号列表** | 顺序重要的步骤（最多 10-15 步） |
| **子弹列表** | 无顺序要求的规则/约定 |

来源: [skywork.ai blog]

### 5.7 模式七：角色定义 + 约束注入 (Role-based Agent Template)

被 multi-agent-orchestrator 广泛使用。Agent 被分配明确的角色身份，并在 prompt 开头注入：

```
[Role: <角色名>]
[Goal: <核心目标>]
[Backstory: <背景设定>]
[Skills: <技能列表>]
[Constraints: <行为约束>]
[Output Format: <输出格式>]
---
<具体任务描述>
```

这是一种受 CrewAI 的 `role + goal + backstory` 三段式定义启发的模式。

来源: [multi-agent-orchestrator/references/role-templates.md]

### 5.8 模式八：顺序/条件工作流 (Sequential/Conditional Workflows)

来自 skill-creator 的推荐模式。顺序流程用编号步骤，条件分支用 **粗体** 关键词引导：

```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow"
   **Editing existing content?** → Follow "Editing workflow"
```

来源: [skill-creator/references/workflows.md]

### 5.9 模式九：输出模板 (Output Templates)

严格 vs 灵活的两种输出规范：

**严格要求**（如 API 响应）:
```markdown
## Report structure
ALWAYS use this exact template structure:
# [Title]
## Executive summary
...
```

**灵活指导**（允许自适应）:
```markdown
## Report structure
Here is a sensible default format, but use your best judgment:
...
Adjust sections as needed.
```

来源: [skill-creator/references/output-patterns.md]

### 5.10 模式十：子 Agent 调度 (Multi-Agent Orchestration)

由 multi-agent-orchestrator 定义的复杂模式，Coordinator 角色负责：

1. **场景识别** — 判定 `code_dev` / `deep_research` / `general`
2. **任务拆解** — 2-10 个单一职责子任务
3. **DAG 生成** — 用 `blockedBy` 表达任务依赖
4. **并行调度** — 最大 10 个 Agent 并发
5. **结果汇总** — 去重、合并、统计摘要

此模式的特点：
- Coordinator 本身不执行任务，只拆解和调度
- 通过文件系统（JSONL/JSON）进行 Agent 间通信
- 支持检查点断点续传
- 分级错误恢复（E1/E2/E3）

来源: [multi-agent-orchestrator/SKILL.md]

---

## 6. 约束清单

### 6.1 命名约束

| 规则 | 详情 | 来源 |
|------|------|------|
| 目录名 | kebab-case，仅小写字母、数字、连字符 | quick_validate.py |
| 首尾连字符 | 不可开头或结尾 | quick_validate.py |
| 连续连字符 | 不允许 `--` | quick_validate.py |
| 长度 | 最长 64 字符 | quick_validate.py |
| 文件名 | 必须为 `SKILL.md`（区分大小写） | skill-creator/SKILL.md |
| 保留名 | 不可包含 "claude" 或 "anthropic" | 社区指南 |

### 6.2 Frontmatter 约束

| 规则 | 详情 | 来源 |
|------|------|------|
| 必需字段 | `name` + `description` | quick_validate.py |
| 不可含 `<>` | description 中不可有尖括号 | quick_validate.py |
| 长度限制 | description 最长 1024 字符 | quick_validate.py |
| 长度限制 | compatibility 最长 500 字符 | quick_validate.py |
| 允许字段 | name, description, license, allowed-tools, metadata, compatibility | quick_validate.py |
| 无额外字段 | 不允许自定义 frontmatter 字段 | quick_validate.py |

### 6.3 内容约束

| 规则 | 详情 | 来源 |
|------|------|------|
| SKILL.md 长度 | < 500 行 | skill-creator/SKILL.md |
| 写作风格 | 祈使句/不定式 | skill-creator/SKILL.md |
| 无 README | 不要创建 README.md 等文档文件 | skill-creator/SKILL.md |
| 引用深度 | references/ 文件仅从 SKILL.md 直接引用 | skill-creator/SKILL.md |
| 指导自由度 | 匹配任务的关键度: 高自由度(文字说明) / 中自由度(伪代码) / 低自由度(具体脚本) | skill-creator/SKILL.md |

### 6.4 行为约束

| 规则 | 详情 | 来源 |
|------|------|------|
| 不做无关改进 | 不"改进"相邻代码、注释或格式 | CLAUDE.md |
| 不删除无关死代码 | 不删除预存的死代码除非被要求 | CLAUDE.md |
| 不添加未请求功能 | 不多做需求之外的事 | CLAUDE.md |
| 不引入多余抽象 | 不创建单用例的抽象层 | CLAUDE.md |
| 不做投机容错 | 不为不可能场景做错误处理 | CLAUDE.md |
| 匹配现有风格 | 即使你会用不同写法 | CLAUDE.md |
| 每次变更可追溯 | 每个变更行应直接追溯到用户请求 | CLAUDE.md |

### 6.5 Skill 开发流程约束

| 步骤 | 约束 | 来源 |
|------|------|------|
| 1. 理解需求 | 收集具体示例，问关键问题 | skill-creator/SKILL.md §219-231 |
| 2. 规划资源 | 分析每示例，确定需要哪些脚本/引用/资产 | skill-creator/SKILL.md §233-256 |
| 3. 初始化 | 使用 `init_skill.py` 生成模板 | skill-creator/SKILL.md §257-278 |
| 4. 编辑 | 先实现资源文件，再更新 SKILL.md；测试脚本 | skill-creator/SKILL.md §280-321 |
| 5. 打包 | 运行 `package_skill.py` 验证后打包 | skill-creator/SKILL.md §322-348 |
| 6. 迭代 | 在真实任务中使用后改进 | skill-creator/SKILL.md §349-355 |

### 6.6 微约束（来自真实部署经验）

| 规则 | 详情 | 来源 |
|------|------|------|
| 不链 CLI 工具 `||` | `npm audit` 和 `eslint` 成功发现问题时也非零退出 | skywork.ai blog |
| `#N` 在 bash 中是注释 | 用纯数字或 `ISSUE_NUMBER` 占位符 | skywork.ai blog |
| PreToolUse hooks | prompt 指令被视为建议性；hook 做硬约束 | skywork.ai blog |
| Fail-closed 非 fail-open | hook 不确定上下文时，阻塞并解释而非猜测 | skywork.ai blog |
| 单条事件 < 500 字节 | macOS PIPE_BUF 为 512，超限导致 JSONL 行交错损坏 | multi-agent-orchestrator/templates/progress-injection.md |

---

## 7. 示例分析

### 7.1 video-to-md — 中等复杂度 Skill

**目录结构**:
```
video-to-md/
├── SKILL.md        # ~13K, ~300 行
├── assets/         # 空（预留）
├── references/     # 可能含模型对比表
└── scripts/        # 转录/下载脚本
```

**特点**:
- Description 包含中英文触发短语
- 内置并行处理逻辑（多视频并发下载+转录）
- 选择分支逻辑（多转录引擎选择）
- 输出模板（结构化 Markdown）
- 硬件依赖明确（Apple Silicon GPU）

**可观察模式**: 复杂工作流使用 `SKILL.md` 直接内联所有步骤（而非使用 references/），这意味着其作者判定所有内容都应处于 Level 2（触发即加载）。

### 7.2 alphagbm-stock-analysis — API 集成型 Skill

**特点**:
- 描述包含多个特定触发短语
- 定义了 API 端点、认证方式（环境变量中的 API Key）
- 输出结构化评分（1-10）
- 使用 globs 关联本地 mock-data

**可观察模式**: API 集成型 Skill 的标准模板：先声明认证方式 + 环境变量 → API 端点清单 → 输出格式。

### 7.3 context7-mcp — 子步骤工作流 Skill

**特点**:
- 最小化 SKILL.md（仅 2K）
- 只定义工作流步骤，代码示例极少
- 每个步骤对应一个具体 MCP 工具调用

**可观察模式**: 当 Skill 的逻辑由外部工具（MCP Server）承载时，SKILL.md 只需编排调用顺序。

### 7.4 gstack/qa — 大型生产级 Skill

**特点**:
- 使用 `allowed-tools` 声明所需工具
- 使用 `preamble-tier` 控制加载优先级
- 使用 `triggers` 字段声明语音触发别名
- 通过 `.tmpl` 模板文件生成正式 SKILL.md
- 使用版本号 (`version: 2.0.0`)

**可观察模式**: 企业级 Skill 的标准特征 — 版本管理、工具权限白名单、多触发路径。

### 7.5 docker-manage — 纯管理型 Skill

**特点**:
- `disable-model-invocation: true` — 仅用户手动调用
- `allowed-tools: [Read, Bash, Grep]` — 最小权限原则
- 使用独立的 config 文件管理 SSH 连接参数

**可观察模式**: 管理运维类 Skill 遵循"最小权限 + 配置外置"原则。

---

## 8. 参考来源

### 官方来源

| 来源 | 描述 |
|------|------|
| skill-creator/SKILL.md | 官方 Skill 开发指南 - 定义、结构、原则、步骤 |
| skill-creator/scripts/quick_validate.py | 官方验证脚本 - frontmatter 字段白名单、校验规则 |
| skill-creator/scripts/init_skill.py | 官方初始化脚本 - 生成模板目录 |
| skill-creator/scripts/package_skill.py | 官方打包脚本 - 验证+打包 .skill 文件 |
| skill-creator/references/workflows.md | 工作流设计模式（顺序/条件） |
| skill-creator/references/output-patterns.md | 输出模板设计（严格/灵活） |

### 真实 Skill 实现参考

| 来源 | 描述 |
|------|------|
| multi-agent-orchestrator/SKILL.md | 复杂编排 Skill - 全功能示例，含 DAG/并行/HITL/检查点 |
| multi-agent-orchestrator/references/role-templates.md | 7 种角色模板定义 |
| multi-agent-orchestrator/templates/progress-injection.md | Agent 进度上报协议 |
| video-to-md/SKILL.md | 中等复杂度处理管线 Skill |
| video-downloader/SKILL.md | 参考式 Skill（主文档+引用拆分） |
| context7-mcp/SKILL.md | 最小化编排 Skill |
| alphagbm-stock-analysis/SKILL.md | API 集成型 Skill |
| gstack/qa/SKILL.md | 生产级 Skill（版本/工具/多触发） |
| docker-manage/SKILL.md | 管理运维型 Skill |
| workflow-manager/SKILL.md | 多阶段工作流编排 Skill |

### 第三方研究

| 来源 | URL |
|------|-----|
| skywork.ai — Claude Code Skills 终极指南 | https://skywork.ai/blog/ai-bot/claude-code-skills-ultimate-guide/ |
| skywork.ai — Best Practices 指南 | https://skywork.ai/blog/ai-bot/claude-code-skills-ultimate-guide-3/ |
| morphllm — Skills vs MCP vs Plugins | https://www.morphllm.com/claude-code-skills-mcp-plugins |
| rube-de/cc-skills — 实践经验 | https://github.com/rube-de/cc-skills |
| kdnuggets — Anthropic 官方指南摘要 | https://www.kdnuggets.com/anthropics-complete-guide-to-claude-skills-building |
| Anthropic Skills 官方仓库 | https://github.com/anthropics/skills |

---

## 附录 A: Skill 系统的关键文件路径

| 路径 | 内容 |
|------|------|
| `~/.claude/skills/*/SKILL.md` | 所有已安装 Skill 的定义文件 |
| `~/.claude/skills/skill-creator/` | 官方 Skill 开发工具包 |
| `~/.claude/skills/multi-agent-orchestrator/` | 多 Agent 编排器 — 最复杂的 Skill 示例 |
| `~/.claude/settings.json` | Skill 加载和管理配置 |
| `~/.claude/skills/skill-creator/scripts/init_skill.py` | 初始化新 Skill 的脚本 |
| `~/.claude/skills/skill-creator/scripts/quick_validate.py` | Skill 验证脚本（frontmatter 校验规则） |
| `~/.claude/skills/skill-creator/scripts/package_skill.py` | Skill 打包脚本 |
| `~/.claude/orchestrator/` | multi-agent-orchestrator 运行态目录 |

---

*本报告基于对本地 ~/.claude/skills/ 下所有 Skill 的源码阅读、skill-creator 官方文档分析以及网络搜索获得的最佳实践信息整理而成。*
