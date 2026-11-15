"""Keep the two most recent chat sessions in a local JSON file."""

import json
import time
from pathlib import Path
from threading import Lock
from uuid import uuid4

HISTORY_FILE = Path(__file__).resolve().with_name("chat_history.json")
RETENTION_SECONDS = 24 * 60 * 60
CHAT_LIMIT = 2
HISTORY_LOCK = Lock()


def read_history():
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []


def write_history(chats):
    # Replace the old file only after the new JSON is fully written.
    temporary_file = HISTORY_FILE.with_suffix(".tmp")
    temporary_file.write_text(json.dumps(chats, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary_file.replace(HISTORY_FILE)


def recent_chats(chats, now):
    return [chat for chat in chats if now - chat["updated_at"] < RETENTION_SECONDS][:CHAT_LIMIT]


def load_history():
    with HISTORY_LOCK:
        saved = read_history()
        chats = recent_chats(saved, time.time())
        if chats != saved:
            write_history(chats)
        return chats


def save_exchange(chat_id, exchange):
    with HISTORY_LOCK:
        now = time.time()
        chats = recent_chats(read_history(), now)
        chat = next((chat for chat in chats if chat["id"] == chat_id), None)
        if chat is None:
            chat = {"id": uuid4().hex, "exchanges": []}
        else:
            chats.remove(chat)
        chat["exchanges"].append(exchange)
        chat["updated_at"] = now
        chats.insert(0, chat)
        chats = chats[:CHAT_LIMIT]
        write_history(chats)
        return chat["id"], chats
