#!/usr/bin/env python3
"""ПР-4, вариант B, задание 1. Сумма чисел из numbers.txt тремя способами:
1 поток, 4 потока (threading), 4 процесса (multiprocessing). 3 повтора, медиана.
Каждый исполнитель сам читает и разбирает свою часть файла — это CPU-задача.
Время генерации numbers.txt в замер не входит."""
import multiprocessing
import os
import statistics
import sys
import threading
import time

PATH = "numbers.txt"
WORKERS = 4
REPEATS = 3


def chunks(path, n):
    """Делит файл на n частей по границам строк: [(start, end), ...]."""
    size = os.path.getsize(path)
    bounds = [0]
    with open(path, "rb") as f:
        for i in range(1, n):
            f.seek(size * i // n)
            f.readline()  # дойти до начала следующей строки
            bounds.append(f.tell())
    bounds.append(size)
    return list(zip(bounds, bounds[1:]))


def sum_part(path, start, end):
    with open(path, "rb") as f:
        f.seek(start)
        data = f.read(end - start)
    return sum(map(int, data.split()))


def one_thread():
    return sum_part(PATH, 0, os.path.getsize(PATH))


def with_threads():
    results = [0] * WORKERS

    def work(i, start, end):
        results[i] = sum_part(PATH, start, end)

    threads = [threading.Thread(target=work, args=(i, s, e))
               for i, (s, e) in enumerate(chunks(PATH, WORKERS))]
    for t in threads:
        t.start()  # сначала запускаем все потоки...
    for t in threads:
        t.join()   # ...и только потом ждём
    return sum(results)


def with_processes():
    with multiprocessing.Pool(WORKERS) as pool:
        return sum(pool.starmap(sum_part, [(PATH, s, e) for s, e in chunks(PATH, WORKERS)]))


def main():
    gil = sys._is_gil_enabled() if hasattr(sys, "_is_gil_enabled") else True
    print(f"Ядер: {len(os.sched_getaffinity(0))}  Python {sys.version.split()[0]}  "
          f"GIL: {'включён' if gil else 'выключен'}  повторов: {REPEATS}")
    print(f"{'Способ':<26}{'прогоны, с':<20}{'медиана, с':>10}  сумма")
    methods = [("1 поток", one_thread),
               ("4 потока (threading)", with_threads),
               ("4 процесса (multiproc.)", with_processes)]
    one_thread()  # прогрев: файл попадает в кэш ОС, память выделена; не измеряется
    for name, fn in methods:
        times = []
        for _ in range(REPEATS):
            t0 = time.perf_counter()
            total = fn()
            times.append(time.perf_counter() - t0)
        runs = " ".join(f"{t:.2f}" for t in times)
        print(f"{name:<26}{runs:<20}{statistics.median(times):>10.2f}  {total}", flush=True)


if __name__ == "__main__":
    main()