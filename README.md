# mset-ai-pipeline

AI-powered test automation pipeline. Four autonomous Claude Code agents collaborate to turn a feature description into a complete, ready-to-run WebDriverIO test suite — with human review gates at each step.

---

## What it does

1. You send a feature description to Donna (Orchestrator) via Telegram or console
2. Donna asks 6 intake questions (project name, platform, test type, priority, app)
3. **Agent 2** writes a structured test plan → sent to you for review
4. You approve (`PROCEED`) or request changes (`REVISE [what to change]`)
5. **Agent 3** writes test cases classified as Manual / Automate / Hybrid → sent to you for review
6. You approve or revise
7. **Agent 4** generates runnable WebDriverIO `.spec.ts` files for all automatable cases
8. All output files delivered to Telegram

---

## Agent Breakdown

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| Orchestrator (Donna) | Coordinator — intake, routing, human checkpoints | Feature description | project.config.json, session files |
| TestPlanAgent | Test planner | Feature + config | test-plan.md |
| TestCaseAgent | Test case writer + classifier | Test plan | test-cases.json |
| AutomationAgent | Code generator | Automatable cases | *.spec.ts + *.page.ts |

---

## Architecture

```
User (Telegram @Donna_mset_bot or console)
        |
        v
  ORCHESTRATOR  ──── plan_request ────>  TestPlanAgent
        |                                      |
        |<──── plan_ready ─────────────────────+
        |  [sends test-plan.md to Telegram, waits for PROCEED]
        |
        |──── cases_request ──────────>  TestCaseAgent
        |                                      |
        |<──── cases_ready ────────────────────+
        |  [sends test-cases.json to Telegram, waits for PROCEED]
        |
        |──── automation_request ─────>  AutomationAgent
        |                                      |
        |<──── automation_ready ───────────────+
        |
        v
User receives all 3 output files via Telegram
```

All agent-to-agent communication goes through a central **message broker** (`broker.ts`, Bun/TypeScript). Agents poll the broker on a fixed interval. The broker is stateless — it queues messages until each agent picks them up.

> Full technical design — broker protocol, agent prompt engineering, and classification framework — discussed during interview.

---

## Prerequisites

- [Bun](https://bun.sh/) — for the message broker
- [Claude Code](https://claude.ai/code) — `claude` CLI installed globally
- Python 3.x — for launcher and Telegram bot
- `pip install pyautogui pywin32 requests`

---

## Setup

```bash
git clone https://github.com/Guneet-S/mset-ai-pipeline.git
cd mset-ai-pipeline
```

Copy `.env.example` to `.env` and fill in your Telegram bot token and chat ID (see `.env.example` for the required fields).

---

## Running the Pipeline

Double-click `start-all.bat`.

Opens 6 terminal windows (Broker, Orchestrator, Telegram Bot, and 3 specialist agents) tiled on screen. Each agent starts, registers with the broker, and enters a polling loop.

Then send **NEW** to `@Donna_mset_bot` on Telegram to start a project.

---

## Telegram Control

- Send `NEW` to start a new project
- Answer Donna's 6 intake questions
- Receive `test-plan.md` for review — reply `PROCEED` or `REVISE [what to change]`
- Receive `test-cases.json` for review — reply `PROCEED` or `REVISE`
- Receive all output files when the pipeline completes

---

## Output Files

All outputs saved under `projects/<project-name>/output/`:

| File | Agent | Description |
|------|-------|-------------|
| `output/test-plan.md` | Agent 2 | Structured test plan (scope, approach, risks, timeline) |
| `output/test-cases.json` | Agent 3 | Full test case list with Manual / Automate / Hybrid labels |
| `output/specs/*.spec.ts` | Agent 4 | WebDriverIO + Appium spec files, one per module |
| `output/pages/*.page.ts` | Agent 4 | Page Object Models |

Each project folder also contains:
- `SESSION.md` — pipeline progress checklist
- `HANDOFF.md` — resume state (pick up where you left off)

---

## Running the Generated Tests

```bash
# Install WebDriverIO dependencies
npm init wdio@latest

# Start Appium (for Android) or run directly (for web)
npx appium

# Run all generated specs
npx wdio run wdio.conf.ts
```

The included `wdio.conf.ts` picks up all spec files from `projects/*/output/specs/` automatically.

---

## Sample Output

The `sample-output/` folder contains real output from a pipeline run targeting [https://www.saucedemo.com](https://www.saucedemo.com):

| File | Description |
|------|-------------|
| `sample-output/test-plan.md` | Structured test plan (8 sections) |
| `sample-output/test-cases.json` | 14 test cases — 7 Automate, 6 Manual, 1 Hybrid |
| `sample-output/specs/authentication.spec.ts` | 7 automated WebDriverIO tests |
| `sample-output/pages/login.page.ts` | Page Object for the login screen |

---

## Future Improvements

- **Zephyr Scale** — export test-cases.json to Jira via REST API
- **Sauce Labs cloud** — execute specs on real cloud devices
- **CI/CD** — GitHub Actions trigger on PR to auto-generate specs for new features
- **Multi-module** — extend AutomationAgent to generate specs for full apps (10+ modules)
