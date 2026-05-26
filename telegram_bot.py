"""
mset-ai-pipeline Telegram Bot (@Donna_mset_bot)
Bridges Telegram chat with the mset broker.

Flow:
  Telegram message -> POST /send to broker (to: orchestrator)
  Orchestrator reply via SSE -> sendMessage to Telegram

Usage: python telegram_bot.py
"""
import requests, json, threading, time, sys

import os
from pathlib import Path

_env = Path(__file__).parent / ".env"
if _env.exists():
    for line in _env.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

BOT_TOKEN   = os.environ["MSET_BOT_TOKEN"]
OWNER_ID    = int(os.environ.get("MSET_OWNER_CHAT_ID", "1136475116"))
BROKER_URL  = os.environ.get("BROKER_URL", "http://localhost:7801")
AGENT_NAME  = "telegram-bot"
TG_API      = f"https://api.telegram.org/bot{BOT_TOKEN}"


def tg_send(chat_id: int, text: str):
    try:
        requests.post(f"{TG_API}/sendMessage", json={
            "chat_id": chat_id,
            "text": text
        }, timeout=10)
    except Exception as e:
        print(f"[tg] send error: {e}")


def tg_send_file(chat_id: int, file_path: str, caption: str = ""):
    try:
        with open(file_path, "rb") as f:
            requests.post(f"{TG_API}/sendDocument", data={
                "chat_id": chat_id,
                "caption": caption
            }, files={"document": f}, timeout=30)
    except Exception as e:
        print(f"[tg] file send error: {e}")


def register():
    for _ in range(10):
        try:
            r = requests.post(f"{BROKER_URL}/register",
                              json={"agent": AGENT_NAME}, timeout=3)
            if r.status_code == 200:
                print(f"[bot] Registered with broker as {AGENT_NAME}")
                return True
        except Exception:
            pass
        time.sleep(2)
    print("[bot] Could not register with broker — is it running?")
    return False


def broker_send(to: str, msg_type: str, payload: dict):
    try:
        requests.post(f"{BROKER_URL}/send", json={
            "from": AGENT_NAME,
            "to": to,
            "type": msg_type,
            "payload": payload
        }, timeout=5)
    except Exception as e:
        print(f"[bot] broker send error: {e}")


def listen_broker():
    """Poll broker for messages and forward to Telegram. Polling is reliable on Windows — no SSE."""
    print(f"[bot] Polling broker for messages...")
    while True:
        try:
            resp = requests.get(f"{BROKER_URL}/poll/{AGENT_NAME}", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                for msg in data.get("messages", []):
                    payload = msg.get("payload", {})
                    msg_type = msg.get("type", "")

                    if msg_type == "reply":
                        text = payload.get("text", "")
                        chat_id = payload.get("chat_id", OWNER_ID)
                        if text:
                            tg_send(int(chat_id), text)

                    elif msg_type == "send_file":
                        file_path = payload.get("file_path", "")
                        caption = payload.get("caption", "")
                        chat_id = payload.get("chat_id", OWNER_ID)
                        if file_path:
                            tg_send_file(int(chat_id), file_path, caption)

                    elif msg_type == "pipeline_complete":
                        chat_id = payload.get("chat_id", OWNER_ID)
                        summary = payload.get("summary", "Pipeline complete.")
                        files = payload.get("files", [])
                        tg_send(int(chat_id), summary)
                        for fp in files:
                            tg_send_file(int(chat_id), fp)
        except Exception as e:
            print(f"[bot] broker poll error: {e}")
        time.sleep(3)


def poll_telegram():
    """Long-poll Telegram for incoming messages and route to broker."""
    offset = 0
    print(f"[bot] Polling Telegram for messages...")
    tg_send(OWNER_ID, "mset pipeline bot online. Send NEW to start a project or type a project name to resume.")

    while True:
        try:
            resp = requests.get(f"{TG_API}/getUpdates", params={
                "offset": offset,
                "timeout": 30,
                "allowed_updates": ["message"]
            }, timeout=40)

            updates = resp.json().get("result", [])
            for update in updates:
                offset = update["update_id"] + 1
                msg = update.get("message", {})
                chat_id = msg.get("chat", {}).get("id")
                text = msg.get("text", "").strip()
                user = msg.get("from", {}).get("first_name", "User")

                if not text or chat_id != OWNER_ID:
                    continue

                print(f"[tg] {user}: {text}")
                broker_send("orchestrator", "user_message", {
                    "text": text,
                    "chat_id": chat_id,
                    "user": user
                })

        except Exception as e:
            print(f"[bot] poll error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    print("[bot] Starting mset Telegram bot (@Donna_mset_bot)...")

    if not register():
        sys.exit(1)

    broker_thread = threading.Thread(target=listen_broker, daemon=True)
    broker_thread.start()

    poll_telegram()
