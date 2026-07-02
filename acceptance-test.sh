#!/bin/bash
# ================================================================
# agent-verify 完整验收测试
# 从零开始: init → assert → regression → baseline → report
# ================================================================
set -o pipefail
SKILL="${HOME}/.claude/skills/agent-verify"
TEST_DIR="/tmp/agent-verify-acceptance-$$"
PASS=0; FAIL=0

check() { if [ $1 -eq 0 ]; then echo "  ✅ $2"; PASS=$((PASS+1)); else echo "  ❌ $2"; FAIL=$((FAIL+1)); fi; }
cleanup() { rm -rf "$TEST_DIR"; }
trap cleanup EXIT

echo "════════════════════════════════════════════════════════"
echo "  agent-verify 完整验收测试"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "════════════════════════════════════════════════════════"

# ═══════════════════════════════════════════════
# Phase 1: Init
# ═══════════════════════════════════════════════
echo ""; echo "━━━ Phase 1/6: init ━━━"
mkdir -p "$TEST_DIR" && cd "$TEST_DIR"

python3 "$SKILL/scripts/init_verify.py" --target-dir . --target-name "acceptance-test" 2>&1 | grep "✅"
check $? "1.1 init 执行"

[ -f agent-verify/config.yaml ] && [ -f agent-verify/assertions.yaml ] && [ -d agent-verify/suites ]
check $? "1.2 目录结构 (config + assertions + suites)"

python3 -c "
import yaml
d = yaml.safe_load(open('agent-verify/assertions.yaml'))
assert 'assertions' in d, 'missing root key'
print(f'  模板断言: {len(d[\"assertions\"])} 条')
"
check $? "1.3 assertions.yaml 格式正确 (含 root key)"

# ═══════════════════════════════════════════════
# Phase 2: Assert — 写入自定义断言
# ═══════════════════════════════════════════════
echo ""; echo "━━━ Phase 2/6: assert ━━━"

python3 << 'PYEOF'
import yaml
assertions = {"assertions": [
    {"id":"must-call-search","name":"必须调用 web_search","type":"tool_call",
     "target":{"tool_name":"web_search"},"condition":{"min_count":1},
     "severity":"error","enabled":True},
    {"id":"query-not-empty","name":"搜索参数不为空","type":"tool_param",
     "target":{"tool_name":"web_search","param":"query"},
     "condition":{"not_null":True,"not_whitespace_only":True,"min_length":2},
     "severity":"error","enabled":True},
    {"id":"output-has-answer","name":"输出包含答案标记","type":"output_match",
     "target":{"agent":"test"},"condition":{"pattern":"答案[：:]","operator":"regex","case_sensitive":False},
     "severity":"error","enabled":True},
    {"id":"response-meaningful","name":"响应长度合理","type":"output_match",
     "target":{"agent":"test"},"condition":{"pattern":".{10,}","operator":"regex","min_matches":1},
     "severity":"warning","enabled":True},
]}
with open("agent-verify/assertions.yaml","w") as f:
    yaml.dump(assertions, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
print("  ✅ 4条自定义断言已写入")
PYEOF
check $? "2.1 断言写入"

python3 "$SKILL/scripts/assertion_engine.py" \
  --assertions agent-verify/assertions.yaml --list 2>/dev/null | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f'  {d[\"count\"]} 条加载'); assert d['count']==4"
check $? "2.2 断言引擎加载 4/4"

# ═══════════════════════════════════════════════
# Phase 3: Regression — 双场景 trace 检查
# ═══════════════════════════════════════════════
echo ""; echo "━━━ Phase 3/6: regression ━━━"

# 场景A: 正确Agent — 调了 web_search, 返回正确答案
cat > /tmp/trace-A.jsonl << 'JSONL'
{"type":"tool_call","tool_name":"web_search","input":{"query":"北京天气"},"seq":1}
{"type":"tool_result","tool_name":"web_search","output":{"result":"北京晴 22°C"},"seq":2}
{"type":"run_end","final_output":"答案：北京今天天气晴朗，气温22°C。","seq":3}
JSONL

python3 "$SKILL/scripts/assertion_engine.py" \
  --assertions agent-verify/assertions.yaml \
  --trace /tmp/trace-A.jsonl --check 2>/dev/null > /tmp/result-A.json
check $? "3.1 场景A 断言检查执行"

A_OK=$(python3 -c 'import json; print(json.load(open("/tmp/result-A.json"))["passed"])' | tr -d '[:space:]')
echo "  场景A: $A_OK/4 通过"
python3 -c "
import json; d=json.load(open('/tmp/result-A.json'))
for r in d['results']:
    print(f'    {\"✅\" if r[\"pass_\"] else \"❌\"} {r[\"assertion_id\"]}')"
[ "$A_OK" = "4" ]; check $? "3.2 场景A 全部通过"

# 场景B: 错误Agent — 没调工具, 直接报错
cat > /tmp/trace-B.jsonl << 'JSONL'
{"type":"run_end","final_output":"抱歉，服务不可用。","seq":1}
JSONL

python3 "$SKILL/scripts/assertion_engine.py" \
  --assertions agent-verify/assertions.yaml \
  --trace /tmp/trace-B.jsonl --check 2>/dev/null > /tmp/result-B.json
check $? "3.3 场景B 断言检查执行"

B_OK=$(python3 -c 'import json; print(json.load(open("/tmp/result-B.json"))["passed"])' | tr -d '[:space:]')
echo "  场景B: $B_OK/4 通过 (越低越好=错误被拦截)"
python3 -c "
import json; d=json.load(open('/tmp/result-B.json'))
for r in d['results']:
    print(f'    {\"🔴\" if not r[\"pass_\"] else \"⚠️\"} {r[\"assertion_id\"]}')"
[ "$B_OK" = "0" ]; check $? "3.4 场景B 错误被正确拦截"

# ═══════════════════════════════════════════════
# Phase 4: Baseline
# ═══════════════════════════════════════════════
echo ""; echo "━━━ Phase 4/6: baseline ━━━"

python3 << 'PYEOF'
import json, os, yaml
from datetime import datetime
os.makedirs("agent-verify/baselines", exist_ok=True)

with open("agent-verify/assertions.yaml") as f:
    assertions = yaml.safe_load(f)

baseline = {
    "id": "v1.0-acceptance",
    "timestamp": datetime.now().isoformat(),
    "description": "验收测试基线",
    "summary": {"total": 4},
    "assertions_snapshot": assertions["assertions"],
}
with open("agent-verify/baselines/v1.0-acceptance.json", "w") as f:
    json.dump(baseline, f, ensure_ascii=False, indent=2)
print("  ✅ 基线 v1.0-acceptance 已保存")
PYEOF
check $? "4.1 baseline 保存"

[ -f agent-verify/baselines/v1.0-acceptance.json ]
check $? "4.2 baseline 文件存在"

# ═══════════════════════════════════════════════
# Phase 5: Report
# ═══════════════════════════════════════════════
echo ""; echo "━━━ Phase 5/6: report ━━━"

python3 << 'PYEOF'
import json
A = json.load(open('/tmp/result-A.json'))
B = json.load(open('/tmp/result-B.json'))
report = {
    "title": "agent-verify 验收测试报告",
    "summary": {
        "场景A(正确Agent)": f'{A["passed"]}/{A["total"]} 通过',
        "场景B(错误Agent)": f'{B["passed"]}/{B["total"]} 通过',
    },
    "results": {"happy-path": A["results"], "error-case": B["results"]},
}
json.dump(report, open('/tmp/report-in.json','w'), ensure_ascii=False, indent=2)
print("  ✅ 报告数据已聚合")
PYEOF

mkdir -p agent-verify/reports
python3 "$SKILL/scripts/report_generator.py" \
  --input /tmp/report-in.json --format markdown 2>/dev/null \
  > agent-verify/reports/acceptance-report.md
check $? "5.1 Markdown 报告生成"

python3 "$SKILL/scripts/report_generator.py" \
  --input /tmp/report-in.json --format json 2>/dev/null \
  > agent-verify/reports/acceptance-report.json
check $? "5.2 JSON 报告生成"

echo "  ┌─ 报告预览 ──────────────────┐"
head -6 agent-verify/reports/acceptance-report.md | while read line; do
  printf "  │ %-30s │\n" "${line:0:28}"
done
echo "  └──────────────────────────────┘"

# ═══════════════════════════════════════════════
# Phase 6: V1.0 接口验证
# ═══════════════════════════════════════════════
echo ""; echo "━━━ Phase 6/6: V1.0 组件接口 ━━━"

python3 "$SKILL/scripts/llm_judge.py" --help > /dev/null 2>&1
check $? "6.1 llm_judge CLI"

python3 "$SKILL/scripts/feature_flag.py" --help > /dev/null 2>&1
check $? "6.2 feature_flag CLI"

# ═══════════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════════
TOTAL=$((PASS + FAIL))
echo ""
echo "════════════════════════════════════════════════════════"
printf "  验收结果: %2d/%2d 通过" "$PASS" "$TOTAL"
if [ "$FAIL" -eq 0 ]; then
  echo "  🎉 全部通过！"
else
  echo "  ⚠️  $FAIL 项失败"
fi
echo ""
echo "  测试目录: $TEST_DIR (退出后自动清理)"
echo "  报告文件: agent-verify/reports/acceptance-report.md"
echo "════════════════════════════════════════════════════════"
echo ""
echo "  验证链路:"
echo "    init → assert(4条) → regression(2场景)"
echo "    → baseline(保存) → report(MD+JSON) → V1.0接口"
echo ""
echo "  场景A(正确Agent): $A_OK/4 ✅"
echo "  场景B(错误Agent): $B_OK/4 🔴"

exit $FAIL
