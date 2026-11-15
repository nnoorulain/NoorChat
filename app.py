"""Serve NoorChat in your browser using Python's standard library."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from chatbot import get_reply
from history import load_history, save_exchange

FRONTEND = Path(__file__).resolve().parent / "frontend"
FILES = {
    "/": ("index.html", "text/html"),
    "/style.css": ("style.css", "text/css"),
    "/chat.js": ("chat.js", "text/javascript"),
    "/companion.webp": ("companion.webp", "image/webp"),
    "/companion-laptop.webp": ("companion-laptop.webp", "image/webp"),
    "/companion-phone.webp": ("companion-phone.webp", "image/webp"),
}
PORT = 8000


class ChatServer(BaseHTTPRequestHandler):
    def send_data(self, status, content_type, data):
        self.send_response(status)
        if content_type.startswith("text/") or content_type == "application/json":
            content_type += "; charset=utf-8"
        self.send_header("Content-Type", content_type)
        if content_type.startswith("application/json"):
            self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_json(self, status, payload):
        self.send_data(status, "application/json", json.dumps(payload).encode("utf-8"))

    def do_GET(self):
        if self.path == "/history":
            try:
                self.send_json(200, {"chats": load_history()})
            except (OSError, ValueError):
                self.send_json(500, {"error": "I couldn't open the saved chats."})
            return

        if self.path not in FILES:
            self.send_error(404)
            return
        filename, content_type = FILES[self.path]
        self.send_data(200, content_type, (FRONTEND / filename).read_bytes())

    def do_POST(self):
        if self.path != "/chat":
            self.send_error(404)
            return

        if self.headers.get_content_type() != "application/json":
            self.send_json(415, {"error": "Send the message as JSON."})
            return

        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 4096:
                raise ValueError
            payload = json.loads(self.rfile.read(size))
            message = payload["message"]
            if not isinstance(message, str) or not message.strip() or len(message) > 300:
                raise ValueError
            chat_id = payload.get("chat_id")
        except (ValueError, KeyError, TypeError):
            self.send_json(400, {"error": "Enter a message between 1 and 300 characters."})
            return

        result = get_reply(message)
        try:
            chat_id, chats = save_exchange(chat_id, {"message": message, **result})
        except (OSError, ValueError):
            self.send_json(500, {"error": "I couldn't save this reply to chat history."})
            return
        self.send_json(200, {**result, "chat_id": chat_id, "chats": chats})


if __name__ == "__main__":
    with ThreadingHTTPServer(("127.0.0.1", PORT), ChatServer) as server:
        print(f"NoorChat is ready at http://127.0.0.1:{PORT}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nNoorChat stopped.")
