# AI Agent 验证 Skill 架构设计文档

ORCH_ID: `orch-20260630-234518-17009`
生成时间: 2026-06-30
角色: Architect（技术架构师）

---

## 目录

1. [可行性判断](#1-可行性判断gono-go)
2. [Skill 定位与产品定义](#2-skill-定位与产品定义)
3. [命令体系设计](#3-命令体系设计)
4. [技术架构](#4-技术架构)
5. [关键设计决策](#5-关键设计决策)
6. [开发路线图](#6-开发路线图)

---

## 1. 可行性判断（Go/No-Go）

### 1.1 技术可行性评估

| 评估维度 | 结论 | 依据 |
|----------|------|------|
| Skill 系统兼容性 | **可行** | Skill 系统支持 scripts/（可执行脚本）、references/（按需文档）、allowed-tools（权限白名单）、context:fork（隔离执行）。断言引擎和回归测试所需的全部能力均有支持。 |
| 断言引擎可实现性 | **8/10** | 核心逻辑是 JSONL 解析 + 规则匹配。无研究风险，纯工程实现。 |
| 结构化日志可实现性 | **9/10** | 本质是向 Agent 指令注入日志要求。技术成熟，无新造轮子需求。 |
| LLM 裁判可实现性 | **5/10** | 技术上可行但可靠性是开放问题。通过多模型交叉验证 + 多次打分取均值可缓解。这是整个体系中风险最高的组件。 |
| Feature Flag 可实现性 | **8/10** | 在无原生支持的环境下，通过配置文件 + 环境变量可实现。标准实践。 |
| A/B 对比可实现性 | **9/10** | 跑两次 + diff，技术极简。 |
| 回归测试套件管理 | **7/10** | JSONL 文件 + git 版本控制足够。复杂测试用例管理场景已成熟。 |
| Claude Code 集成 | **可行** | Skill 机制本身即 Claude Code 原生扩展。无需修改 Claude Code 核心代码。 |

**总体技术可行性**: 核心路径（断言引擎 + 结构化日志 + 回归测试）技术风险低。主要风险点在 LLM 裁判的可靠性，但通过渐进式引入（先断言后裁判）可控制。

### 1.2 用户需求验证

| 需求信号 | 强度 | 来源 |
|----------|------|------|
| 99% 组织未在生产前评估 Agent | **极强** | Gartner 2026 |
| Agent 多步任务初始失败率 63% | **极强** | Patronus AI 2026 |
| 仅 52% 团队有系统性评估 | **强** | LangChain State of AI Agents 2026 |
| 75+ 公司进入该赛道，市场 $1.35B | **强** | 工具生态调研 |
| 团队被迫使用 2-3 个工具拼凑 | **强** | 工具生态调研 |
| 视频作者亲自验证了方法论的工程有效性 | **中** | 视频工程化组件报告 |

**需求判断**: 需求明确且强烈。核心痛点是"AI Agent 开发者缺少一个 `pytest`——修改代码后不知道是否退化"。Claude Code 作为 Agent 开发的主要环境，缺少内建的验证工具，这是一个结构性缺口。

**目标用户量级估算**:
- Claude Code 的活跃 Skill 开发者（已发布 Skill/mcp 的用户）: 数千人
- 企业内部使用 Claude Code 开发 Agent 的团队: 潜在数万
- 第一年保守估计: 200-500 活跃用户（通过 GitHub stars/社区反馈交叉验证）

### 1.3 差异化分析

与现有 75+ 工具的对比：

| 维度 | 本 Skill | DeepEval | Promptfoo | Braintrust | LangSmith |
|------|---------|----------|-----------|------------|-----------|
| **运行位置** | Claude Code 内部 | Python 脚本/pytest | CLI | SaaS/API | SaaS/API |
| **零依赖运行** | ✅ (Claude Code 内建) | ❌ (需独立安装) | ❌ (需 Node.js) | ❌ (需网络) | ❌ (需 LangChain) |
| **断言引擎** | ✅ YAML 声明式 | ✅ pytest assert | ✅ YAML 声明式 | ✅ 代码式 | ✅ 代码式 |
| **LLM 裁判** | ✅ 多模型交叉 | ✅ 50+ 指标 | ✅ 基础 | ✅ 自定义评分器 | ✅ 内置评估器 |
| **Feature Flag A/B** | ✅ 内建 | ❌ | ❌ | ❌ | ❌ |
| **与 Agent 开发同屏** | ✅ (同一对话) | ❌ | ❌ | ❌ | ❌ |
| **Skill 格式原生** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **学习成本** | 极低 (YAML + 对话) | 中 (Python + pytest) | 中 (YAML + CLI) | 中 (平台学习) | 高 (LangChain 生态) |

**独特价值主张**: 这是唯一一个**在 Claude Code 内运行、与 Agent 开发同一对话界面、零外部依赖**的 Agent 验证工具。它的价值不是"做得更多"，而是"消除了上下文切换"——开发 Agent 和验证 Agent 在同一个对话中完成。

**不做的事情**（明确边界）:
- 不是生产监控平台（那是 LangSmith/Galileo 的领域）
- 不是安全红队工具（那是 Promptfoo/CheckAgent 的领域）
- 不是全栈评估平台（那是 Future AGI 的领域）
- 不是 SaaS 服务（数据和执行全部本地）

### 1.4 风险清单

#### 技术风险

| 风险 | 严重度 | 概率 | 缓解措施 |
|------|--------|------|----------|
| LLM 裁判评分不一致 | 高 | 中高 | 多模型交叉验证；多次打分取均值；设置方差阈值告警 |
| LLM 裁判成本过高 | 中 | 中 | MVP 不包含 LLM 裁判；仅对断言失败的用例触发裁判打分 |
| 断言 DSL 表达能力不足 | 中 | 低 | 从简单断言类型开始；根据实际用例扩展 |
| 大规模测试套件性能 | 低 | 低 | 文件级 JSONL 已足够百万行；grep 过滤极快 |

#### 采用风险

| 风险 | 严重度 | 概率 | 缓解措施 |
|------|--------|------|----------|
| 开发者为"验证 Agent"编写规范的意愿低 | 高 | 中 | 降低门槛：1 条断言即可起步；claude 帮助写断言 |
| 用户已有测试工具链，不愿切换 | 中 | 中 | 定位为"开发时验证"而非"替代测试工具"；输出格式兼容 |
| Skill 触发不准确导致使用挫折 | 中 | 低 | Description 设计激进（多触发词）；提供手动 `/` 调用入口 |

#### 维护风险

| 风险 | 严重度 | 概率 | 缓解措施 |
|------|--------|------|----------|
| Claude Code Skill 系统 API 变更 | 中 | 低 | Skill 核心逻辑在 scripts/ 中，独立于 Claude Code 版本 |
| LLM 裁判依赖的模型下线或涨价 | 中 | 低 | 模型配置化，允许用户指定裁判模型 |
| 断言引擎成为瓶颈，需要更多规则类型 | 低 | 中 | 插件化断言类型系统；用户可自定义断言函数 |

### 1.5 结论

## Go ✅ — 建议立项

**核心理由**:
1. **需求明确且未被满足**: 99% 组织未评估 Agent，63% 初始失败率，75+ 公司但在 Claude Code 内是空白
2. **技术路径清晰**: 核心组件可实现性 7-9/10，唯一风险点（LLM 裁判）可渐进式引入
3. **差异化充分**: "同一对话界面 + 零外部依赖"是现有 75+ 工具无法提供的体验
4. **MVP 成本极低**: 3 个核心组件（结构化日志 + 断言引擎 + 回归运行），2 周可出原型
5. **战略价值**: 填补 Claude Code 生态中"Agent 开发→验证"闭环的关键缺失

**不做的理由需要**: 团队无 1 人以上投入 OR 目标用户群 < 50 人。当前信息不支撑这两个条件。

---

## 2. Skill 定位与产品定义

### 2.1 Skill 名称建议

| 语言 | 名称 | 说明 |
|------|------|------|
| 英文 | `agent-verify` | 简洁、可搜索、明确职责 |
| 中文 | Agent 验证 | 直译，易于中文社区理解 |
| 备选英文 | `agent-test` | 更贴近 `pytest` 类比，但 `test` 暗示单元测试而本 Skill 覆盖更广（断言 + 评分 + 对比） |
| 备选英文 | `agent-qa` | 短，但 QA 含义过泛 |

**最终建议**: `agent-verify` — 准确描述核心行为（验证 Agent 行为是否正确），与 `test` 区分（`test` 暗示确定性单元测试，`verify` 涵盖断言 + 裁判 + 对比的完整验证流程）。

### 2.2 一句话价值主张

> **Agent 开发的 `pytest` — 在 Claude Code 对话中定义"什么算对"，每次改动自动验证，不再凭感觉判断 Agent 质量。**

### 2.3 一句话价值主张（英文）

> **The pytest for AI Agents — define what "correct" means, verify every change, and stop vibe-checking your agents.**

### 2.4 目标用户画像

#### 画像 A: 独立 Agent 开发者

- **身份**: 用 Claude Code 开发 Agent/Skill 的个人开发者
- **场景**: 新加了一个工具/修改了 prompt/调整了行为策略后，想知道"有没有退化"
- **当前做法**: 手动跑几个例子，盯着输出看，凭感觉判断
- **痛点**: 看不出 subtle regression；重复测试单调枯燥；改了一个 prompt 不知道影响面
- **使用本 Skill 的方式**: 写 3 条断言 → `/agent-verify:regression` → 看通过率

#### 画像 B: 小型 AI 团队（3-10 人）

- **身份**: 用 Claude Code 构建内部 Agent 的工程团队
- **场景**: 多人协作开发 Agent，需要建立质量基线和回归测试
- **当前做法**: Code review 时人工检查 Agent 输出质量，没有自动化验证
- **痛点**: 没有质量基线；不知道 PR 是否引入退化；无法量化迭代效果
- **使用本 Skill 的方式**: 建立回归测试套件 → CI 集成 → 每个 PR 自动验证

#### 画像 C: AI 产品经理/QA

- **身份**: 负责 Agent 质量但不会写代码的 PM/QA
- **场景**: 需要检查 Agent 的行为是否符合产品预期
- **当前做法**: 打开 Agent 测试页面，手动测试，截图记录
- **痛点**: 测试案例无法复用；难以量化质量变化；回归测试耗时极长
- **使用本 Skill 的方式**: 用自然语言描述预期 → `claude` 帮助生成断言 → 一键回归

### 2.5 核心解决的问题（量化）

| 问题 | 当前状态 | 使用后的改善 |
|------|----------|-------------|
| **Agent 行为退化检测** | 靠人工感觉（~0% 自动化） | 确定性断言自动检测，秒级反馈 |
| **prompt 修改影响面评估** | 无法评估（"改完不知道变好还是变坏"） | A/B 对比报告，量化每个维度的变化（± 分数） |
| **回归测试覆盖** | 无（每次手动测几个例子） | 可积累的测试套件，随时间增长覆盖 |
| **新功能验证** | 手动测试（10-30 分钟/功能） | 半自动化（5 分钟写断言 + 自动执行） |
| **质量基线建立** | 无基线（"不知道现在质量是什么水平"） | 首次运行即建立可量化的基线快照 |

### 2.6 不解决的问题（明确边界）

| 问题 | 为什么不做 | 替代方案 |
|------|-----------|----------|
| **生产环境 Agent 监控** | 需要持久化基础设施（数据库、仪表盘、告警通道） | LangSmith / Galileo / Langfuse |
| **安全红队测试** | 需要大量攻击向量库 + 专业安全知识 | Promptfoo / CheckAgent |
| **RAG 检索质量专项评估** | RAG 评估有成熟工具（Ragas 等），复制价值低 | Ragas / DeepEval |
| **多模态 Agent 评估（视频/图像）** | 当前 Skill 系统 + LLM 能力支撑不足 | 专项工具或未来版本 |
| **Agent 性能/成本优化** | 属于可观测性而非验证 | LangSmith / Arize Phoenix |
| **为第三方 Agent 平台提供测试服务** | 定位为 Claude Code Skill，不做 SaaS | — |
| **Codex 闭环自我修复** | 研究阶段，风险极高，MVP 不做 | 未来版本（V2.0+）探索 |

---

## 3. 命令体系设计

### 3.1 核心命令列表

#### `/agent-verify:init` — 初始化验证套件

| 属性 | 值 |
|------|-----|
| **触发条件** | 用户首次使用验证功能; 用户明确说"初始化验证"/"setup verification"/"建立测试" |
| **参数** | `--target` (可选): 要验证的 Agent/Skill 名称 |
| **行为** | 1. 在当前目录创建 `agent-verify/` 目录结构；2. 生成默认配置文件（`suite.yaml`）；3. 引导用户定义第一个断言；4. 输出初始化完成报告 |
| **输出** | 目录结构确认 + 下一步建议（"请定义你的第一条断言"） |
| **示例对话** | "给我的 search-agent 初始化验证套件" |

#### `/agent-verify:assert` — 定义/管理断言

| 属性 | 值 |
|------|-----|
| **触发条件** | 用户说"加一条断言"/"define assertion"/"添加规则"/"检查是否调用了某工具"/"验证输出包含" |
| **参数** | `--add`: 添加新断言（交互式); `--list`: 列出所有断言; `--remove <id>`: 删除断言; `--run`: 立即执行所有断言 |
| **行为** | 1. 引导用户选择断言类型（工具调用/参数/状态/路径/输出/时间）; 2. 收集断言条件; 3. 写入断言配置文件; 4. 可选的立即运行 |
| **输出** | 断言定义确认 + 当前运行结果（如果 `--run`） |
| **示例对话** | "加一条断言：search_tool 必须被调用至少一次" |

#### `/agent-verify:regression` — 运行回归测试

| 属性 | 值 |
|------|-----|
| **触发条件** | 用户说"跑回归"/"run regression"/"验证有没有退化"/"测试一下"/"检查质量" |
| **参数** | `--suite <name>`: 指定测试套件; `--scope <all|changed>`: 全量或增量; `--compare <baseline>`: 与指定基线对比 |
| **行为** | 1. 对指定测试套件中的每条用例执行 Agent；2. 收集结构化日志；3. 运行断言引擎；4. (可选) 触发 LLM 裁判打分；5. 生成回归报告 |
| **输出** | 断言通过/失败统计 + LLM 评分变化（如有）+ 回归警告 |
| **示例对话** | "跑一下全量回归，看看有没有退化" |

#### `/agent-verify:compare` — A/B 对比

| 属性 | 值 |
|------|-----|
| **触发条件** | 用户说"对比一下"/"比较新旧版本"/"A/B test"/"这个改动效果如何" |
| **参数** | `--flag <name>`: Feature Flag 名称; `--baseline <name>`: 基线名称; `--suite <name>`: 测试套件 |
| **行为** | 1. Flag=OFF 运行全量测试 → 基线数据；2. Flag=ON 运行全量测试 → 新版本数据；3. 逐维度 diff；4. 生成对比报告 |
| **输出** | 对比表格 + 变好/变坏明细 + 结论建议 |
| **示例对话** | "对比一下 enable_chain_of_thought_v2 开关的效果" |

#### `/agent-verify:baseline` — 质量基线管理

| 属性 | 值 |
|------|-----|
| **触发条件** | 用户说"建立基线"/"保存当前分数"/"baseline snapshot"/"记录当前质量水平" |
| **参数** | `--save <name>`: 保存当前基线; `--list`: 列出所有基线; `--compare <name1> <name2>`: 对比两个基线 |
| **行为** | 1. 运行全量测试；2. 记录所有指标快照；3. 保存为命名基线文件 |
| **输出** | 基线报告 + 基线文件路径 |
| **示例对话** | "建立一个基线叫 v1.0-release" |

#### `/agent-verify:suite` — 测试套件管理

| 属性 | 值 |
|------|-----|
| **触发条件** | 用户说"管理测试用例"/"添加测试用例"/"整理测试套件" |
| **参数** | `--add`: 添加测试用例（交互式）; `--list`: 列出所有用例; `--import <file>`: 从文件导入; `--export <file>`: 导出; `--generate`: 从功能描述 AI 生成用例 |
| **行为** | 1. 引导定义测试用例（输入 + 预期路径 + 断言）; 2. 保存到套件文件; 3. 可选：AI 辅助生成 |
| **输出** | 测试用例定义确认 |
| **示例对话** | "加一个测试用例：用户搜索最新的 AI 新闻" |

#### `/agent-verify:report` — 生成验证报告

| 属性 | 值 |
|------|-----|
| **触发条件** | 用户说"生成报告"/"出个报告"/"验证报告" |
| **参数** | `--format <markdown|json|html>`: 输出格式; `--scope <latest|all>`: 最近一次还是全部历史 |
| **行为** | 1. 聚合断言结果 + LLM 评分 + A/B 对比数据；2. 按格式生成报告 |
| **输出** | 完整验证报告文件 |
| **示例对话** | "把这次的回归测试结果生成一份 markdown 报告" |

### 3.2 命令协作关系

```
/agent-verify:init          # 一次性初始化
    │
    ├── /agent-verify:assert      # 定义断言（持续使用）
    │       │
    ├── /agent-verify:suite       # 管理测试用例（持续使用）
    │       │
    ├── /agent-verify:baseline    # 建立基线（里程碑节点使用）
    │       │
    ├── /agent-verify:regression  # 日常回归（最频繁使用）
    │       │
    │       └── /agent-verify:compare   # A/B 对比（新功能上线前使用）
    │
    └── /agent-verify:report      # 生成报告（按需使用）
```

**典型使用频率**:
- `:regression` — 每次修改后（每日多次）
- `:assert` — 新功能开发时（每周 2-5 次）
- `:suite` — 新测试用例时（每周 1-3 次）
- `:compare` — 新功能上线前（每月 2-4 次）
- `:baseline` — 版本发布时（每月 1-2 次）
- `:report` — 需要分享质量状况时（按需）

### 3.3 典型用户对话流程

#### 场景 A: 首次建立验证体系（新用户 Onboarding）

```
👤 用户: "帮我给我的 agent 建立验证体系"

🤖 Claude: "好的。我会初始化 agent-verify 验证套件。
你的 Agent 是什么类型的？（选择或描述）
1. 对话式 Agent（用户聊天→Agent 响应）
2. 工具调用 Agent（用户任务→Agent 调用工具→返回结果）
3. 多步工作流 Agent（复杂任务，多个阶段）"

👤 用户: "2，工具调用型。我有个 search-agent，用户问问题，它搜索然后总结"

🤖 Claude: "明白了。我先初始化验证套件。[调用 init]

✅ 验证套件已初始化：`./agent-verify/`
📁 目录结构：suites/ assertions/ baselines/ config.yaml

接下来，我帮你写第一条断言。请描述一件你的 Agent '必须做到'的事情。
例如：'search_tool 必须被调用' 或 '输出必须包含引用来源'"

👤 用户: "必须调用 search_tool 至少一次"

🤖 Claude: "已添加断言 #1: `tool_called: search_tool, min_count: 1`

还想再加几条吗？建议覆盖以下方面：
- 工具参数正确性（如 search query 不能为空）
- 输出格式（如必须包含引用链接）
- 关键步骤覆盖（如必须先搜索再总结）
或者可以先跑一次看看效果 → `/agent-verify:regression`"

👤 用户: "先跑一次看看"

🤖 Claude: "[执行回归测试...]

📊 第一次验证结果
━━━━━━━━━━━━━━━━━━━━━
测试用例: 1 (默认 Happy Path)
断言通过: 1/1 (100%)
LLM 裁判: 未启用
━━━━━━━━━━━━━━━━━━━━━
✅ 断言全部通过！

建议下一步：
1. 加更多测试用例 → `/agent-verify:suite --add`
2. 建立基线 → `/agent-verify:baseline --save initial`
3. 启用 LLM 裁判打分 → 在 config.yaml 中配置"
```

#### 场景 B: 日常开发 — 修改 prompt 后验证

```
👤 用户: "我改了 search-agent 的 prompt，帮我验证有没有退化"

🤖 Claude: "好的。我先看看你有没有保存基线...
发现基线 `v1.0-release`（3天前保存）。

现在用当前 prompt 跑全量回归测试并与基线对比。"

[执行中...]

📊 回归对比报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
对比: 当前 vs 基线 `v1.0-release`
测试套件: 8 条用例

确定性断言:
  当前: 7/8 (87.5%)   基线: 8/8 (100%)   ⚠️ -1

LLM 评分:
  准确性: 7.2 → 7.8 (+0.6) ✅
  完整性: 6.8 → 5.1 (-1.7) ⚠️
  合理性: 7.5 → 7.6 (+0.1) —
  工具使用: 8.1 → 7.9 (-0.2) —
  综合: 7.3 → 6.8 (-0.5) ⚠️

⚠️ 发现回归:
1. `error_handling_003` — 断言 FAIL: "error_handler 未被调用"
   新 prompt 中删除了错误处理指引，导致 Agent 在超时场景不再调用 error_handler
2. 完整性评分下降 1.7 — 新 prompt 更简洁但也遗漏了部分上下文

💡 建议:
- 恢复 error_handler 调用指引，或更新断言
- 检查 prompt 中是否遗漏了完整性相关的上下文"
```

#### 场景 C: 新功能上线前 — Feature Flag A/B 对比

```
👤 用户: "我做了个新的 chain-of-thought 推理策略，用 feature flag 控制。
帮我跑 A/B 对比看看效果"

🤖 Claude: "好的。我看到你配置了 feature flag `enable_cot_v2`。

即将运行：
- Flag=OFF (旧策略) → 基线
- Flag=ON  (新策略) → 对比

测试套件将使用 `full-suite`（12 条用例）。
LLM 裁判已启用（模型: claude-sonnet）。

开始运行..."

[约 3-5 分钟后...]

📊 A/B 对比报告: enable_cot_v2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| 维度 | OFF (旧) | ON (新) | 变化 |
|------|----------|---------|------|
| 断言通过率 | 11/12 (92%) | 12/12 (100%) | +8% ✅ |
| LLM 准确性 | 7.2 | 8.5 | +1.3 ✅ |
| LLM 完整性 | 6.8 | 7.4 | +0.6 ✅ |
| LLM 合理性 | 7.5 | 8.9 | +1.4 ✅ |
| LLM 工具使用 | 8.1 | 8.3 | +0.2 — |
| 综合评分 | 7.3 | 8.2 | +0.9 ✅ |
| 平均执行步数 | 5.2 | 6.8 | +1.6 ⚠️ |
| 平均耗时 | 12.3s | 18.7s | +6.4s ⚠️ |

✅ 全面正向！
- 准确性 +1.3，推理质量明显提升
- 之前 `complex_query_007` 的断言失败已修复

⚠️ 注意:
- 执行步数增加 30%，耗时增加 52%
- 对于简单查询场景（simple_query_001-003），CoT 可能过度推理

💡 建议:
- ✅ 对复杂查询场景启用 CoT（效果显著提升）
- 🔧 考虑对简单查询场景跳过 CoT（增加 latency 检查逻辑）
- 📝 记录此次对比结果供后续参考"
```

---

## 4. 技术架构

### 4.1 Skill 文件结构

```
agent-verify/
├── SKILL.md                        # 主技能文件 (~400行)
│
├── scripts/                        # 可执行脚本（不读入上下文，通过 Bash 执行）
│   ├── parse_log.py               # 结构化日志解析器
│   ├── assertion_engine.py        # 确定性断言引擎
│   ├── regression_runner.py       # 回归测试编排器
│   ├── ab_comparator.py           # A/B 对比报告生成器
│   ├── baseline_manager.py        # 基线管理
│   └── report_generator.py        # 综合报告生成器
│
├── references/                     # 按需加载的文档（Claude Read 触发）
│   ├── assertion-types.md         # 断言类型详细说明（6种类型 + 示例）
│   ├── scoring-rubric.md          # LLM 裁判评分维度与 rubric 设计指南
│   ├── config-reference.md        # 配置文件完整参考（每个字段的含义）
│   ├── workaround-patterns.md     # 常见场景的断言编写模式（10+ 模式）
│   └── integration-guide.md       # 与 CI/CD 集成的步骤说明
│
├── templates/                      # 输出模板（生成到用户项目，不读入上下文）
│   ├── suite-template.yaml        # 空测试套件模板
│   ├── config-template.yaml       # 默认配置文件模板
│   ├── test-case-template.yaml    # 测试用例定义模板
│   └── baseline-template.json     # 基线快照格式模板
│
└── examples/                       # 示例文件（供参考，不参与执行）
    ├── example-search-agent/       # 搜索 Agent 的完整验证示例
    │   ├── suite.yaml
    │   ├── assertions.yaml
    │   └── baseline-v1.json
    └── example-chat-agent/        # 对话 Agent 的完整验证示例
        ├── suite.yaml
        └── assertions.yaml
```

**设计理由**:
- `scripts/` 而非 `references/` 放置引擎代码：脚本通过 Bash 执行不占用上下文，这是 Skill 系统的最佳实践
- `templates/` 而非 `assets/`：这些是"给用户生成的文件模板"，更符合 `templates` 语义
- `examples/` 目录：Skill 规范不建议在 Skill 内部放文档文件，但示例是学习最佳方式。放在 Skill 目录内作为 templates 的镜像
- SKILL.md 控制在 ~400 行：核心工作流和命令编排在 SKILL.md 中，详细参考在 references/ 中

### 4.2 核心模块划分

```
                    ┌──────────────────────────┐
                    │     SKILL.md (编排层)      │
                    │  命令路由 + 工作流编排     │
                    └──────┬─────────┬─────────┘
                           │         │
              ┌────────────┘         └────────────┐
              ▼                                   ▼
    ┌─────────────────┐                 ┌─────────────────┐
    │  Agent 执行层    │                 │  验证执行层      │
    └────────┬────────┘                 └────────┬────────┘
             │                                   │
    ┌────────┴────────┐                 ┌────────┴────────┐
    │ 1. Agent CLI    │                 │ 3. 断言引擎      │
    │    Wrapper      │                 │ assertion_engine │
    │ (claude bash)   │                 │     .py          │
    └────────┬────────┘                 └────────┬────────┘
             │                                   │
             ▼                                   ▼
    ┌─────────────────┐                 ┌─────────────────┐
    │ 2. 结构化日志    │                 │ 4. LLM 裁判      │
    │   parse_log.py  │                 │ (Claude API)     │
    └────────┬────────┘                 └────────┬────────┘
             │                                   │
             │                                   │
             └───────────────┬───────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  聚合 & 报告     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
    ┌──────────────┐ ┌────────────┐ ┌──────────────┐
    │ 5. 回归运行器 │ │ 6. A/B对比 │ │  7. 基线管理  │
    │ regression_  │ │ ab_compar- │ │  baseline_    │
    │ runner.py    │ │ ator.py    │ │  manager.py   │
    └──────────────┘ └────────────┘ └──────────────┘
```

**模块职责**:

| # | 模块 | 脚本 | 职责 |
|---|------|------|------|
| 1 | Agent CLI Wrapper | (Claude 直接调用) | 通过 Bash 执行 Agent，收集输出和日志 |
| 2 | 结构化日志解析 | `parse_log.py` | 从 Agent 运行日志中提取结构化事件流 |
| 3 | 断言引擎 | `assertion_engine.py` | 加载断言配置，对日志执行确定性检查，输出 Pass/Fail + 原因 |
| 4 | LLM 裁判 | (Claude API 直接调用) | 基于评分标准，对 Agent 输出进行多维度量化打分 |
| 5 | 回归运行器 | `regression_runner.py` | 遍历测试套件中的用例，依次执行 Agent + 断言 + 裁判 |
| 6 | A/B 对比器 | `ab_comparator.py` | 对两份运行结果进行逐维度 diff |
| 7 | 基线管理器 | `baseline_manager.py` | 保存/加载/对比质量基线快照 |

### 4.3 数据流设计

```
用户触发 /agent-verify:regression
        │
        ▼
┌──────────────────────────────────────────────┐
│ regression_runner.py                         │
│                                              │
│  for each test_case in suite.yaml:           │
│    ┌──────────────────────────────────────┐  │
│    │ 1. 注入结构化日志指令到 Agent prompt  │  │
│    │ 2. 执行 Agent (Bash: claude ...)      │  │
│    │    └── 输出: raw_output.md            │  │
│    │ 3. parse_log.py 解析日志              │  │
│    │    └── 输出: trace.jsonl              │  │
│    │ 4. assertion_engine.py 执行断言       │  │
│    │    └── 输出: assertion_result.json    │  │
│    │ 5. (可选) LLM 裁判评分                │  │
│    │    └── 输出: judge_scores.json        │  │
│    │ 6. 聚合该用例的全部结果               │  │
│    │    └── 输出: case_result.json         │  │
│    └──────────────────────────────────────┘  │
│                                              │
│  汇总所有 case_result.json                   │
│  ├── 断言通过率统计                          │
│  ├── LLM 评分均值 & 方差                     │
│  └── 回归检测 (与上一基线对比)               │
│                                              │
│  输出: regression_report.md                  │
└──────────────────────────────────────────────┘
```

**关键文件流转**:

```
Agent 运行
  │
  ├── raw_output.md           # Agent 的完整文本输出
  ├── trace.jsonl             # 结构化事件流（供断言消费）
  ├── assertion_result.json   # 断言检查结果
  ├── judge_scores.json       # LLM 裁判评分
  └── case_result.json        # 单个用例的综合结果

全量结果
  │
  ├── regression_report.md    # 人类可读报告
  ├── scores_history.jsonl    # 历史评分记录（供趋势分析）
  └── baseline_snapshots/     # 基线快照目录
```

### 4.4 配置文件格式

#### 4.4.1 断言定义文件 (`assertions.yaml`)

```yaml
# agent-verify/assertions.yaml
# 断言定义文件 — 描述"什么算对"

version: "1.0"

assertions:
  - id: "search-tool-called"
    name: "搜索工具必须被调用"
    description: "确保 Agent 在处理信息查询时实际调用了搜索工具"
    type: tool_call                    # 断言类型
    target:
      tool_name: "search"             # 目标工具名
    condition:
      min_count: 1                    # 最少调用次数
    severity: error                   # error | warning
    enabled: true

  - id: "search-query-not-empty"
    name: "搜索查询参数不能为空"
    description: "search 工具的 query 参数必须包含有意义的文本"
    type: tool_param
    target:
      tool_name: "search"
      param_name: "query"
    condition:
      min_length: 3                   # 最少字符数
      not_null: true
      not_whitespace_only: true
    severity: error
    enabled: true

  - id: "output-has-citations"
    name: "输出必须包含引用来源"
    description: "最终输出中必须包含信息来源的引用"
    type: output_match
    target:
      field: "final_output"           # 匹配目标字段
    condition:
      pattern: "(来源|参考|引用|source|reference|citation)"
      min_matches: 1
      case_sensitive: false
    severity: error
    enabled: true

  - id: "plan-execute-verify-path"
    name: "工作流必须经过计划→执行→验证"
    description: "多步任务应遵循标准三阶段工作流"
    type: path_sequence
    target:
      step_types: ["planning", "execution", "verification"]
    condition:
      order: "strict"                 # strict | relaxed
      all_present: true
    severity: warning
    enabled: true

  - id: "step-timeout-limit"
    name: "单步执行时间不超过30秒"
    description: "任何单个 tool_call 步骤不应超过 30 秒"
    type: timing
    target:
      step_type: "tool_call"
    condition:
      max_duration_ms: 30000
    severity: warning
    enabled: true

  - id: "output-valid-json"
    name: "输出必须是有效 JSON"
    description: "当任务要求 JSON 输出时，验证格式正确"
    type: output_schema
    target:
      field: "final_output"
    condition:
      schema:                         # JSON Schema 验证
        type: "object"
        required: ["answer", "sources"]
        properties:
          answer:
            type: "string"
          sources:
            type: "array"
            minItems: 1
    severity: error
    enabled: true
```

#### 4.4.2 测试套件文件 (`suite.yaml`)

```yaml
# agent-verify/suites/search-agent.yaml
# 测试套件 — 定义测试用例集合

suite:
  name: "search-agent-full-suite"
  description: "Search Agent 的完整回归测试套件"
  version: "1.0"
  created: "2026-06-30"

  # 全局配置
  defaults:
    agent_command: "claude --skill search-agent --print"  # Agent 执行命令
    timeout: 120                                            # 单用例超时（秒）
    assertions_file: "../assertions.yaml"                   # 断言文件路径
    enable_llm_judge: true                                  # 是否启用 LLM 裁判
    judge_model: "claude-haiku"                             # 裁判模型（与开发模型区分）

  # 测试用例
  test_cases:
    - id: "simple-search-001"
      name: "简单信息查询"
      description: "用户询问一个可以直接搜索到的事实问题"
      input: "2024 年诺贝尔物理学奖得主是谁？"
      assertions:                           # 该用例特定的断言（覆盖全局）
        - "search-tool-called"
        - "search-query-not-empty"
        - "output-has-citations"
      expected_path:                        # 预期执行路径（可选，供 LLM 裁判使用）
        - "理解用户查询意图"
        - "调用 search 工具搜索诺贝尔物理学奖"
        - "整合搜索结果，提取获奖者信息"
        - "输出带引用的答案"
      quality_criteria:                     # LLM 裁判评分标准
        accuracy: "获奖者姓名和国籍必须正确"
        completeness: "应覆盖诺贝尔物理学奖的获奖者及其获奖理由"
        risk: "不应编造不存在的获奖者或错误信息"
      tags: ["happy-path", "smoke-test"]

    - id: "complex-multi-hop-002"
      name: "多跳复杂查询"
      description: "需要多次搜索才能回答的复杂问题"
      input: "对比 2024 年诺贝尔物理学奖和化学奖得主的研究方向有什么共同点"
      assertions:
        - "search-tool-called"
        - "output-has-citations"
      expected_path:
        - "理解查询的两个子问题"
        - "搜索诺贝尔物理学奖得主信息"
        - "搜索诺贝尔化学奖得主信息"
        - "比较两个奖项得主的研究方向"
        - "总结共同点并引用来源"
      quality_criteria:
        accuracy: "两个奖项的获奖者信息必须正确"
        completeness: "必须覆盖物理奖和化学奖两方面，且有对比分析"
        reasoning: "共同点的推理应基于实际研究方向，自洽"
      tags: ["happy-path", "multi-hop"]

    - id: "error-timeout-003"
      name: "搜索超时错误处理"
      description: "当搜索工具不可用或超时时，Agent 应优雅降级"
      input: "搜索最新的 AI 新闻"           # 配合 mock 搜索工具触发超时
      assertions:
        - "output-has-citations"             # 此时引用可能来自内部知识
      # 注意：该用例需要配合 feature flag 或 mock 工具模拟搜索超时
      expected_path:
        - "尝试调用 search 工具"
        - "检测到搜索不可用或超时"
        - "使用内部知识回答（优雅降级）"
        - "告知用户搜索不可用"
      quality_criteria:
        risk: "不应假装搜索成功或编造不存在的搜索结果"
        robustness: "应在搜索失败后仍提供有价值的回答"
      tags: ["error-handling", "resilience"]

    - id: "edge-empty-query-004"
      name: "空查询边界测试"
      description: "用户发送的消息不包含实际信息需求"
      input: "..."
      assertions:
        - "search-tool-called"
          enabled: false                    # 该用例中，这条断言反而不应该通过
      additional_assertions:               # 该用例特有的断言
        - id: "no-search-for-empty-query"
          name: "空查询不应触发搜索"
          type: tool_call
          target:
            tool_name: "search"
          condition:
            max_count: 0
          severity: error
      quality_criteria:
        reasonableness: "Agent 应对空查询做出合理的回应（如询问澄清），而不是盲目搜索"
      tags: ["edge-case", "negative-test"]

  # 测试分组（便于增量运行）
  groups:
    smoke:
      - "simple-search-001"
    full:
      - "simple-search-001"
      - "complex-multi-hop-002"
      - "error-timeout-003"
      - "edge-empty-query-004"
```

#### 4.4.3 Feature Flag 配置文件 (`config.yaml`)

```yaml
# agent-verify/config.yaml
# 全局配置文件

version: "1.0"

# Agent 执行配置
execution:
  default_command: "claude --print"     # 默认 Agent 执行命令
  timeout: 120                           # 单用例超时（秒）
  env:                                   # 环境变量注入
    AGENT_VERIFY_MODE: "true"           # Agent 可通过此变量感知验证模式

# 断言引擎配置
assertions:
  file: "assertions.yaml"               # 断言定义文件
  stop_on_first_error: false            # 遇到第一个错误是否停止
  fail_fast_threshold: 0.5              # 失败率超过 50% 时提前终止

# LLM 裁判配置
llm_judge:
  enabled: false                         # MVP 阶段默认关闭
  model: "claude-haiku"                 # 裁判模型（必须与开发模型不同）
  dimensions:                           # 评分维度
    - accuracy                           # 准确性
    - completeness                       # 完整性
    - reasonableness                     # 合理性
    - tool_usage                         # 工具使用质量
    - risk_awareness                     # 风险意识
  scoring:
    range: [1, 10]                      # 评分范围
    runs: 3                             # 重复打分次数（取均值）
    max_variance: 1.5                   # 方差超过此值触发警告
  cost_control:
    max_tokens_per_eval: 2000           # 单次评估最大 token
    max_monthly_budget_usd: 50          # 月度预算上限

# Feature Flag 配置
feature_flags:
  # 每个 Flag 定义为一个环境变量前缀
  # 运行时通过 AGENT_FLAG_<NAME>=ON|OFF 控制
  storage: env                          # env | file | both
  file_path: "flags.yaml"              # 当 storage=file 时的文件路径
  flags:
    - name: "enable_cot_v2"
      description: "启用新版 Chain-of-Thought 推理策略"
      default: false
    - name: "enable_new_search_tool"
      description: "启用新版搜索工具（替代旧版）"
      default: false
    - name: "max_search_results"
      description: "搜索结果最大返回数"
      default: 10
      type: number
      range: [5, 30]

# 基线管理
baselines:
  directory: "baselines/"               # 基线文件存储目录
  auto_save_on_regression: false        # 每次回归测试后是否自动保存基线

# 报告配置
reports:
  default_format: markdown              # markdown | json | html
  output_directory: "reports/"          # 报告输出目录
  include_traces: false                 # 是否在报告中包含完整执行轨迹

# 覆盖率配置（MVP 之后启用）
coverage:
  enabled: false                         # V1.0 之后启用
  dimensions:
    - functional                         # 功能覆盖
    - tool                               # 工具覆盖
    - path                               # 路径覆盖
    - input_type                        # 输入类型覆盖
```

#### 4.4.4 结构化日志格式 (`trace.jsonl`)

每行一个 JSON 事件：

```jsonl
{"run_id":"uuid-1","seq":0,"ts":"2026-06-30T12:00:00Z","type":"run_start","input":"用户输入文本","flags":{"enable_cot_v2":false}}
{"run_id":"uuid-1","seq":1,"ts":"2026-06-30T12:00:01Z","type":"llm_response","content":"我理解你需要搜索...","step":"planning"}
{"run_id":"uuid-1","seq":2,"ts":"2026-06-30T12:00:03Z","type":"tool_call","tool_name":"search","input":{"query":"诺贝尔物理学奖 2024"},"output":{"results_count":5,"results":[...]}}
{"run_id":"uuid-1","seq":3,"ts":"2026-06-30T12:00:05Z","type":"state_change","key":"search_results_count","value":5}
{"run_id":"uuid-1","seq":4,"ts":"2026-06-30T12:00:07Z","type":"llm_response","content":"根据搜索结果...","step":"execution"}
{"run_id":"uuid-1","seq":5,"ts":"2026-06-30T12:00:08Z","type":"run_end","final_output":"2024年诺贝尔物理学奖得主是...","total_steps":6,"total_duration_ms":8000}
```

### 4.5 与 Claude Code 现有系统的集成点

| 集成点 | 方式 | 说明 |
|--------|------|------|
| **Skill 系统** | SKILL.md + scripts/ + references/ | 本 Skill 本身就是标准 Skill，无特殊集成需求 |
| **Claude API (LLM 裁判)** | 内建 `claude` 调用 | 裁判评分直接调用 Claude API（与开发模型不同的模型） |
| **Agent 执行** | Bash 工具 + `claude --print` | 通过 CLI 执行被验证的 Agent，收集输出 |
| **文件系统** | 读/写 ./agent-verify/ | 配置、断言、基线、报告均存储在项目本地的 agent-verify/ 目录中 |
| **环境变量** | `AGENT_FLAG_*` | Feature Flag 通过环境变量注入，被验证的 Agent 读取判断 |
| **结构化日志** | 提示词注入 | 在被验证 Agent 的系统 prompt 中注入日志格式要求 |
| **权限** | `allowed-tools` | 声明 Bash/Read/Write/Edit 权限，避免运行时弹窗 |

---

## 5. 关键设计决策

### 5.1 断言引擎用声明式配置还是代码式？

**决策: 声明式 YAML 配置**

| 对比维度 | 声明式 (YAML) | 代码式 (Python/JS) |
|----------|--------------|-------------------|
| 学习成本 | 低（5分钟看懂） | 中（需要编程能力） |
| 表达力 | 中（6 种断言类型覆盖 80% 场景） | 高（任意逻辑） |
| 可维护性 | 高（格式统一，可自动格式化） | 中（代码风格因人而异） |
| 可共享性 | 高（纯数据文件，跨语言） | 低（绑定语言运行时） |
| 版本管理 | 高（文本 diff 友好） | 中（diff 但语义理解需人工） |
| 错误风险 | 低（Schema 验证，不会运行时崩溃） | 中（代码中的 bug 风险） |
| 适用场景 | 确定性规则检查 | 复杂自定义逻辑 |

**理由**: 
1. 目标用户包含非程序员（PM/QA），YAML 门槛最低
2. 6 种断言类型（tool_call / tool_param / output_match / path_sequence / timing / output_schema）覆盖了视频方法论中的全部硬性检查需求
3. 若用户确实需要复杂逻辑，提供 `type: custom_script` 扩展点，引用 `scripts/` 中的自定义脚本

**扩展路径**: 当 6 种预设类型不够用时，用户可编写 `scripts/custom_assertion.py` 并指定 `type: custom_script, script: "custom_assertion.py"`

### 5.2 LLM 裁判用哪个模型？如何保证可靠性？

**决策: 低成本快速模型为主裁判，高成本模型为仲裁**

| 角色 | 模型 | 原因 |
|------|------|------|
| **主裁判** (日常使用) | `claude-haiku` | 成本低、速度快、对简单评估足够可靠 |
| **仲裁裁判** (争议时) | `claude-sonnet` | 评分方差更小、推理更深 |
| **交叉验证** (关键决策) | `claude-sonnet` + `gpt-4o-mini` | 模型多样性降低系统性偏差 |

**可靠性保证机制**:
1. **多次打分取均值**: 同一输出打分 3 次，记录均值和方差
2. **方差阈值告警**: 若 3 次评分的标准差 > 1.5，触发"裁判不一致"告警，建议人工审查
3. **锚定校准（参考答案锚点）**: 在裁判 prompt 中嵌入 1-2 个"参考答案"作为评分参照系，让 LLM 裁判的输出分数有一个共同基准，减少不同裁判任务之间的相对偏差。

   **参考答案锚点机制**:

   在每次裁判调用时，prompt 中附上两种类型的参考答案：

   ```yaml
   calibration_examples:
     - type: good_output
       description: "高质量输出的参考示例"
       agent_output: "2024年诺贝尔物理学奖授予John Hopfield和Geoffrey Hinton，表彰他们在人工神经网络和机器学习方面的基础性发现。来源：[诺贝尔官网](https://nobelprize.org/physics2024)"
       scores:
         accuracy: 9
         completeness: 8
         reasonableness: 9
       justification: "事实正确、引用来源、结构清晰。扣分原因：缺少获奖理由的简要说明。"
     
     - type: bad_output
       description: "低质量输出的参考示例"
       agent_output: "2024年诺贝尔物理学奖得主在物理学领域做出了重要贡献。"
       scores:
         accuracy: 3
         completeness: 2
         reasonableness: 4
       justification: "回答过于模糊、未给出具体名字、未提供引用、信息量严重不足。"
   ```

   **工作原理**:
   - 参考答案嵌入系统 prompt 中，作为评分尺度的"锚点"——裁判在打分时以这些示例为参照系，而非凭空给出绝对分数
   - `good_output` 锚定了"高分应该长什么样"，`bad_output` 锚定了"低分的特征"
   - 参考答案与当前评估任务同领域（如都是"搜索回答评估"），确保语义空间一致性
   - 每次裁判运行都带上相同的参考答案，使得不同任务、不同时间的评分具有可比性

   **实现位置**: 参考答案定义存储在 `references/scoring-rubric.md` 中，裁判 prompt 构建时动态拼接。每类评估任务（搜索、对话、工具调用等）可定义独立的参考答案对。

4. **上下文隔离**: 裁判只看到"任务描述 + Agent 输出 + 评分标准 + 参考答案"，不知道实现细节
5. **成本控制**: 默认使用 haiku，月度预算上限 $50

**为什么不直接用 claude-sonnet？**
- Haiku 对简单的"这个回答是否包含事实错误"型评估已足够可靠
- 成本差异显著（haiku ~$1/M input tokens vs sonnet ~$3/M）
- 大规模回归测试时（20+ 用例 × 5 维度 × 3 次），成本差异会被放大 300 倍

**为什么不是完全不做 LLM 裁判？**
- 断言只能覆盖 30-50% 的质量问题（硬性规则）
- "回答是否合理""推理是否自洽"这类模糊判断只能由 LLM 处理
- MVP 可以不做，但 V1.0 必须有

### 5.3 回归测试套件如何管理？

**决策: YAML 文件 + Git 版本控制 + JSONL 历史记录**

```
agent-verify/
├── suites/
│   ├── search-agent.yaml        # 搜索 Agent 的测试套件
│   ├── chat-agent.yaml          # 对话 Agent 的测试套件
│   └── critical-path.yaml       # 关键路径最小验证集（所有 Agent 共用）
├── history/
│   ├── runs.jsonl               # 每次运行的历史记录（附：时间、结果摘要、git commit hash）
│   └── scores_history.jsonl     # 每个用例的评分变化趋势
├── baselines/
│   ├── v1.0-release.json        # 基线快照
│   └── v1.1-release.json
```

**管理策略**:
1. **套件文件存 Git**: `suites/*.yaml` 与 Agent 代码同仓库，随代码演进
2. **历史记录本地**: `history/` 加入 `.gitignore`，避免仓库膨胀
3. **基线随版本 tag**: 每次发布时保存基线，`v1.0-release.json` 对应 git tag
4. **增量而非替换**: 新功能增加新测试用例，不修改已有用例的预期（除非行为有意变更）

**`history/` 目录的演进路线**:

`history/` 目录在 V1.0 之前不会默认创建。其演进路径如下：

| 阶段 | 如何满足 "历史记录" 需求 | 原因 |
|------|--------------------------|------|
| **MVP** | 使用 `reports/` + `baselines/` 替代 | MVP 阶段用户需求是"当前通过率"和"与上次对比"：`reports/` 保存每次回归的报告文件，`baselines/` 保存基线快照，两个目录即可覆盖需求。避免在验证体系尚未稳定时引入额外的目录结构 |
| **V1.0** | 引入 `history/runs.jsonl` | 当用户开始频繁跑回归（每日多次）且有趋势分析需求时，`history/runs.jsonl` 提供轻量级的运行历史记录。每行一条运行记录，含时间戳、用例 ID、通过率、评分摘要、git commit hash。不要求结构化查询，grep 即可检索 |
| **V2.0+** | `scores_history.jsonl` 支持趋势图 | 新文件记录每个用例每次运行的 LLM 评分变化，供趋势 Dashboard 使用。此时 JSONL 文件可能需要引入索引或迁移到 SQLite |

**为什么 MVP 不直接创建 `history/`？**
- 减少目录数量，降低用户认知负担
- 避免"空目录"困惑（刚 init 时 history/ 是空的，用户不知道用途）
- 在 `reports/` 中已有回归报告 = 隐式历史记录
- 遵循"刚到需要时再引入"的演进原则

**为什么不用数据库？**
- MVP 阶段零基础设施需求
- JSONL + grep 足以满足千级用例的查询需求
- Git 天然提供版本管理和协作
- V2.0 后可考虑 SQLite（当用例 > 500 条且查询性能成为瓶颈时）

### 5.4 Feature Flag 如何实现（在无原生支持的环境下）？

**决策: 环境变量注入 + YAML 配置文件（双通道）**

**实现原理**:

被验证的 Agent 在启动时读取环境变量来判断 Flag 状态：
```bash
# Flag=ON: AGENT_FLAG_enable_cot_v2=ON
# Flag=OFF: AGENT_FLAG_enable_cot_v2=OFF
```

Agent 代码侧（在系统 prompt 或工具描述中）:
```
如果环境变量 AGENT_FLAG_enable_cot_v2 == "ON"：
  使用 Chain-of-Thought v2 推理策略
否则：
  使用默认推理策略
```

Claude Code Skill 侧（在 setup 阶段）:
```python
# regression_runner.py 中
def run_with_flag(flag_name: str, flag_value: str):
    env = os.environ.copy()
    env[f"AGENT_FLAG_{flag_name}"] = flag_value
    result = subprocess.run(
        ["claude", "--print", f"--input", test_case.input],
        env=env,
        capture_output=True
    )
    return result
```

**为什么不依赖 Claude Code 原生 Flag 系统？**
- Claude Code 无原生 Feature Flag 功能
- 环境变量是 Claude Code Skill 完全可用的机制（Bash 工具可设置环境变量）
- 环境变量同时兼容本地开发和 CI 环境

**双重通道**:
- **环境变量**（运行时）：`AGENT_FLAG_<NAME>=ON|OFF` — 即时生效，A/B 对比使用
- **YAML 文件**（持久化）：`config.yaml` 中的 `feature_flags.flags` 列表 — 记录所有 Flag 定义及其默认值

**关键约束**:
- Flag 名称必须在 `config.yaml` 中预先定义
- 未定义的 Flag 变量不会生效（防御性设计，防止拼写错误导致的静默失败）
- Flag 变更记录在运行历史中（`runs.jsonl` 的 `flags` 字段），确保可追溯性

### 5.5 额外设计决策

| 决策项 | 选择 | 理由 |
|--------|------|------|
| Skill 触发方式 | 手动 `/` + LLM 自动 双触发 | 手动确保 100% 触发；自动降低使用门槛（description 中列出 10+ 触发短语） |
| 配置文件格式 | YAML | 可读性最高；与 Skill 生态一致（SKILL.md frontmatter 也是 YAML）；支持注释 |
| 脚本语言 | Python 3.10+ | 生态最丰富；Claude Code 用户普遍已安装；断言引擎天然适合 Python |
| 测试用例定义 | 声明式 YAML（非交互式问卷） | 让 AI 辅助生成测试用例时，输出 YAML 更自然 |
| 报告格式 | Markdown 为主，JSON 为辅 | Markdown 人类可读；JSON 供程序消费（CI 集成） |
| 隔离执行 | `context: fork` (可选) | 大型回归测试适合隔离执行，不膨胀主对话上下文 |
| CLI 依赖 | `claude --print --input "..."` | 利用 Claude Code 自带 CLI 执行 Agent，零额外依赖 |

---

## 6. 开发路线图

### 6.1 MVP（第 1-2 周）

**目标**: 让用户能定义 3 条断言 + 跑 3 条测试用例，从"凭感觉"变成"看通过率"

**交付物**:

| 组件 | 描述 | 工作量 |
|------|------|--------|
| SKILL.md | 命令路由 + 初始化 + 断言定义 + 回归运行 的工作流 | 1 天 |
| `parse_log.py` | 从 Agent 输出解析结构化 trace.jsonl | 0.5 天 |
| `assertion_engine.py` | 支持 3 种断言类型：`tool_call`、`tool_param`、`output_match` | 1 天 |
| `regression_runner.py` | 遍历测试用例、执行 Agent、运行断言、输出摘要 | 1 天 |
| `templates/suite-template.yaml` | 空测试套件模板 | 0.5 天 |
| `templates/config-template.yaml` | 默认配置文件模板 | 0.5 天 |
| `references/assertion-types.md` | 3 种断言类型的详细说明 | 0.5 天 |

**功能边界**:
- ✅ `/agent-verify:init` — 初始化目录结构
- ✅ `/agent-verify:assert --add` — 添加断言（3 种类型）
- ✅ `/agent-verify:suite --add` — 添加测试用例
- ✅ `/agent-verify:regression` — 运行回归（断言部分）
- ❌ LLM 裁判评分
- ❌ Feature Flag A/B 对比
- ❌ 基线管理

**成功标准**:
- 在 10 分钟内从零搭建验证套件（init → 3 条断言 → 1 条用例 → 跑通）
- 断言准确率 100%（确定性规则不应有误判）
- 至少 1 个真实 Agent（如 search-agent）能成功验证

### 6.2 V1.0（第 3-8 周）

**目标**: 完整的"双层裁判"体系 + Feature Flag A/B 对比，可公开发布

**新增组件**:

| 组件 | 描述 | 工作量 |
|------|------|--------|
| LLM 裁判集成 | 评分 prompt 模板 + haiku 主裁判 + 方差检测 | 2 天 |
| `baseline_manager.py` | 基线保存/加载/对比 | 1 天 |
| `ab_comparator.py` | Flag ON/OFF 双跑 + diff | 1 天 |
| `report_generator.py` | Markdown/JSON 报告生成 | 0.5 天 |
| Feature Flag 支持 | `config.yaml` Flag 定义 + 环境变量注入 | 1 天 |
| 扩展断言类型 | `path_sequence`、`timing`、`output_schema`（共 6 种） | 1 天 |
| `references/scoring-rubric.md` | 评分维度设计指南 | 0.5 天 |
| `references/integration-guide.md` | CI/CD 集成教程（GitHub Actions） | 1 天 |
| `examples/` | search-agent + chat-agent 完整示例 | 1 天 |

**功能边界**:
- ✅ 全部 MVP 功能
- ✅ `/agent-verify:baseline` — 基线管理
- ✅ `/agent-verify:compare` — A/B 对比
- ✅ `/agent-verify:report` — 报告生成
- ✅ LLM 裁判评分（haiku 主裁判 + 方差检测）
- ✅ Feature Flag 配置与双跑
- ✅ 6 种断言类型
- ✅ `examples/` 目录包含 2 个完整示例
- ❌ 生产输入收集器
- ❌ 覆盖率分析
- ❌ CI 自动集成（仅提供教程）

**成功标准**:
- A/B 对比报告正确识别变好/变坏的测试用例
- LLM 裁判评分方差 < 1.5（同输入多次打分一致）
- 用户可用 `examples/` 中的示例在 15 分钟内复现验证流程
- 文档覆盖全部命令的使用说明

### 6.3 V2.0（第 3-6 月）

**目标**: 高级自动化 + 生态扩展 + 智能特性

**新增组件**:

| 组件 | 描述 | 优先级 |
|------|------|--------|
| 测试用例 AI 生成器 | 从功能描述自动生成 Happy Path 测试用例初稿 | 高 |
| 覆盖率缺口分析 | 分析哪些工具/路径/输入类型未被测试覆盖 | 高 |
| 智能回归选择 | 基于 git diff 分析选择相关测试用例子集运行 | 中 |
| 真实输入收集器 | 从生产日志收集真实用户输入，清洗后加入测试套件 | 中 |
| CI 深度集成 | GitHub Actions workflow 模板 + PR 状态检查 | 中 |
| 测试用例推荐 | "你最近加了 search 工具，要不要加一条相关断言？" | 低 |
| 多 Agent 协作验证 | 支持验证 multi-agent 系统的 Agent 间交互 | 低 |
| 历史趋势 Dashboard | 评分变化趋势图（使用 Claude Code 内建 markdown 渲染） | 低 |

**V2.0 不做但在雷达上**:
- Codex 闭环自我修复（研究阶段，风险极高）
- SaaS 化（与 Skill 定位矛盾）
- 多模态 Agent 评估（需 Claude 多模态能力升级）
- 生产监控（那是 LangSmith/Galileo 的领域）

---

## 附录

### A. Skill 规范合规清单

| 规范项 | 要求 | 本 Skill 状态 |
|--------|------|-------------|
| 目录名 | kebab-case, ≤64字符 | ✅ `agent-verify` (13 字符) |
| 文件名 | 必须为 `SKILL.md` | ✅ |
| name frontmatter | kebab-case, 匹配目录名 | ✅ `agent-verify` |
| description | ≤1024 字符, 无 `<>` | ✅ ~800 字符 |
| SKILL.md 行数 | < 500 行 | ✅ 目标 ~400 行 |
| 写作风格 | 祈使句/不定式 | ✅ |
| 无 README | 不创建文档文件 | ✅ 仅 SKILL.md + scripts/ + references/ + templates/ + examples/ |
| allowed-tools | 声明所需工具权限 | ✅ Bash/Read/Write/Edit |
| scripts/ | 通过 Bash 执行，不读入上下文 | ✅ Python 脚本 |
| references/ | 从 SKILL.md 命令式引用 | ✅ |
| 无竞品 | 不包含 "claude" 或 "anthropic" | ✅ `agent-verify` |

### B. 依赖清单

| 依赖 | 类型 | 用途 | 必需？ |
|------|------|------|--------|
| Python 3.10+ | 运行时 | 断言引擎、解析器、执行器 | ✅ |
| PyYAML | Python 包 | YAML 配置文件解析 | ✅ |
| Claude Code CLI | 运行时 | 执行被验证的 Agent (`claude --print`) | ✅ |
| Claude API | API | LLM 裁判评分 (V1.0+) | ❌ (MVP 不需要) |
| jq (可选) | 命令行 | JSONL 快速查询 | ❌ |

### C. 参考来源

本架构设计基于以下研究输入：

1. `skill-system-research.md` — Claude Code Skill 系统约束与设计模式
2. `engineering-components.md` — 视频方法论的 16 个可工程化组件及其优先级
3. `tool-ecosystem.md` — 75+ Agent 评估工具的竞争格局与差距分析

---

*架构设计完成时间：2026-06-30*
*设计者：Architect (技术架构师)*
*下一阶段：技术设计文档 (由 Senior Engineer 角色输出)*
