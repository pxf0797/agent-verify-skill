# agent-verify 工作流指南

## 工作流1: 首次使用 (4分钟)

1. `/agent-verify setup` — AI 初始化项目 + 分析 Agent + 建议断言
2. 逐条确认 AI 建议的断言 (Y/n/修改)
3. `/agent-verify add "补充规则"` — 追加自己的断言
4. `/agent-verify check "场景描述"` — 验证

## 工作流2: 日常开发循环

修改 Agent → `/agent-verify check "新场景"` → 看结果(✅/❌) → 调整 → 重复

## 工作流3: 质量改进

1. `/agent-verify list` — 查看现有断言
2. 编辑 assertions.yaml 调整规则
3. `/agent-verify check "回归场景"` — 验证
4. `git commit agent-verify/` — 保存基线

## 脚本调用

```bash
agent-verify setup          # 初始化 + AI 建议断言
agent-verify add "规则"     # 自然语言加断言
agent-verify check "场景"   # 描述行为 → 自动验证
agent-verify list           # 列出断言
agent-verify demo           # 演示
```
