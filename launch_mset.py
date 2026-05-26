"""
mset-ai-pipeline launcher
Opens broker + 4 agent windows + telegram bot, arranges on screen.
  Top row:    Broker | Orchestrator | TelegramBot
  Bottom row: TestPlanAgent | TestCaseAgent | AutomationAgent
"""
import subprocess, time, requests
import win32gui, win32con, win32api

ROOT      = r"C:\Users\Administrator\Desktop\mset-ai-pipeline"
BROKER_URL = "http://127.0.0.1:7801"

screen_w = win32api.GetSystemMetrics(0)
screen_h = win32api.GetSystemMetrics(1)
half_h   = screen_h // 2
third_w  = screen_w // 3

# Top row:    Broker (left) | Orchestrator (center) | TelegramBot (right)
# Bottom row: TestPlanAgent | TestCaseAgent | AutomationAgent
grid = [
    (0,           0,      third_w, half_h),   # Broker        — top-left
    (third_w,     0,      third_w, half_h),   # Orchestrator  — top-center
    (third_w * 2, 0,      third_w, half_h),   # TelegramBot   — top-right
    (0,           half_h, third_w, half_h),   # TestPlanAgent — bottom-left
    (third_w,     half_h, third_w, half_h),   # TestCaseAgent — bottom-center
    (third_w * 2, half_h, third_w, half_h),   # AutomationAgent — bottom-right
]

# Each entry: (title, workdir, command, bg_color, fg_color)
# Black background for all — clean professional look
agents = [
    ("BROKER",          ROOT,                               "bun broker.ts",                             "Black", "Cyan"),
    ("ORCHESTRATOR",    f"{ROOT}\\orchestrator",            "claude --dangerously-skip-permissions",      "Black", "White"),
    ("TELEGRAM-BOT",    ROOT,                               "C:\\Python314\\python.exe telegram_bot.py",  "Black", "Green"),
    ("TEST-PLAN-AGENT", f"{ROOT}\\agents\\test-plan",       "claude --dangerously-skip-permissions",      "Black", "Magenta"),
    ("TEST-CASE-AGENT", f"{ROOT}\\agents\\test-cases",      "claude --dangerously-skip-permissions",      "Black", "Cyan"),
    ("AUTOMATION-AGENT",f"{ROOT}\\agents\\automation",      "claude --dangerously-skip-permissions",      "Black", "Yellow"),
]


def is_broker_running():
    try:
        requests.get(f"{BROKER_URL}/agents", timeout=1)
        return True
    except Exception:
        return False


def get_console_windows():
    hwnds = set()
    def cb(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            if win32gui.GetClassName(hwnd) in ("ConsoleWindowClass", "CASCADIA_HOSTING_WINDOW_CLASS"):
                hwnds.add(hwnd)
    win32gui.EnumWindows(cb, None)
    return hwnds


print(f"Screen: {screen_w}x{screen_h}")
print("Launching mset-ai-pipeline...\n")

window_handles = []

for i, (name, work_dir, cmd_str, bg_color, fg_color) in enumerate(agents):
    before = get_console_windows()

    role_line = {
        "BROKER":           "Message Broker  |  port 7801",
        "ORCHESTRATOR":     "Pipeline Coordinator  |  Agent 1",
        "TELEGRAM-BOT":     "Telegram Bridge  |  @Donna_mset_bot",
        "TEST-PLAN-AGENT":  "Test Planner  |  Agent 2",
        "TEST-CASE-AGENT":  "Test Case Writer  |  Agent 3",
        "AUTOMATION-AGENT": "Automation Code Gen  |  Agent 4",
    }.get(name, name)

    header = (
        f"$host.UI.RawUI.WindowTitle = '{name}'; "
        f"$host.UI.RawUI.BackgroundColor = '{bg_color}'; "
        f"$host.UI.RawUI.ForegroundColor = '{fg_color}'; "
        f"Clear-Host; "
        f"Write-Host ''; "
        f"Write-Host ('  ' + ('=' * 46)) -ForegroundColor {fg_color}; "
        f"Write-Host ('  ' + '{name}') -ForegroundColor {fg_color}; "
        f"Write-Host ('  ' + '{role_line}') -ForegroundColor {fg_color}; "
        f"Write-Host ('  ' + ('=' * 46)) -ForegroundColor {fg_color}; "
        f"Write-Host ''; "
        f"cd '{work_dir}'; "
        f"{cmd_str}"
    )

    cmd = f'start "{name}" powershell -NoExit -Command "{header}"'
    subprocess.Popen(cmd, shell=True)
    print(f"  Launched {name} (bg={bg_color}, fg={fg_color})...")

    if name == "BROKER":
        print("  Waiting for broker to be ready...")
        for _ in range(15):
            time.sleep(1)
            if is_broker_running():
                print("  Broker is up.")
                break
        else:
            print("  WARNING: Broker did not respond.")
    else:
        time.sleep(1.5)

    for _ in range(20):
        time.sleep(0.5)
        after = get_console_windows()
        new = after - before
        if new:
            window_handles.append((name, list(new)[0]))
            print(f"  Window tracked: {name}")
            break
    else:
        print(f"  WARNING: Window not found for {name}")

print("\nArranging windows...")
time.sleep(1)

for i, (name, hwnd) in enumerate(window_handles):
    if i >= len(grid):
        break
    x, y, w, h = grid[i]
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.MoveWindow(hwnd, x, y, w, h, True)
        print(f"  {name} -> ({x},{y}) {w}x{h}")
    except Exception as e:
        print(f"  Failed to move {name}: {e}")

print("\nAll 6 windows launched.")
print("Layout:")
print("  Top:    BROKER | ORCHESTRATOR | TELEGRAM-BOT")
print("  Bottom: TEST-PLAN | TEST-CASE | AUTOMATION")
print("\nSend NEW to @Donna_mset_bot to start a project.")
