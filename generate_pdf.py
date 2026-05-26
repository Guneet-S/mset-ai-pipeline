"""
generate_pdf.py
Generates mset-ai-pipeline visual architecture PDF.
Output: C:/Users/Administrator/Desktop/mset_architecture.pdf
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

W, H = A4
styles = getSampleStyleSheet()

# Color palette
C_DARK   = colors.HexColor("#1a1a2e")
C_BLUE   = colors.HexColor("#0f3460")
C_ACCENT = colors.HexColor("#e94560")
C_TEAL   = colors.HexColor("#16213e")
C_GREEN  = colors.HexColor("#0d7377")
C_YELLOW = colors.HexColor("#f5a623")
C_PURPLE = colors.HexColor("#6c5ce7")
C_PINK   = colors.HexColor("#fd79a8")
C_LIGHT  = colors.HexColor("#f8f9fa")
C_GRAY   = colors.HexColor("#6c757d")
C_WHITE  = colors.white

def style(name, **kw):
    s = ParagraphStyle(name, parent=styles["Normal"], **kw)
    return s

TITLE    = style("T", fontSize=22, textColor=C_WHITE, backColor=C_DARK, alignment=TA_CENTER, spaceAfter=4, spaceBefore=4, fontName="Helvetica-Bold", leading=28)
HEADING  = style("H", fontSize=13, textColor=C_WHITE, backColor=C_BLUE, alignment=TA_LEFT, spaceBefore=10, spaceAfter=4, fontName="Helvetica-Bold", leftIndent=4, leading=18)
SUBHEAD  = style("SH", fontSize=10, textColor=C_DARK, fontName="Helvetica-Bold", spaceAfter=2, spaceBefore=4)
BODY     = style("B", fontSize=9, textColor=C_DARK, fontName="Helvetica", leading=13)
CODE     = style("C", fontSize=8, textColor=C_BLUE, fontName="Courier", leading=12)
SMALL    = style("SM", fontSize=8, textColor=C_GRAY, fontName="Helvetica")
CENTERED = style("CEN", fontSize=9, textColor=C_DARK, alignment=TA_CENTER, fontName="Helvetica")
ARROW    = style("AR", fontSize=14, textColor=C_ACCENT, alignment=TA_CENTER, fontName="Helvetica-Bold")


def section_label(text, bg=C_BLUE):
    return Table([[Paragraph(text, style("SL", fontSize=10, textColor=C_WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER))]],
        colWidths=[170*mm],
        style=TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), bg),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
        ]))


def agent_box(name, role, color, detail=""):
    inner = [[
        Paragraph(name, style("AN", fontSize=11, textColor=C_WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph(role, style("AR2", fontSize=8, textColor=C_WHITE, fontName="Helvetica", alignment=TA_CENTER)),
    ]]
    if detail:
        inner.append([Paragraph(detail, style("AD", fontSize=7, textColor=C_LIGHT, fontName="Courier", alignment=TA_CENTER)), ""])
    t = Table([[Paragraph(name, style("AN", fontSize=11, textColor=C_WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER))],
               [Paragraph(role, style("AR2", fontSize=8, textColor=C_LIGHT, fontName="Helvetica", alignment=TA_CENTER))]],
        colWidths=[80*mm],
        style=TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), color),
            ("TOPPADDING", (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING", (0,0), (-1,-1), 6),
            ("RIGHTPADDING", (0,0), (-1,-1), 6),
            ("ROUNDEDCORNERS", (0,0), (-1,-1), 4),
        ]))
    return t


def flow_row(*boxes, arrow=True):
    cells = []
    for i, b in enumerate(boxes):
        cells.append(b)
        if arrow and i < len(boxes)-1:
            cells.append(Paragraph("→", ARROW))
    widths = []
    for i in range(len(cells)):
        if i % 2 == 0:
            widths.append(80*mm)
        else:
            widths.append(10*mm)
    return Table([cells], colWidths=widths, style=TableStyle([
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ]))


def info_table(rows, col_widths=None, header_bg=C_BLUE):
    col_widths = col_widths or [60*mm, 110*mm]
    data = []
    for i, (k, v) in enumerate(rows):
        data.append([
            Paragraph(k, style("IK", fontSize=8, textColor=C_WHITE if i==0 else C_DARK, fontName="Helvetica-Bold")),
            Paragraph(v, style("IV", fontSize=8, textColor=C_WHITE if i==0 else C_DARK, fontName="Helvetica"))
        ])
    ts = TableStyle([
        ("BACKGROUND", (0,0), (-1,0), header_bg),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [C_LIGHT, C_WHITE]),
        ("GRID", (0,0), (-1,-1), 0.5, C_GRAY),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
    ])
    return Table(data, colWidths=col_widths, style=ts)


def build():
    doc = SimpleDocTemplate(
        "C:/Users/Administrator/Desktop/mset_architecture.pdf",
        pagesize=A4,
        leftMargin=15*mm, rightMargin=15*mm,
        topMargin=15*mm, bottomMargin=15*mm
    )
    story = []

    # ── TITLE ────────────────────────────────────────────────────────────
    story.append(Table([[Paragraph("mset-ai-pipeline", TITLE)],
                         [Paragraph("AI-Powered Test Automation Pipeline — Architecture & Build Summary", style("SUB", fontSize=11, textColor=C_LIGHT, alignment=TA_CENTER, fontName="Helvetica"))]],
        colWidths=[180*mm],
        style=TableStyle([("BACKGROUND",(0,0),(-1,-1),C_DARK),("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10)])))
    story.append(Spacer(1, 6*mm))

    # ── SECTION 1: WHAT WE BUILT ─────────────────────────────────────────
    story.append(section_label("SECTION 1 — WHAT WE BUILT", C_BLUE))
    story.append(Spacer(1, 3*mm))
    story.append(info_table([
        ("Component", "Description"),
        ("broker.ts", "Bun HTTP server on port 7801 — message queue, SSE push, poll fallback"),
        ("Orchestrator", "Claude Code agent — intake questions, project setup, pipeline routing"),
        ("TestPlanAgent", "Claude Code agent — generates structured test plan from feature description"),
        ("TestCaseAgent", "Claude Code agent — writes test cases JSON with Manual/Automate/Hybrid labels"),
        ("AutomationAgent", "Claude Code agent — generates WebDriverIO .spec.ts files via Page Object Model"),
        ("telegram_bot.py", "Telegram bot (@Donna_mset_bot) — bridges Telegram chat with broker"),
        ("launch_mset.py", "Python launcher — opens and arranges 5 windows on screen"),
        ("confirm_mset.py", "Python script — auto-clicks and wakes each agent after launch"),
        ("start-all.bat", "One double-click to launch the entire system"),
        (".env / .env.example", "Secure token storage — .env gitignored, .env.example committed"),
    ], col_widths=[55*mm, 125*mm]))
    story.append(Spacer(1, 5*mm))

    # ── SECTION 2: PIPELINE FLOW ─────────────────────────────────────────
    story.append(section_label("SECTION 2 — PIPELINE FLOW", C_GREEN))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("INPUT", SUBHEAD))
    story.append(flow_row(
        agent_box("Telegram / Console", "User sends feature description", C_PURPLE),
        agent_box("ORCHESTRATOR", "Agent 1 — 6 intake questions, creates project folder", C_BLUE),
    ))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("↓  plan_request  { feature, platform, test_type, project_path }", CODE))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("STEP 1 — TEST PLAN", SUBHEAD))
    story.append(flow_row(
        agent_box("TestPlanAgent", "Agent 2 — scope, approach, test types, tools", C_GREEN),
        agent_box("output/test-plan.md", "Saved to project folder", C_TEAL),
    ))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("↓  plan_ready  { file: project_path/output/test-plan.md }", CODE))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("STEP 2 — TEST CASES", SUBHEAD))
    story.append(flow_row(
        agent_box("TestCaseAgent", "Agent 3 — writes cases, classifies each Manual/Automate/Hybrid", C_YELLOW),
        agent_box("output/test-cases.json", "N total, M automate cases", C_TEAL),
    ))
    story.append(Spacer(1, 2*mm))

    # Split arrow
    story.append(Table([
        [Paragraph("↓  cases_ready  { file, total: N, automate_count: M }", CODE)],
        [Paragraph("ORCHESTRATOR reads file → filters type='Automate' → sends cases_file path to AutomationAgent", SMALL)],
    ], colWidths=[170*mm]))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("STEP 3 — AUTOMATION CODE", SUBHEAD))
    story.append(flow_row(
        agent_box("AutomationAgent", "Agent 4 — reads cases file, generates .spec.ts per module", C_ACCENT),
        agent_box("output/specs/*.spec.ts", "login.spec.ts, cart.spec.ts, checkout.spec.ts", C_TEAL),
    ))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("↓  automation_ready  { files: [...], summary }  →  Orchestrator sends to Telegram", CODE))
    story.append(Spacer(1, 5*mm))

    # ── SECTION 3: BROKER ────────────────────────────────────────────────
    story.append(section_label("SECTION 3 — MESSAGE BROKER (broker.ts)", C_TEAL))
    story.append(Spacer(1, 3*mm))
    story.append(info_table([
        ("Endpoint", "Method / Purpose"),
        ("POST /register", "Agent registers on startup with name"),
        ("POST /send", "Queue message { from, to, type, payload } for target agent"),
        ("GET /poll/:agent", "Fetch + drain pending messages — agents poll every 5s"),
        ("GET /stream/:agent", "SSE push — broker pushes instantly when message queued"),
        ("GET /agents", "List all registered agents"),
    ], col_widths=[60*mm, 110*mm]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Key design: payloads contain FILE PATHS only — never full file content. Agents read from disk. Prevents broker hanging on large JSON.", BODY))
    story.append(Spacer(1, 5*mm))

    # ── SECTION 4: PROJECT FOLDER ────────────────────────────────────────
    story.append(section_label("SECTION 4 — PROJECT FOLDER STRUCTURE", C_PURPLE))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("""projects/
  &lt;project-name&gt;/
    project.config.json    Platform, test type, app, priority filter
    SESSION.md             Pipeline checklist (step status)
    HANDOFF.md             Resume state — updated after each step
    LEARNING.md            Edge cases and agent observations
    LESSONS.md             Post-run retrospective
    output/
      test-plan.md         Agent 2 output
      test-cases.json      Agent 3 output (all cases with type field)
      specs/
        login.spec.ts      Agent 4 — login module
        cart.spec.ts       Agent 4 — cart module
        checkout.spec.ts   Agent 4 — checkout module""", CODE))
    story.append(Spacer(1, 5*mm))

    # ── SECTION 5: TELEGRAM ──────────────────────────────────────────────
    story.append(section_label("SECTION 5 — TELEGRAM INTEGRATION", C_ACCENT))
    story.append(Spacer(1, 3*mm))
    story.append(flow_row(
        agent_box("@Donna_mset_bot", "Telegram — user sends NEW or feature description", C_PURPLE),
        agent_box("telegram_bot.py", "Registered as 'telegram-bot' agent in broker", C_TEAL),
        agent_box("ORCHESTRATOR", "Receives via poll, replies back through broker", C_BLUE),
    ))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Output files (test-plan.md, test-cases.json) delivered as Telegram document attachments on pipeline completion.", BODY))
    story.append(Spacer(1, 5*mm))

    # ── SECTION 6: TECH STACK ────────────────────────────────────────────
    story.append(section_label("SECTION 6 — TECH STACK", C_BLUE))
    story.append(Spacer(1, 3*mm))
    story.append(info_table([
        ("Layer", "Technology"),
        ("Broker", "Bun + TypeScript — zero external dependencies"),
        ("Agents", "Claude Code CLI (claude --dangerously-skip-permissions)"),
        ("Test Specs", "WebDriverIO v8 + Appium + Page Object Model + TypeScript"),
        ("Demo App", "Sauce Labs My Demo App (React Native, Android)"),
        ("Launcher", "Python + win32gui (window positioning + auto-wake)"),
        ("Telegram", "Python + Telegram Bot API (long polling)"),
        ("Secrets", ".env file (gitignored) + .env.example (committed)"),
    ], col_widths=[55*mm, 125*mm]))
    story.append(Spacer(1, 5*mm))

    # ── SECTION 7: FUTURE ────────────────────────────────────────────────
    story.append(section_label("SECTION 7 — FUTURE IMPROVEMENTS", C_GRAY))
    story.append(Spacer(1, 3*mm))
    story.append(info_table([
        ("Improvement", "Description"),
        ("wdio.conf.ts", "Configuration file to actually run the generated specs on Android emulator"),
        ("Zephyr Scale", "Export test-cases.json to Zephyr via REST API for test management"),
        ("Sauce Labs Cloud", "Execute specs on Sauce Labs cloud instead of local emulator"),
        ("CI/CD Integration", "GitHub Actions trigger pipeline on PR — auto-generate specs for new features"),
        ("Push model (waker)", "Replace polling with push model using waker script (like GPS system)"),
    ], col_widths=[55*mm, 125*mm]))

    # ── SECTION 8: INTERVIEW Q&A ─────────────────────────────────────────
    story.append(section_label("SECTION 8 — INTERVIEW Q&A", C_BLUE))
    story.append(Spacer(1, 3*mm))
    story.append(info_table([
        ("Question", "Answer"),
        ("Why 4 agents not 1?", "Single responsibility — Planner, Writer, Automator each has one job. Swap or improve one without touching others. Mirrors real QA teams."),
        ("Why a message broker?", "Decoupling. Agents don't call each other directly. If one is slow or crashes, others are unaffected. Broker queues messages until the agent is ready."),
        ("Why file paths in messages?", "Early version sent full JSON through the broker. 70+ test cases caused CLOSE_WAIT hangs. File paths are tiny — agents read from disk directly."),
        ("How does Manual/Automate work?", "TestCaseAgent reads classification rules in its CLAUDE.md. Automate = repetitive/data-driven. Manual = exploratory/visual. Only Automate cases go to Agent 4."),
        ("Why not run the tests?", "Pipeline job is generation, not execution. wdio.conf.ts is provided — any CI/CD can pick up the specs and run them. Separation is intentional."),
        ("What if an agent fails?", "Orchestrator times out after 60s, sends ONE error to Telegram, waits for RETRY. HANDOFF.md tracks last completed step — pipeline resumes without restarting."),
        ("Can it scale?", "Yes. test_type controls scope: smoke 10 cases, functional 25, regression 50+. Revision loop adds cases without full restart. Multiple projects run in parallel folders."),
    ], col_widths=[70*mm, 110*mm]))

    story.append(Spacer(1, 5*mm))
    story.append(HRFlowable(width="100%", color=C_GRAY))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("Built by Guneet Singh — GPS Agent System | mset-ai-pipeline v1.0", SMALL))

    doc.build(story)
    print("PDF generated: C:/Users/Administrator/Desktop/mset_architecture.pdf")


if __name__ == "__main__":
    build()
