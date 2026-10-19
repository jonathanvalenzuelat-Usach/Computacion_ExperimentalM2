"""Valida los CSV (estructura y conteo) y compara los checksums entre lenguajes."""
import csv
import sys
from collections import defaultdict

LANGS = ["cpp", "go", "java", "python"]
EXPECTED_COLS = ["language", "N", "repetition", "time_seconds"]
SIZES = [int(x) for x in (sys.argv[1].split(",") if len(sys.argv) > 1 else ["500", "1000", "1500"])]
REPS = int(sys.argv[2]) if len(sys.argv) > 2 else 10
ok = True

print("== Validación de CSV ==")
for lang in LANGS:
    path = f"results/{lang}.csv"
    try:
        with open(path, newline="", encoding="utf-8") as f:
            rd = csv.DictReader(f)
            if rd.fieldnames != EXPECTED_COLS:
                print(f"[ERROR] {path}: columnas {rd.fieldnames}")
                ok = False
                continue
            count = defaultdict(int)
            for row in rd:
                if row["language"] != lang or float(row["time_seconds"]) <= 0:
                    print(f"[ERROR] {path}: fila inválida {row}")
                    ok = False
                count[int(row["N"])] += 1
    except FileNotFoundError:
        print(f"[ERROR] falta {path}")
        ok = False
        continue
    for n in SIZES:
        if count.get(n, 0) != REPS:
            print(f"[ERROR] {path}: N={n} tiene {count.get(n, 0)} filas (se esperaban {REPS})")
            ok = False
    if ok:
        print(f"[OK] {path}")

print("\n== Comparación de checksums ==")
vals = defaultdict(dict)
try:
    with open("results/checksums.txt", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 4 and parts[0] == "CHECKSUM":
                vals[int(parts[2])][parts[1]] = float(parts[3])
except FileNotFoundError:
    print("[ERROR] falta results/checksums.txt")
    ok = False

for n in sorted(vals):
    ref = vals[n].get("cpp")
    if ref is None or set(vals[n]) != set(LANGS):
        print(f"[ERROR] N={n}: checksums incompletos ({sorted(vals[n])})")
        ok = False
        continue
    exact = all(vals[n][l] == ref for l in LANGS)
    close = all(abs(vals[n][l] - ref) <= 1e-9 * abs(ref) for l in LANGS)
    estado = "idénticos" if exact else ("coinciden (tol. 1e-9)" if close else "NO COINCIDEN")
    print(f"N={n}: {estado}  (referencia C++ = {ref!r})")
    if not close:
        ok = False

print("\nRESULTADO:", "TODO OK" if ok else "HAY ERRORES")
sys.exit(0 if ok else 1)
