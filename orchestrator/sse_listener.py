"""Persistent SSE listener — reconnects on disconnect, appends messages to queue.jsonl"""
import json
import time
import urllib.request
import urllib.error
from pathlib import Path

STREAM_URL = "http://localhost:7801/stream/orchestrator"
QUEUE_FILE = Path(__file__).parent / "msg_queue.jsonl"


def listen():
    print(f"[listener] connecting to {STREAM_URL}", flush=True)
    try:
        with urllib.request.urlopen(STREAM_URL, timeout=120) as resp:
            for raw in resp:
                line = raw.decode("utf-8").strip()
                if not line.startswith("data:"):
                    continue
                payload = line[5:].strip()
                if not payload:
                    continue
                try:
                    msg = json.loads(payload)
                    with QUEUE_FILE.open("a") as f:
                        f.write(json.dumps(msg) + "\n")
                    print(f"[listener] queued: {msg.get('type')} from {msg.get('from')}", flush=True)
                except json.JSONDecodeError:
                    pass
    except Exception as e:
        print(f"[listener] stream closed ({e}), reconnecting in 2s…", flush=True)
        time.sleep(2)


if __name__ == "__main__":
    print("[listener] started", flush=True)
    while True:
        listen()
