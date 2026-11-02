"""Validate and combine the four language CSVs and their checksums."""
import csv
import math
from pathlib import Path


LANGUAGES = ("cpp", "go", "python", "java")
EXPECTED_COLUMNS = ["language", "N", "repetition", "time_seconds"]
expected_sizes = {int(size) for size in snakemake.params.sizes}
expected_repetitions = int(snakemake.params.repetitions)
all_rows = []
checksum_lines = []

for language, csv_file, checksum_file in zip(
    LANGUAGES, snakemake.input.csvs, snakemake.input.checksums
):
    with open(csv_file, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != EXPECTED_COLUMNS:
            raise ValueError(f"{csv_file}: columnas inesperadas {reader.fieldnames}")
        language_rows = list(reader)

    counts = {size: 0 for size in expected_sizes}
    repetitions_by_size = {size: set() for size in expected_sizes}
    for row in language_rows:
        size = int(row["N"])
        repetition = int(row["repetition"])
        duration = float(row["time_seconds"])
        if (
            row["language"] != language
            or size not in expected_sizes
            or repetition < 1
            or repetition > expected_repetitions
            or not math.isfinite(duration)
            or duration <= 0
        ):
            raise ValueError(f"{csv_file}: fila inválida {row}")
        counts[size] += 1
        repetitions_by_size[size].add(repetition)

    for size in expected_sizes:
        expected = set(range(1, expected_repetitions + 1))
        if counts[size] != expected_repetitions or repetitions_by_size[size] != expected:
            raise ValueError(
                f"{csv_file}: N={size} debe tener una vez cada repetición "
                f"de 1 a {expected_repetitions}"
            )
    all_rows.extend(language_rows)

    lines = Path(checksum_file).read_text(encoding="utf-8").splitlines()
    expected_prefix = f"CHECKSUM,{language},"
    if len(lines) != len(expected_sizes) or any(
        not line.startswith(expected_prefix) for line in lines
    ):
        raise ValueError(f"{checksum_file}: checksums faltantes o inválidos")
    checksum_lines.extend(lines)

benchmark_path = Path(str(snakemake.output.benchmark))
benchmark_path.parent.mkdir(parents=True, exist_ok=True)
with benchmark_path.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=EXPECTED_COLUMNS)
    writer.writeheader()
    writer.writerows(all_rows)

Path(str(snakemake.output.checksums)).write_text(
    "\n".join(checksum_lines) + "\n", encoding="utf-8"
)
