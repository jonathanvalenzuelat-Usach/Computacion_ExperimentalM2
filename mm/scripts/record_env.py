"""Registra las características del entorno de ejecución en results/environment.{json,md}."""
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone


def run(cmd):
    """Ejecuta un comando y devuelve la primera línea de su salida (stdout o stderr)."""
    if shutil.which(cmd[0]) is None:
        return "no disponible"
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        out = (p.stdout or p.stderr).strip().splitlines()
        return out[0] if out else "sin salida"
    except Exception as e:  # noqa: BLE001
        return f"error: {e}"


def cpu_model():
    system = platform.system()
    if system == "Linux":
        try:
            with open("/proc/cpuinfo", encoding="utf-8") as f:
                for line in f:
                    if line.lower().startswith(("model name", "hardware", "cpu model")):
                        return line.split(":", 1)[1].strip()
        except OSError:
            pass
    elif system == "Darwin":
        return run(["sysctl", "-n", "machdep.cpu.brand_string"])
    return platform.processor() or "desconocido"


def ram_gib():
    system = platform.system()
    try:
        if system == "Linux":
            with open("/proc/meminfo", encoding="utf-8") as f:
                kb = int(f.readline().split()[1])
            return round(kb / 1024 / 1024, 2)
        if system == "Darwin":
            return round(int(run(["sysctl", "-n", "hw.memsize"])) / 1024**3, 2)
    except Exception:  # noqa: BLE001
        pass
    return None


def os_name():
    try:
        with open("/etc/os-release", encoding="utf-8") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    return line.split("=", 1)[1].strip().strip('"')
    except OSError:
        pass
    return f"{platform.system()} {platform.release()}"


def governor():
    path = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
    try:
        with open(path, encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return "no disponible"


env = {
    "fecha_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "procesador": cpu_model(),
    "nucleos_logicos": os.cpu_count(),
    "ram_gib": ram_gib(),
    "sistema_operativo": os_name(),
    "kernel": platform.release(),
    "arquitectura": platform.machine(),
    "gobernador_cpu": governor(),
    "versiones": {
        "g++": run(["g++", "--version"]),
        "go": run(["go", "version"]),
        "javac": run(["javac", "-version"]),
        "java": run(["java", "-version"]),
        "python": f"Python {sys.version.split()[0]}",
    },
    "banderas_compilacion": {
        "cpp": "g++ -O2 -std=c++17 -ffp-contract=off",
        "go": "go build (valores por defecto)",
        "java": "javac / java (valores por defecto)",
        "python": "CPython sin extensiones, sin NumPy",
    },
}

os.makedirs("results", exist_ok=True)
with open("results/environment.json", "w", encoding="utf-8") as f:
    json.dump(env, f, indent=2, ensure_ascii=False)

lines = ["# Entorno de ejecución", "", "| Característica | Valor |", "|---|---|"]
for k in ("fecha_utc", "procesador", "nucleos_logicos", "ram_gib", "sistema_operativo", "kernel",
          "arquitectura", "gobernador_cpu"):
    lines.append(f"| {k} | {env[k]} |")
for k, v in env["versiones"].items():
    lines.append(f"| versión {k} | {v} |")
for k, v in env["banderas_compilacion"].items():
    lines.append(f"| compilación {k} | {v} |")
with open("results/environment.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("Entorno registrado en results/environment.json y results/environment.md")
