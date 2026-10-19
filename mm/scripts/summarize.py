"""Estadística descriptiva por lenguaje y tamaño; escribe results/summary.md."""
import csv
import statistics as st
from collections import defaultdict

data = defaultdict(list)
for lang in ("cpp", "go", "java", "python"):
    with open(f"results/{lang}.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            data[(row["language"], int(row["N"]))].append(float(row["time_seconds"]))

lines = ["| Lenguaje | N | n | Media (s) | Mediana (s) | Desv. est. (s) | Mín (s) | Máx (s) |",
         "|---|---|---|---|---|---|---|---|"]
for (lang, n) in sorted(data, key=lambda k: (k[1], k[0])):
    v = data[(lang, n)]
    sd = st.stdev(v) if len(v) > 1 else 0.0
    lines.append(f"| {lang} | {n} | {len(v)} | {st.mean(v):.4f} | {st.median(v):.4f} | {sd:.4f} | {min(v):.4f} | {max(v):.4f} |")
text = "\n".join(lines) + "\n"
print(text)
with open("results/summary.md", "w", encoding="utf-8") as f:
    f.write(text)
