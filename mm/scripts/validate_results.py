"""Run the project's CSV and cross-language checksum validator."""
from pathlib import Path
import subprocess
import sys


artifact_root = Path(snakemake.scriptdir).parent
validator = artifact_root / "scripts" / "verify.py"
subprocess.run(
    [
        sys.executable,
        str(validator),
        snakemake.params.sizes,
        str(snakemake.params.repetitions),
    ],
    cwd=artifact_root,
    check=True,
)
