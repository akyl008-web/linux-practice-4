#!/usr/bin/env python3
"""ПР-4, вариант B, задание 2. Загрузка 20 URL: последовательно,
ThreadPoolExecutor(4), ProcessPoolExecutor(4). 3 повтора, медиана.
Сервер slow_server.py запускается и останавливается автоматически."""
import os
import socket
import statistics
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

PORT = 8000
URLS = [f"http://127.0.0.1:{PORT}/file{i:02d}" for i in range(1, 21)]
WORKERS = 4
REPEATS = 3


def fetch(url):
    with urllib.request.urlopen(url) as r:
        return len(r.read())


def sequential():
    return sum(fetch(u) for u in URLS)


def with_threads():
    with ThreadPoolExecutor(WORKERS) as ex:
        return sum(ex.map(fetch, URLS))


def with_processes():
    with ProcessPoolExecutor(WORKERS) as ex:
        return sum(ex.map(fetch, URLS))


def wait_for_server():
    for _ in range(50):
        try:
            socket.create_connection(("127.0.0.1", PORT), timeout=0.1).close()
            return
        except OSError:
            time.sleep(0.1)
    sys.exit("Сервер не запустился")


def main():
    server = subprocess.Popen([sys.executable, "slow_server.py", str(PORT)])
    try:
        wait_for_server()
        print(f"Ядер: {len(os.sched_getaffinity(0))}  URL: {len(URLS)}  "
              f"задержка ответа: 0.5 с  повторов: {REPEATS}")
        print(f"{'Способ':<26}{'прогоны, с':<20}{'медиана, с':>10}  байт")
        methods = [("последовательно", sequential),
                   ("ThreadPoolExecutor(4)", with_threads),
                   ("ProcessPoolExecutor(4)", with_processes)]
        for name, fn in methods:
            times = []
            for _ in range(REPEATS):
                t0 = time.perf_counter()
                total = fn()
                times.append(time.perf_counter() - t0)
            runs = " ".join(f"{t:.2f}" for t in times)
            print(f"{name:<26}{runs:<20}{statistics.median(times):>10.2f}  {total}", flush=True)
    finally:
        server.terminate()  # не оставляем фоновый сервер
        server.wait()


if __name__ == "__main__":
    main()