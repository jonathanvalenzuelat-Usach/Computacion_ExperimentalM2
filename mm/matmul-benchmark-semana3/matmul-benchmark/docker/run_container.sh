#!/bin/sh
# Ejecuta el experimento de UN lenguaje dentro del contenedor.
# Variables: LANG_ID, RUN_CMD, VERSION_CMD (definidas en la imagen) y
# SIZES, REPS, SEED (opcionales).
set -eu
SIZES="${SIZES:-500 1000 1500}"
REPS="${REPS:-10}"
SEED="${SEED:-42}"
OUT=/app/results
mkdir -p "$OUT"
rm -f "$OUT/$LANG_ID.csv"

{
  echo "language: $LANG_ID"
  echo "version: $(sh -c "$VERSION_CMD 2>&1" | head -n 1)"
  echo "so: $(grep PRETTY_NAME /etc/os-release | cut -d= -f2)"
  echo "kernel: $(uname -r)"
  echo "arquitectura: $(uname -m)"
  echo "nucleos_visibles: $(nproc)"
  echo "ram_total: $(grep MemTotal /proc/meminfo | awk '{print $2, $3}')"
} > "$OUT/environment_$LANG_ID.txt"

for n in $SIZES; do
  echo ">> $LANG_ID N=$n" >&2
  $RUN_CMD "$n" "$REPS" "$SEED" "$OUT/$LANG_ID.csv" >> "$OUT/checksums.txt"
done
