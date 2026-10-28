#!/usr/bin/env python3
"""ПР-4, вариант B, задание 4. Потоки разделяют память, процессы — нет."""
import multiprocessing
import threading

data = []


def add(who):
    data.append(who)
    print(f"  внутри ({who}): data = {data}", flush=True)


if __name__ == "__main__":
    print(f"Способ запуска процессов: {multiprocessing.get_start_method()}")
    print(f"Родитель до:             data = {data}")

    t = threading.Thread(target=add, args=("поток",))
    t.start()
    t.join()
    print(f"Родитель после потока:   data = {data}")

    p = multiprocessing.Process(target=add, args=("процесс",))
    p.start()
    p.join()
    print(f"Родитель после процесса: data = {data}")