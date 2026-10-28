"""Multiplicación naive de matrices NxN (Python puro, sin NumPy).

Uso: python3 matmul.py <N> <repeticiones> <semilla> <archivo_csv> [repeticion_inicial]

El argumento opcional permite reanudar un bloque interrumpido (por defecto 1).
"""
import os
import sys
import time


def make_matrix(count, state):
    """Generador congruencial lineal de 32 bits, idéntico en los cuatro lenguajes."""
    m = [0.0] * count
    for idx in range(count):
        state = (state * 1664525 + 1013904223) & 0xFFFFFFFF
        m[idx] = (state >> 8) / 16777216.0
    return m, state


def multiply(a, b, c, n):
    """Algoritmo naive: triple bucle i-j-k, matrices en lista plana por filas."""
    for i in range(n):
        for j in range(n):
            s = 0.0
            for k in range(n):
                s += a[i * n + k] * b[k * n + j]
            c[i * n + j] = s


def checksum(c):
    s = 0.0
    for x in c:
        s += x
    return s


def main():
    if len(sys.argv) not in (5, 6):
        sys.exit("Uso: python3 matmul.py <N> <repeticiones> <semilla> <archivo_csv> [repeticion_inicial]")
    start = int(sys.argv[5]) if len(sys.argv) == 6 else 1
    n = int(sys.argv[1])
    reps = int(sys.argv[2])
    state = int(sys.argv[3]) & 0xFFFFFFFF
    out = sys.argv[4]

    # Creación de matrices: FUERA de la medición.
    a, state = make_matrix(n * n, state)
    b, state = make_matrix(n * n, state)
    c = [0.0] * (n * n)

    header = (not os.path.exists(out)) or os.path.getsize(out) == 0
    ref = 0.0
    with open(out, "a", encoding="utf-8", newline="") as f:
        if header:
            f.write("language,N,repetition,time_seconds\n")
        for r in range(start, reps + 1):
            t0 = time.perf_counter()
            multiply(a, b, c, n)
            secs = time.perf_counter() - t0

            cs = checksum(c)
            if r == start:
                ref = cs
            elif cs != ref:
                sys.exit("Checksum inconsistente entre repeticiones")

            f.write(f"python,{n},{r},{secs:.9f}\n")
            f.flush()
            print(f"[python N={n} rep {r}/{reps}] {secs:.6f} s", file=sys.stderr)
    print(f"CHECKSUM,python,{n},{ref!r}")


if __name__ == "__main__":
    main()
