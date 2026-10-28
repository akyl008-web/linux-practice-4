#!/usr/bin/env python3
"""ПР-4. Генерирует numbers.txt — 10 000 000 целых чисел, по одному в строке.
Результат детерминирован (seed = 2026). Запуск: python3 gen_numbers.py"""
import random

N = 10_000_000
CHUNK = 100_000

rng = random.Random(2026)
with open("numbers.txt", "w") as f:
    for _ in range(N // CHUNK):
        f.write("\n".join(str(rng.randint(-1_000_000, 1_000_000)) for _ in range(CHUNK)))
        f.write("\n")
print(f"Создан numbers.txt: {N} чисел")