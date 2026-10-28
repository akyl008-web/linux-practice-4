#!/usr/bin/env python3
"""ПР-4. Локальный HTTP-сервер, имитирующий медленную сеть:
каждый ответ — 100 КБ с задержкой 0.5 с. Запуск: python3 slow_server.py [порт]"""
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DELAY = 0.5
BODY = b"x" * 100_000


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        time.sleep(DELAY)  # имитация задержки сети
        self.send_response(200)
        self.send_header("Content-Length", str(len(BODY)))
        self.end_headers()
        self.wfile.write(BODY)

    def log_message(self, *args):
        pass  # не засорять вывод


port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()