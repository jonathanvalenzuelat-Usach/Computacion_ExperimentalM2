#!/usr/bin/env bash
# Compila y ejecuta el experimento completo (Linux / macOS / WSL).
# Variables opcionales: SEED (42), REPS (10), SIZES ("500 1000 1500"), LANGS_ONLY ("" = todos)
set -euo pipefail
cd "$(dirname "$0")/.."

SEED="${SEED:-42}"
REPS="${REPS:-10}"
SIZES="${SIZES:-500 1000 1500}"
OUT=results

mkdir -p "$OUT" bin/java

echo "== Compilando =="
g++ -O2 -std=c++17 -ffp-contract=off src/cpp/matmul.cpp -o bin/matmul_cpp
(cd src/go && go build -o ../../bin/matmul_go .)
javac -d bin/java src/java/MatMul.java

echo "== Registrando entorno =="
python3 scripts/record_env.py

rm -f "$OUT"/cpp.csv "$OUT"/go.csv "$OUT"/java.csv "$OUT"/python.csv "$OUT"/checksums.txt

echo "== Ejecutando (orden aleatorizado, semilla $SEED) =="
# shellcheck disable=SC2086
python3 scripts/gen_order.py "$SEED" $SIZES | while IFS=: read -r lang n; do
  if [[ -n "${LANGS_ONLY:-}" && " $LANGS_ONLY " != *" $lang "* ]]; then continue; fi
  echo ">> $lang N=$n"
  case "$lang" in
    cpp)    bin/matmul_cpp "$n" "$REPS" "$SEED" "$OUT/cpp.csv" >> "$OUT/checksums.txt" ;;
    go)     bin/matmul_go  "$n" "$REPS" "$SEED" "$OUT/go.csv"  >> "$OUT/checksums.txt" ;;
    java)   java -cp bin/java MatMul "$n" "$REPS" "$SEED" "$OUT/java.csv" >> "$OUT/checksums.txt" ;;
    python) python3 src/python/matmul.py "$n" "$REPS" "$SEED" "$OUT/python.csv" >> "$OUT/checksums.txt" ;;
  esac
done

echo "== Verificación y resumen =="
python3 scripts/verify.py "${SIZES// /,}" "$REPS"
python3 scripts/summarize.py
