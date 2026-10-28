#!/bin/sh
# Para la imagen única (Dockerfile.all): elige el lenguaje a ejecutar.
# Uso: run_lang.sh [cpp | go | java | python | all]
set -eu
run() {
  case "$1" in
    cpp)    LANG_ID=cpp;    RUN_CMD=/app/matmul_cpp;                 VERSION_CMD="g++ --version" ;;
    go)     LANG_ID=go;     RUN_CMD=/app/matmul_go;                  VERSION_CMD="go version" ;;
    java)   LANG_ID=java;   RUN_CMD="java -cp /app/java MatMul";     VERSION_CMD="java -version" ;;
    python) LANG_ID=python; RUN_CMD="python3 /app/python/matmul.py"; VERSION_CMD="python3 --version" ;;
    *) echo "Uso: cpp | go | java | python | all" >&2; exit 1 ;;
  esac
  export LANG_ID RUN_CMD VERSION_CMD
  /app/run_container.sh
}
if [ "${1:-all}" = "all" ]; then
  for l in cpp go java python; do run "$l"; done
else
  run "$1"
fi
