---
name: agent-verify
description: >-
  AI Agent verification — assertion-based testing, regression testing,
  LLM-as-Judge, A/B comparison. Trigger: verify agent, regression test,
  check agent output, suggest assertions, design assertions, 验证Agent,
  回归测试, 断言, agent-verify, setup, suggest, 设计断言, 建议规则,
  添加断言, 检查Agent.
  Use when user wants to verify an AI Agent's behaviour, design assertions
  for agent quality, run regression checks, or compare agent versions.
license: MIT
compatibility: macOS, Linux
allowed-tools: [Bash, Read, Write, Edit]
---

# agent-verify

为 AI Agent 建立质量验证体系。AI 帮你设计断言，你确认即可。

## 核心工作流（对话式）

### 1. 初始化 — AI 分析你的 Agent 并建议断言

```
/agent-verify setup
```

AI 会：
1. 运行 `init_verify.py` 创建 `agent-verify/` 目录
2. 阅读你的项目（SKILL.md / CLAUDE.md / 代码），分析 Agent 的职责
3. **自动设计 3-5 条断言**，逐条展示并请求确认
4. 你确认/修改/补充后，写入 `assertions.yaml`

### 2. AI 帮你设计断言

```
/agent-verify suggest
```

AI 分析你的 Agent 应该做什么，逐条展示建议的断言：

> 根据你的 Agent 功能，我建议以下断言:
>
> 1. [tool_call] 必须调用 TaskCreate 工具 — 理由: 核心约束要求创建子任务
>    确认? [Y/n/修改]
> 2. [tool_param] query 参数不能为空 — 理由: 空查询会导致搜索失败
>    确认? [Y/n/修改]
> 3. [output_match] 输出必须包含引用来源 — 理由: 承诺"引用可靠来源"
>    确认? [Y/n/修改]

每条都可以：
- `Y` → 接受
- `n` → 跳过
- `改为xxx` → 用自然语言修改
- `加一条xxx` → 追加新规则

### 3. 手动添加规则

```
/agent-verify add "Agent 调用 Read 工具后必须返回文件内容摘要"
/agent-verify add "输出中不能包含'抱歉'或'无法'等推诿词"
```

### 4. 验证

```
/agent-verify check "场景描述"
```

AI 构造 trace → 运行断言引擎 → 展示结果：

```
✅ 必须调用 TaskCreate     — 检测到 3 次调用
✅ 无依赖任务并行调度       — 检测到 2 次并行 Agent
❌ 进度摘要格式            — 缺少 [orch-<id>] 前缀
──
5/6 通过
```

## 断言类型速查

| 类型 | 检查什么 | 示例 |
|------|---------|------|
| `tool_call` | 工具是否被调用 | 必须调用 TaskCreate ≥1次 |
| `tool_param` | 工具参数是否正确 | query 参数不能为空 |
| `output_match` | 输出内容匹配 | 输出包含"答案"或"根据" |
| `path_sequence` | 执行步骤顺序 (V1.0) | 先planning→再execution |
| `timing` | 执行耗时 (V1.0) | 总耗时 < 60秒 |
| `output_schema` | 输出JSON结构 (V1.0) | 必须含 answer 字段 |

## 直接使用脚本

```bash
agent-verify setup          # 初始化 + AI建议断言
agent-verify suggest        # AI分析项目 → 设计断言
agent-verify add "规则"     # 自然语言加断言
agent-verify test "场景"    # 自然语言描述场景 → 检查
agent-verify list           # 列出断言
agent-verify demo           # 一分钟演示
```

## 参考文档

- 断言类型详解: [references/assertions-guide.md](references/assertions-guide.md)
- 配置完整参考: [references/config-reference.md](references/config-reference.md)
- 工作流指南: [references/workflows.md](references/workflows.md)

## 实战示例: 验证一个搜索 Agent

假设你有一个 `search-agent` Skill，它调用 `web_search` 工具并返回答案。

**1. 初始化**
```
/agent-verify setup
```
AI 分析 search-agent 后建议 3 条断言，你全部接受。

**2. 日常开发**
```
修改了搜索 prompt → /agent-verify check "用户问天气，Agent搜索后返回22°C"
```
结果: 2/3 通过 — output_match 失败，因为输出格式变了。
→ 更新 assertions.yaml 放宽 pattern → 重新 check → 3/3 ✅

**3. 质量门禁**
```
/agent-verify check "用户问天气"
/agent-verify check "用户问股价"
/agent-verify check "用户问新闻"   # 三个场景全部通过 → 提交
```

## 已知限制

- trace 获取: Agent 需输出 `[AGENT_VERIFY:TRACE]` 格式的结构化日志
- LLM Judge (V1.0): 当前版本需手动配置 Anthropic API key
- 自然语言解析: 复杂断言建议直接编辑 assertions.yaml
