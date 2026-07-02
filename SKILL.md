---
name: agent-verify
description: >-
  AI Agent verification, assertion-based testing, regression testing,
  LLM-as-Judge, A/B comparison for prompts, agent quality baseline.
  Trigger: verify agent output, run regression on agent, compare agent
  versions, save quality baseline, manage test suites, generate verification
  reports, agent assertions, 验证 Agent, 回归测试, 断言检查, Agent 质量基线,
  A/B 对比, 初始化验证项目, init, agent-verify, setup verify project,
  bootstrap agent testing, 初始化验证.
  Use when you need to assert tool calls / output correctness of a Claude
  Agent, run a test suite against an agent, compare two agent versions with
  feature flags, save or compare quality baselines, generate structured
  verification reports, or initialize a new verification project.
license: MIT
compatibility: macOS, Linux
allowed-tools: [Bash, Read, Write, Edit]
---

# agent-verify: AI Agent Verification Toolkit

Verify AI Agent behaviour deterministically: assert tool-call patterns, capture
output correctness, run regression suites, score quality with LLM judging, and
compare A/B variants — all from the CLI.

## Quick Start

Three steps from zero to a passing regression:

**1. Initialize**
```
/agent-verify:init --target my-search-agent
```
Creates `agent-verify/` with `config.yaml`, `assertions.yaml`, and `suites/`.

**2. Add an assertion**
```
/agent-verify:assert --add --type tool_call --tool-name search --condition exactly:1
```
Walks through type, target, and condition; appends to `assertions.yaml`.

**3. Run the regression**
```
/agent-verify:regression --suite suites/default.yaml
```
Executes every case, checks every enabled assertion, prints a summary table.

→ Full onboarding & daily-development loop: [workflows.md](references/workflows.md)

## Commands

Seven sub-commands cover verify→improve→guard. Commands marked **(V1.0)** require
scripts shipping in the next release; all others work in MVP.

### /agent-verify:init

**Triggers:** `init agent-verify`, `setup verify project`, `初始化验证项目`, `bootstrap agent testing`.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--target <name>` | No | dir name | Agent/Skill name for template variable substitution |
| `--template <type>` | No | `default` | `default` (all 3 templates) or `minimal` (config + assertions only) |

**Workflow**

```bash
python scripts/init_verify.py --target-dir "$(pwd)" \
    --target-name "my-agent" --template default
```

Parse the returned JSON. On `"success"`, display `created_files` and
`next_steps`. On `"error"`, surface `message` to the user.

**Example output**

```
✅ agent-verify/ initialized for "my-agent"
Created:
  agent-verify/config.yaml
  agent-verify/assertions.yaml
  agent-verify/suites/default.yaml
Next:
  1. Edit assertions.yaml to match your agent's expected behaviour
  2. Run /agent-verify:assert --list to review
  3. Run /agent-verify:regression --suite suites/default.yaml
```

### /agent-verify:assert

**Triggers:** `add assertion`, `create assert`, `check tool call`, `verify output matches`,
`添加断言`, `断言管理`, `验证工具调用`, `检查输出匹配`.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--add` | — | Interactive assertion-creation flow |
| `--type <name>` | No | Pre-select assertion type (skip the type prompt) |
| `--list` | — | Print all assertions with enabled/disabled status |
| `--remove <id>` | No | Remove the assertion with the given ID |
| `--run <id>` | No | Execute a single assertion against the most recent trace |

**Interactive flow (`--add`)**

1. Ask assertion type (show numbered menu) if `--type` not supplied.
2. Ask for `target` details (tool name, param path, regex) per type.
3. Ask for `condition` (e.g. `exactly:1`, `pattern:"\\d{4}"`).
4. Load `assertions.yaml`, generate unique `id`, append entry, write back.
5. **MVP guard**: only `tool_call`, `tool_param`, `output_match` are active;
   other types save but warn they require V1.0.
6. Optionally run immediately: `--run <new-id>`.

**List assertions**
```bash
python scripts/assertion_engine.py --list \
    --assertions agent-verify/assertions.yaml
```
Prints: `ID | Name | Type | Enabled | Target`.

→ Full field reference & edge cases: [assertions-guide.md](references/assertions-guide.md)

### /agent-verify:regression  **(MVP core)**

**Triggers:** `run regression`, `regression test`, `verify agent`, `check for regressions`,
`运行回归`, `回归验证`, `全量测试`, `冒烟测试`.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--suite <file>` | Yes | — | Suite YAML path (e.g. `suites/default.yaml`) |
| `--scope <name>` | No | `all` | `all`, `smoke`, `changed`, group name, or single case ID |
| `--compare` | No | `false` | Diff against latest baseline after run |
| `--output <fmt>` | No | `markdown` | `markdown` or `json` |
| `--judge` | No | `false` | Enable LLM judging **(V1.0)** |
| `--no-judge` | No | — | Force-disable LLM judging |

**Workflow**
```bash
python scripts/regression_runner.py \
    --suite agent-verify/suites/default.yaml \
    --config agent-verify/config.yaml \
    --scope all --output json
```
Show progress (`[2/5] search-basic … PASS`), then render the summary table.
If `--compare`, also diff against the latest baseline.

**Scope shortcuts:** `all` (every case), `smoke` (tagged in groups), `changed`
(git-diff related), `<group>` (custom group), `<case-id>` (single case).

**Example output**

```
Suite: default  Cases: 5  Passed: 4  Failed: 1  Pass rate: 80.0%

Case              Result  Assertions  Duration
search-basic      PASS    3/3         2.1s
search-no-results PASS    2/2         1.8s
search-ambiguous  FAIL    1/2         3.4s
  └ tool_call: expected "search" ≥1 time(s), got 0
search-pagination PASS    2/2         2.6s
search-error      PASS    3/3         1.2s

Baseline vs previous: pass-rate 80.0% → 85.0% (+5.0%)
⚠ 1 regression: search-ambiguous
```

→ Config thresholds, stop-on-first-error, etc.: [config-reference.md](references/config-reference.md)

### /agent-verify:compare  **(V1.0)**

**Triggers:** `compare flag`, `A/B test agent`, `对比 Flag`, `A/B 对比`,
`compare prompt variant`, `feature flag comparison`.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--flag <name>` | Yes | — | Flag name (must be pre-defined in `config.yaml`) |
| `--baseline <name>` | No | — | Use saved baseline as OFF side instead of re-running |
| `--suite <file>` | No | `suites/default.yaml` | Suite for both sides |
| `--judge` | No | `false` | Enable LLM judging on both runs |

**Workflow**
```bash
python scripts/feature_flag.py \
    --flag "new-prompt" \
    --suite agent-verify/suites/default.yaml \
    --config agent-verify/config.yaml --output json
```
Validates flag → runs OFF side → runs ON side (`AGENT_FLAG_<NAME>=ON`) →
renders diff table with assertion flips, score deltas, and conclusion.

**Example output**

```
Comparison: new-prompt = ON vs OFF  (Cases: 5)

Dimension        OFF     ON      Change   Direction
pass_rate        80.0%   90.0%   +10.0%   better ↑
avg_duration_ms  2140    2080    -60ms    neutral

Assertion changes: search-ambiguous/tool-call-SEARCH: FAIL → PASS
Conclusion: ON is better. +10% pass-rate, no regressions.
```

> ⚠ Requires `scripts/feature_flag.py` (V1.0). MVP: manually toggle flags and
> re-run `/agent-verify:regression`.

### /agent-verify:baseline

**Triggers:** `save baseline`, `list baselines`, `compare baselines`, `baseline diff`,
`保存基线`, `基线列表`, `基线对比`, `quality snapshot`.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--save <name>` | Yes | Save last regression result as named baseline |
| `--list` | — | List all baselines with metadata |
| `--compare <a> <b>` | — | Compare two baselines **(V1.0)** |
| `--suite <file>` | No | Suite path (used with `--save`) |

**Save**
```bash
python scripts/regression_runner.py \
    --baseline-save "v0.9-rc1" \
    --suite agent-verify/suites/default.yaml \
    --config agent-verify/config.yaml
```
Saves `baselines/v0.9-rc1.json` with full results, config hash, optional git SHA.

**List**
```bash
python scripts/regression_runner.py \
    --baseline-list --baselines-dir agent-verify/baselines
```
Prints: `Name | Created | Suite | Pass rate | Cases | Git commit`.

**Compare (V1.0)**
```bash
python scripts/regression_runner.py \
    --baseline-compare "v0.8" "v0.9-rc1" \
    --baselines-dir agent-verify/baselines
```
> ⚠ `--compare` needs full baseline-comparison path (V1.0). MVP: diff the JSON files directly.

### /agent-verify:suite

**Triggers:** `manage test suite`, `add test case`, `generate test cases`, `export suite`,
`管理测试套件`, `添加用例`, `生成测试用例`, `导出套件`.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--add` | — | Interactive flow to add a test case |
| `--list <file>` | No | Print all cases in the given suite |
| `--import <file>` | No | Import cases from JSON/CSV |
| `--export <file>` | No | Export suite to JSON |
| `--generate` | — | AI-assisted test-case generation |

**Interactive add** — prompts for `case_id`, `description`, `input_text`,
`expected_tool_sequence`, and group tags; appends to the suite YAML.

**AI generation (`--generate`)** — describe the agent's purpose and tools; generates
3–8 cases (happy-path, edge, error); review & approve before writing.

→ Suite YAML field reference: [config-reference.md](references/config-reference.md)

### /agent-verify:report

**Triggers:** `generate report`, `verification report`, `export results`, `生成报告`,
`导出验证报告`, `测试报告`.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--format <type>` | No | `markdown` | `markdown`, `json`, or `html` |
| `--scope <name>` | No | `latest` | `latest`, a baseline name, or a result JSON path |
| `--output <path>` | No | `reports/report.md` | Write destination |

**Workflow**
```bash
python scripts/report_generator.py \
    --input agent-verify/reports/latest-result.json \
    --format markdown --output agent-verify/reports/report.md
```
HTML reports are self-contained (inline CSS). Baseline-scoped reports load the
snapshot first, then pass its path.

→ Report format examples: [workflows.md](references/workflows.md)

## Configuration

Minimal `config.yaml`:

```yaml
version: 1
execution:
  timeout_seconds: 120
  max_steps: 50
  stop_on_first_error: false
assertions:
  fail_fast_threshold: 0       # 0 = run all; >0 = stop after N failures
llm_judge:                     # (V1.0)
  enabled: false
  dimensions: [accuracy, completeness, reasonableness]
  max_monthly_budget_usd: 50
feature_flags:                 # (V1.0)
  flags: []
```

**Resolution order** (highest priority first):
CLI flags → suite `defaults` → case-level overrides → global `config.yaml`.

→ Every field, type, default, and cross-field dependency:
[config-reference.md](references/config-reference.md)

## Assertion Types Overview

MVP implements the first three types; remainder ship in V1.0.

| Type | MVP | What it checks | Example condition |
|------|-----|----------------|-------------------|
| `tool_call` | ✅ | Tool was called (count) | `exactly: 1` |
| `tool_param` | ✅ | Parameter meets rules | `not_null`, `pattern: "\\d+"` |
| `output_match` | ✅ | Final output matches regex | `pattern: "Found \\d+ results"` |
| `path_sequence` | V1.0 | Step order matches expected | `order: strict` |
| `timing` | V1.0 | Step duration in bounds | `max_duration_ms: 5000` |
| `output_schema` | V1.0 | Output validates JSON Schema | `schema: {…}` |
| `custom_script` | V1.0 | External script verdict | `script: ./checks/my.py` |

→ Complete reference: [assertions-guide.md](references/assertions-guide.md)

## Common Patterns

**1. Verify a tool was called**
```yaml
- id: tool-called
  type: tool_call
  target: { tool_name: "search" }
  condition: { exactly: 1 }
```

**2. Verify output quality**
```yaml
- id: output-has-answer
  type: output_match
  target: {}
  condition: { pattern: "(?i)(found|results|answer)", min_matches: 1 }
```

**3. Verify error handling**
```yaml
- id: graceful-empty
  type: output_match
  target: {}
  condition: { pattern: "(?i)(no results|not found|try again)" }
  severity: warning
```

→ More patterns and end-to-end scenarios: [workflows.md](references/workflows.md)

## Prerequisites

- Python 3.10+
- PyYAML (`pip install pyyaml`)
- Claude Code CLI (`claude`) on `$PATH`
- **LLM judging (V1.0)**: `ANTHROPIC_API_KEY` environment variable

## Project Structure

After `/agent-verify:init`, your project gains:

```
agent-verify/
├── config.yaml              # Global settings
├── assertions.yaml          # Shared assertion definitions
├── suites/                  # Test suites
│   └── default.yaml
├── baselines/               # Saved quality snapshots
└── reports/                 # Generated reports (.md/.json/.html)
```

Commit `agent-verify/` alongside your agent code. The Skill's own scripts live
under `<skill-install>/scripts/` and are never copied into your project.
