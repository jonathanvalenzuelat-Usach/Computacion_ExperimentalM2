"""Imprime el orden aleatorizado (con semilla) de los 12 bloques lenguaje:N."""
import random
import sys

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 42
sizes = sys.argv[2:] or ["500", "1000", "1500"]
blocks = [f"{lang}:{n}" for lang in ("cpp", "go", "java", "python") for n in sizes]
random.Random(seed).shuffle(blocks)
print("\n".join(blocks))
