"""
confirm_mset.py
After launch_mset.py arranges the 6 windows, clicks each one and types the wake message.

Layout (thirds x halves):
  Top row:    Broker | Orchestrator | TelegramBot
  Bottom row: TestPlanAgent | TestCaseAgent | AutomationAgent
"""
import pyautogui, time

sw, sh = pyautogui.size()

# Center of each window based on launch_mset.py grid (thirds x halves)
broker       = (int(sw * (1/6)),   int(sh * 0.25))   # top-left third center
orchestrator = (int(sw * 0.5),     int(sh * 0.25))   # top-center third center
telegram_bot = (int(sw * (5/6)),   int(sh * 0.25))   # top-right third center
test_plan    = (int(sw * (1/6)),   int(sh * 0.75))   # bottom-left third center
test_cases   = (int(sw * 0.5),     int(sh * 0.75))   # bottom-center third center
automation   = (int(sw * (5/6)),   int(sh * 0.75))   # bottom-right third center


def wake_agent(pos, message):
    pyautogui.click(pos)
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(3)
    pyautogui.typewrite(message, interval=0.05)
    pyautogui.press('enter')
    time.sleep(5)


print("Waiting 12s for Claude windows to load...")
time.sleep(12)

# Wake worker agents first (register and start polling)
print("Waking AutomationAgent (bottom-right)...")
wake_agent(automation, "register with broker and start polling")

print("Waking TestCaseAgent (bottom-center)...")
wake_agent(test_cases, "register with broker and start polling")

print("Waking TestPlanAgent (bottom-left)...")
wake_agent(test_plan, "register with broker and start polling")

# Wake Orchestrator last
print("Waking Orchestrator (top-center)...")
wake_agent(orchestrator, "hello ,register with broker and start polling")

print("\nDone. Send NEW to @Donna_mset_bot to start a project.")
