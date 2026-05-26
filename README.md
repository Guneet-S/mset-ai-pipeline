# mset-ai-pipeline

AI-powered test automation pipeline. Four autonomous Claude Code agents collaborate to turn a feature description into a complete, ready-to-run WebDriverIO test suite — with human review gates at each step.

---

## What it does

1. You send a feature description to Donna (Orchestrator) via Telegram or console
2. Donna asks 7 intake questions (project name, platform, test type, priority, app, existing framework path)
3. **Agent 2** writes a structured test plan → sent to you for review
4. You approve (`PROCEED`) or request changes (`REVISE [what to change]`)
5. **Agent 3** writes test cases classified as Manual / Automate / Hybrid → sent to you for review
6. You approve or revise
7. **Agent 4** generates runnable WebDriverIO `.spec.ts` files for all automatable cases
8. Orchestrator builds a traceability matrix mapping each module to its test case IDs and spec file
9. All output files (test plan, test cases, traceability matrix, spec files) delivered to Telegram

---

## Agent Breakdown

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| Orchestrator (Donna) | Coordinator — intake, routing, human checkpoints | Feature description | project.config.json, session files |
| TestPlanAgent | Test planner | Feature + config | test-plan.md |
| TestCaseAgent | Test case writer + classifier | Test plan | test-cases.json |
| AutomationAgent | Repo-aware code generator — scans existing framework before generating | Automatable cases + framework path | *.spec.ts + *.page.ts |

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
User receives all output files via Telegram (test-plan.md, test-cases.json, traceability.json, *.spec.ts)
```

All agent-to-agent communication goes through a central **message broker** (`broker.ts`, Bun/TypeScript). Agents poll the broker on a fixed interval. The broker is stateless — it queues messages until each agent picks them up.

If an existing framework path is provided at intake, AutomationAgent scans `framework/pages/`, `framework/helpers/`, and `framework/selectors/` before generating — output extends the existing codebase rather than creating a parallel structure.

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

Launch all 6 processes. Each opens in its own terminal window arranged in a 2x3 grid:

```
+--------------------+--------------------+--------------------+
|      BROKER        |   ORCHESTRATOR     |   TELEGRAM-BOT     |
+--------------------+--------------------+--------------------+
|  TEST-PLAN-AGENT   |  TEST-CASE-AGENT   | AUTOMATION-AGENT   |
+--------------------+--------------------+--------------------+
```

Each agent starts, registers with the broker, and enters a polling loop.

Then send **NEW** to `@Donna_mset_bot` on Telegram to start a project.

---

## Telegram Control

- Send `NEW` to start a new project
- Answer Donna's 7 intake questions (Q7 asks for an existing framework path — type path or "no")
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
| `output/pages/*.page.ts` | Agent 4 | Page Object Models — extend BasePage from existing framework when framework path is provided |
| `output/traceability.json` | Orchestrator | Traceability matrix — maps each module to its test case IDs and automation spec file |

Each project folder also contains:
- `SESSION.md` — pipeline progress checklist
- `HANDOFF.md` — resume state (pick up where you left off)

---

## Existing Framework Integration

The `framework/` folder simulates a company's existing automation codebase. It contains:

| File | Purpose |
|------|---------|
| `framework/pages/base.page.ts` | BasePage — parent class all page objects extend |
| `framework/pages/product.page.ts` | Example existing page written by the QA team |
| `framework/helpers/wait.helper.ts` | Shared wait utilities (waitForElement, waitForText, waitForUrl) |
| `framework/selectors/app.selectors.ts` | Centralised selector constants — all selectors in one place |

When you provide this path at Q7, AutomationAgent reads all four files before writing a single line of code. Generated page objects extend `BasePage`, import selectors from `app.selectors.ts`, and use helpers from `wait.helper.ts` — output that looks like it was written by the existing team, not generated from scratch.

To test with the included sample framework, answer Q7 with:
```
C:/Users/Administrator/Desktop/mset-ai-pipeline/framework
```

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

## Design Decisions

**Why Claude Code CLI as the agent runtime?**
Each agent is a Claude Code CLI process running its own CLAUDE.md instruction file. This gives every agent a persistent, stateful session with full tool access (file I/O, HTTP, bash) without any wrapper code. The agent IS the LLM — no orchestration SDK needed. Each agent has a single responsibility and can be updated, replaced, or debugged independently.

**Why a message broker instead of direct agent calls?**
Agents communicate through a central HTTP broker (`broker.ts`) rather than calling each other directly. This decouples them — if one agent is slow, the Orchestrator keeps polling and the pipeline does not stall. If an agent crashes and restarts, it re-registers and picks up from the queue. Direct agent-to-agent calls would create tight coupling and make the pipeline brittle.

**Why file paths in broker messages, not content?**
Passing full JSON payloads through the broker caused hangs when test case output was large (50+ cases). The fix: agents send only the file path, and downstream agents read from disk directly. The broker stays stateless and lightweight regardless of payload size.

**Why polling instead of server-sent events?**
SSE streams on Windows dropped with reconnect errors, causing duplicate message delivery to the Telegram bot. Replacing the SSE listener with a simple polling loop eliminated duplicates entirely — easier to reason about and debug.

**Why framework ingestion before generation?**
AutomationAgent reads the existing page objects, selectors, and helpers before writing any code. This ensures generated output extends the existing codebase — same base class, same selector naming, same helper imports — rather than creating a parallel structure that a real team would have to merge and reconcile.

---

## Challenges

**Multi-process agent communication on Windows (Infrastructure)**
Running four independent Claude Code CLI processes that reliably communicate on a single machine required solving a message delivery problem. Server-sent events (SSE) dropped connections on reconnect and re-delivered queued messages, causing duplicates across the Telegram bot and all agents. The fix was replacing every SSE listener with a simple polling loop — each agent polls the broker on a fixed interval, which is stateless, restartable, and produces no duplicates. This pattern also means any agent can crash and resume without losing messages.

**Test case classification accuracy (QA)**
Deciding whether a test case should be Automate, Manual, or Hybrid is a judgment call that the agent had to make consistently across different feature types and platforms. Early runs produced inconsistent results — visual layout checks tagged as Automate, simple login flows tagged as Hybrid. The fix was defining explicit rule-based classification criteria: Automate for anything repetitive, data-driven, or regression-critical; Manual for anything requiring human judgment on UI feel or visual accuracy; Hybrid for flows where automation handles setup but a human verifies the final state. Consistency improved significantly once the rules were unambiguous.

**Calibrating test volume per test type (QA)**
Without explicit volume targets, the agent over-generated for smoke runs (30+ cases instead of ~10) and under-covered regression scenarios. Fixed by defining scaling rules per test type and priority filter combination, and specifying mandatory coverage areas (authentication, catalog, cart, checkout, UX) that must always be represented. This ensured output was proportionate and complete without manual trimming after each generation run.

---

## What I Would Improve

1. **Zephyr Scale integration** — the pipeline already generates `traceability.json` (requirement → test case → script path); next step is pushing that directly to Jira via the Zephyr Scale REST API so the matrix lives in the test management system, not just the local output folder
2. **Multi-source input** — accept Confluence pages, Jira tickets, or Figma specs as requirement input alongside free-text descriptions
3. **CI/CD trigger** — GitHub Actions workflow to auto-run the pipeline when a new feature branch is opened
4. **Execution layer** — connect `wdio.conf.ts` to Sauce Labs cloud to run generated specs on real devices immediately after generation
5. **Multi-module generation** — AutomationAgent currently generates one spec file per module; extend to handle full apps with 10+ modules in a single run

---

## Future Improvements

- **Zephyr Scale** — export test-cases.json to Jira via REST API
- **Sauce Labs cloud** — execute specs on real cloud devices
- **CI/CD** — GitHub Actions trigger on PR to auto-generate specs for new features
- **Multi-module** — extend AutomationAgent to generate specs for full apps (10+ modules)
