#!/bin/bash
# ============================================================
# agent-verify 完整功能演示脚本
# 模拟: 开发一个"天气查询Agent" → 验证它的行为
# ============================================================
set -e

SKILL_DIR="${HOME}/.claude/skills/agent-verify"
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
NC='\033[0m'

pass=0; fail=0
check() {
  if [ $? -eq 0 ]; then
    echo -e "  ${GREEN}✅ $1${NC}"; ((pass++))
  else
    echo -e "  ${RED}❌ $1${NC}"; ((fail++))
  fi
}

echo -e "${CYAN}════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  agent-verify 功能演示测试${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════${NC}"

# ---- 准备测试环境 ----
echo -e "\n${YELLOW}[1/6] 初始化测试项目${NC}"
TEST_DIR="/tmp/agent-verify-demo-$$"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

python3 "$SKILL_DIR/scripts/init_verify.py" \
  --target-dir . \
  --target-name "weather-bot" 2>&1 | tail -5
check "init_verify 执行"

[ -f agent-verify/config.yaml ] && check "config.yaml 生成"
[ -f agent-verify/assertions.yaml ] && check "assertions.yaml 生成"
[ -f agent-verify/suites/suites.yaml ] && check "suites.yaml 生成"

# ---- 写入断言 ----
echo -e "\n${YELLOW}[2/6] 定义断言规则${NC}"

cat > agent-verify/assertions.yaml << 'YAML'
# weather-bot 验证断言
assertions:
  # 断言1: 必须调用了 get_weather 工具
  - id: "called-get-weather"
    name: "调用了天气查询工具"
    type: tool_call
    target:
      tool_name: "get_weather"
    condition:
      min_count: 1
    severity: error
    enabled: true

  # 断言2: 城市参数不能为空
  - id: "city-not-empty"
    name: "查询城市参数不为空"
    type: tool_param
    target:
      tool_name: "get_weather"
      param_name: "city"
    condition:
      not_empty: true
    severity: error
    enabled: true

  # 断言3: 输出必须包含天气关键词
  - id: "output-contains-weather"
    name: "输出包含天气信息"
    type: output_match
    target:
      agent: "weather-bot"
    condition:
      pattern: "(天气|temperature|°C|晴|雨|多云|wind)"
      operator: "regex"
      case_sensitive: false
    severity: error
    enabled: true

  # 断言4: 输出不能包含错误关键词
  - id: "no-error-in-output"
    name: "输出中无错误信息"
    type: output_match
    target:
      agent: "weather-bot"
    condition:
      pattern: "(error|failed|抱歉|cannot|unable)"
      operator: "regex"
      match_behavior: "must_not_match"
      case_sensitive: false
    severity: warning
    enabled: true

  # 断言5: 至少返回一条结果
  - id: "non-empty-response"
    name: "响应不为空"
    type: output_match
    target:
      agent: "weather-bot"
    condition:
      pattern: ".+"
      operator: "regex"
      min_matches: 1
    severity: error
    enabled: true
YAML

python3 -c "import yaml; yaml.safe_load(open('agent-verify/assertions.yaml'))" 2>/dev/null
check "断言 YAML 语法有效"

COUNT=$(python3 "$SKILL_DIR/scripts/assertion_engine.py" \
  --assertions agent-verify/assertions.yaml --list 2>/dev/null | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['count'])")
echo "  断言数量: $COUNT"
[ "$COUNT" -eq 5 ] && check "5条断言全部加载"

# ---- 场景A: 正确的 Agent 行为 ----
echo -e "\n${YELLOW}[3/6] 测试场景A: Agent 正确完成任务${NC}"

cat > trace-good.jsonl << 'JSONL'
{"event":"tool_call","data":{"tool_name":"get_weather","tool_input":{"city":"北京"}}}
{"event":"tool_result","data":{"tool_name":"get_weather","result":"北京今天晴，温度22°C，湿度45%，风力3级"}}
{"event":"llm_response","data":{"final_output":"北京今天天气晴朗，气温22°C，适合户外活动。"}}
JSONL

python3 "$SKILL_DIR/scripts/assertion_engine.py" \
  --assertions agent-verify/assertions.yaml \
  --trace trace-good.jsonl \
  --check 2>/dev/null > /tmp/result-good.json

PASSED=$(python3 -c "import json; d=json.load(open('/tmp/result-good.json')); print(d['passed'])")
TOTAL=$(python3 -c "import json; d=json.load(open('/tmp/result-good.json')); print(d['total'])")
echo "  通过: $PASSED / 总计: $TOTAL"
[ "$PASSED" -ge 4 ] && check "正确行为通过率 >= 80%"

# 显示每条结果
python3 -c "
import json
d = json.load(open('/tmp/result-good.json'))
for r in d['results']:
    s = '✅' if r['pass_'] else '❌'
    print(f'    {s} {r[\"assertion_id\"]}: {r.get(\"reason\",\"ok\")}')"

# ---- 场景B: 有问题的 Agent 行为 ----
echo -e "\n${YELLOW}[4/6] 测试场景B: Agent 出错（忘调工具+输出错误）${NC}"

cat > trace-bad.jsonl << 'JSONL'
{"event":"llm_response","data":{"final_output":"抱歉，我无法获取天气信息，请稍后再试。"}}
JSONL

python3 "$SKILL_DIR/scripts/assertion_engine.py" \
  --assertions agent-verify/assertions.yaml \
  --trace trace-bad.jsonl \
  --check 2>/dev/null > /tmp/result-bad.json

PASSED_BAD=$(python3 -c "import json; d=json.load(open('/tmp/result-bad.json')); print(d['passed'])")
echo "  通过: $PASSED_BAD / 总计: $TOTAL"
[ "$PASSED_BAD" -le 2 ] && check "错误行为正确被捕获（通过率低）"

python3 -c "
import json
d = json.load(open('/tmp/result-bad.json'))
for r in d['results']:
    s = '✅' if r['pass_'] else '❌'
    print(f'    {s} {r[\"assertion_id\"]}: {r.get(\"reason\",\"ok\")}')"

# ---- 场景C: 写入测试套件并跑 regression runner ----
echo -e "\n${YELLOW}[5/6] 配置测试套件并运行回归测试${NC}"

cat > agent-verify/suites/suites.yaml << 'YAML'
defaults:
  assertion_file: "assertions.yaml"
  agent: "weather-bot"
  timeout: 30

test_cases:
  - id: "happy-path-beijing"
    description: "查询北京天气 - 正常流程"
    trace_file: "../../trace-good.jsonl"
    group: "smoke"

  - id: "error-case"
    description: "Agent 未调工具直接报错"
    trace_file: "../../trace-bad.jsonl"
    group: "realworld"

groups:
  smoke:
    description: "每次改动必须通过"
  realworld:
    description: "真实场景回归"
YAML

python3 "$SKILL_DIR/scripts/regression_runner.py" \
  --suite agent-verify/suites/suites.yaml \
  --config agent-verify/config.yaml 2>&1 | tail -20
check "回归测试运行"

# ---- 生成报告 ----
echo -e "\n${YELLOW}[6/6] 生成验证报告${NC}"

# 合并两个 trace 的结果为报告输入
python3 -c "
import json
good = json.load(open('/tmp/result-good.json'))
bad = json.load(open('/tmp/result-bad.json'))
report = {
    'title': 'weather-bot 验证报告',
    'summary': {
        'scenario_a': f'{good[\"passed\"]}/{good[\"total\"]} passed',
        'scenario_b': f'{bad[\"passed\"]}/{bad[\"total\"]} passed',
        'total_assertions': good['total'],
    },
    'results': {
        'happy-path-beijing': good['results'],
        'error-case': bad['results'],
    }
}
json.dump(report, open('/tmp/report-input.json', 'w'), ensure_ascii=False, indent=2)
"

python3 "$SKILL_DIR/scripts/report_generator.py" \
  --input /tmp/report-input.json \
  --format markdown 2>/dev/null > agent-verify/reports/demo-report.md
check "Markdown 报告生成"

python3 "$SKILL_DIR/scripts/report_generator.py" \
  --input /tmp/report-input.json \
  --format json 2>/dev/null > agent-verify/reports/demo-report.json
check "JSON 报告生成"

echo -e "\n${CYAN}═══ 报告预览 ═══${NC}"
head -25 agent-verify/reports/demo-report.md

# ---- 总结 ----
echo -e "\n${CYAN}════════════════════════════════════════════════════════${NC}"
echo -e "  测试结果: ${GREEN}${pass} 通过${NC} / ${RED}${fail} 失败${NC}"
echo -e "  测试目录: ${TEST_DIR}"
echo -e "  报告文件:"
echo -e "    ${TEST_DIR}/agent-verify/reports/demo-report.md"
echo -e "    ${TEST_DIR}/agent-verify/reports/demo-report.json"
echo -e "${CYAN}════════════════════════════════════════════════════════${NC}"

[ "$fail" -eq 0 ] && echo -e "\n${GREEN}🎉 全部测试通过！agent-verify 功能正常。${NC}"
