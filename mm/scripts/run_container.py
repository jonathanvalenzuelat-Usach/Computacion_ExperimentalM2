"""Run one prebuilt benchmark image and write its CSV and checksums."""
from pathlib import Path
import subprocess


language = snakemake.wildcards.language
image = snakemake.params.image
results_dir = Path(str(snakemake.output.csv)).resolve().parent
csv_path = Path(str(snakemake.output.csv)).resolve()
checksums_path = Path(str(snakemake.output.checksums)).resolve()
log_path = Path(str(snakemake.log[0])).resolve()

results_dir.mkdir(parents=True, exist_ok=True)
log_path.parent.mkdir(parents=True, exist_ok=True)
for path in (csv_path, checksums_path):
    path.unlink(missing_ok=True)

command = [
    "docker",
    "run",
    "--rm",
    "--pull=never",
    "-e",
    f"SIZES={snakemake.params.sizes}",
    "-e",
    f"REPS={snakemake.params.repetitions}",
    "-e",
    f"SEED={snakemake.params.seed}",
    "-e",
    f"CHECKSUM_FILE=/app/results/checksums_{language}.txt",
    "--mount",
    f"type=bind,source={results_dir},target=/app/results",
    image,
]
image_check = subprocess.run(
    ["docker", "image", "inspect", image],
    capture_output=True,
    text=True,
)
if image_check.returncode:
    details = (image_check.stderr or image_check.stdout).strip()
    raise RuntimeError(
        f"No se puede usar la imagen local '{image}'. Comprueba que Docker "
        "Desktop esté iniciado en modo Linux y construye la imagen desde la "
        f"carpeta mm con: docker build --pull -f docker/Dockerfile.{language} "
        f"-t {image} .\nDetalle de Docker: {details}"
    )

with log_path.open("w", encoding="utf-8") as log:
    subprocess.run(command, check=True, stdout=log, stderr=subprocess.STDOUT)

if not csv_path.is_file() or not checksums_path.is_file():
    raise RuntimeError(
        f"La imagen {image} no generó los resultados esperados para {language}."
    )
