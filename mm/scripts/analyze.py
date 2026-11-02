"""Run factorial ANOVA, appropriate Tukey comparisons, tables, and a plot."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
from matplotlib.patches import Patch
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd


ALPHA = float(snakemake.params.alpha)
EXPECTED_COLUMNS = ["language", "N", "repetition", "time_seconds"]
data = pd.read_csv(snakemake.input.benchmark)
if list(data.columns) != EXPECTED_COLUMNS:
    raise ValueError(f"Columnas inesperadas en benchmark.csv: {list(data.columns)}")
if data.empty or data["time_seconds"].isna().any() or (data["time_seconds"] <= 0).any():
    raise ValueError("benchmark.csv contiene datos vacíos o tiempos no positivos.")
data["N"] = data["N"].astype(int)
data["language"] = data["language"].astype(str)

results_dir = Path(str(snakemake.output[0])).resolve().parent
results_dir.mkdir(parents=True, exist_ok=True)

descriptive = (
    data.groupby(["language", "N"], observed=True)["time_seconds"]
    .agg(["count", "mean", "median", "std", "min", "max"])
    .reset_index()
)
descriptive.to_csv(snakemake.output[0], index=False, float_format="%.9g")

model = ols("time_seconds ~ C(language) * C(N)", data=data).fit()
anova = sm.stats.anova_lm(model, typ=2).rename_axis("term").reset_index()
anova = anova.rename(columns={"PR(>F)": "p_value"})
anova.to_csv(snakemake.output[1], index=False, float_format="%.9g")

interaction_term = "C(language):C(N)"
interaction = anova.loc[anova["term"] == interaction_term, "p_value"]
interaction_significant = not interaction.empty and float(interaction.iloc[0]) < ALPHA
tukey_rows = []


def add_tukey(frame, factor, scope):
    comparison = pairwise_tukeyhsd(
        endog=frame["time_seconds"],
        groups=frame[factor].astype(str),
        alpha=ALPHA,
    )
    for row in comparison.summary().data[1:]:
        tukey_rows.append(
            {
                "factor": factor,
                "scope": scope,
                "group1": row[0],
                "group2": row[1],
                "mean_difference": row[2],
                "p_adjusted": row[3],
                "lower": row[4],
                "upper": row[5],
                "reject": row[6],
            }
        )


if interaction_significant:
    for size, subset in data.groupby("N", sort=True):
        add_tukey(subset, "language", f"N={size}")
    for language, subset in data.groupby("language", sort=True):
        add_tukey(subset, "N", f"language={language}")
else:
    for factor, term in (
        ("language", "C(language)"),
        ("N", "C(N)"),
    ):
        p_value = anova.loc[anova["term"] == term, "p_value"]
        if not p_value.empty and float(p_value.iloc[0]) < ALPHA:
            add_tukey(data, factor, "all observations")

tukey_columns = [
    "factor",
    "scope",
    "group1",
    "group2",
    "mean_difference",
    "p_adjusted",
    "lower",
    "upper",
    "reject",
]
tukey = pd.DataFrame(tukey_rows, columns=tukey_columns)
tukey.to_csv(snakemake.output[2], index=False, float_format="%.9g")

with open(snakemake.output[3], "w", encoding="utf-8") as report:
    report.write("# Análisis estadístico del benchmark\n\n")
    report.write(f"ANOVA de dos factores con interacción; α = {ALPHA:g}.\n\n")
    report.write("## Estadística descriptiva\n\n")
    report.write("| Lenguaje | N | n | Media (s) | Mediana (s) | Desv. est. (s) | Mín. (s) | Máx. (s) |\n")
    report.write("|---|---:|---:|---:|---:|---:|---:|---:|\n")
    for row in descriptive.to_dict(orient="records"):
        report.write(
            f"| {row['language']} | {row['N']} | {row['count']} | {row['mean']:.6g} | "
            f"{row['median']:.6g} | {row['std']:.6g} | {row['min']:.6g} | "
            f"{row['max']:.6g} |\n"
        )

    report.write("\n## ANOVA tipo II\n\n")
    report.write("| Factor | Suma de cuadrados | gl | F | p-valor |\n")
    report.write("|---|---:|---:|---:|---:|\n")
    for row in anova.to_dict(orient="records"):
        report.write(
            f"| {row['term']} | {row['sum_sq']:.6g} | {row['df']:g} | "
            f"{row['F']:.6g} | {row['p_value']:.6g} |\n"
        )

    report.write("\n## Comparaciones post-hoc (Tukey HSD)\n\n")
    if tukey.empty:
        report.write(
            "No se realizaron comparaciones: no se detectó un efecto significativo "
            "que las justificara.\n"
        )
    else:
        report.write(
            "Con interacción significativa se comparó lenguaje dentro de cada N y "
            "N dentro de cada lenguaje. Sin interacción significativa, se compararon "
            "los niveles de cada efecto principal significativo.\n\n"
        )
        report.write("| Factor | Estrato | Grupo 1 | Grupo 2 | Diferencia media | p ajustado | Rechaza H0 |\n")
        report.write("|---|---|---|---|---:|---:|---|\n")
        for row in tukey.itertuples(index=False):
            report.write(
                f"| {row.factor} | {row.scope} | {row.group1} | {row.group2} | "
                f"{row.mean_difference:.6g} | {row.p_adjusted:.6g} | {row.reject} |\n"
            )

languages = sorted(data["language"].unique())
sizes = sorted(data["N"].unique())
palette = dict(zip(languages, plt.get_cmap("tab10").colors))
fig, ax = plt.subplots(figsize=(11, 6))
positions = []
box_data = []
colors = []
labels = []
position = 1
for size in sizes:
    for language in languages:
        values = data.loc[
            (data["N"] == size) & (data["language"] == language), "time_seconds"
        ].to_numpy()
        if len(values):
            positions.append(position)
            box_data.append(values)
            colors.append(palette[language])
            labels.append(language)
            position += 1
    position += 1

boxes = ax.boxplot(
    box_data,
    positions=positions,
    patch_artist=True,
    showfliers=True,
    widths=0.7,
)
for box, color in zip(boxes["boxes"], colors):
    box.set_facecolor(color)
    box.set_alpha(0.75)
ax.set_xticks(
    [
        sum(positions[index : index + len(languages)]) / len(languages)
        for index in range(0, len(positions), len(languages))
    ],
    [str(size) for size in sizes],
)
ax.set_xlabel("Tamaño de matriz (N)")
ax.set_ylabel("Tiempo de ejecución (s; escala logarítmica)")
ax.set_yscale("log")
ax.set_title("Tiempo de multiplicación por lenguaje y tamaño de matriz")
ax.grid(axis="y", which="both", alpha=0.25)
ax.legend(
    handles=[Patch(facecolor=palette[language], label=language) for language in languages],
    title="Lenguaje",
)
fig.tight_layout()
fig.savefig(snakemake.output[4], dpi=160)
plt.close(fig)
