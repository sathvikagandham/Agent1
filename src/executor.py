"""Run a snippet of Python in an isolated subprocess and capture the result."""

import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from src.config import EXEC_TIMEOUT

@dataclass
class ExecResult:
    """Outcome of running one code snippet."""
    ok: bool      # True if process exited 0 with no exception
    stdout: str   # Whatever the snippet printed
    stderr: str   # Traceback/error text if it failed

def run_code(code: str) -> ExecResult:
    """Execute code in a subprocess and return what happened."""
    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "candidate.py"
        script.write_text(code, encoding="utf-8")

        try:
            proc = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True,
                text=True,
                timeout=EXEC_TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            return ExecResult(
                ok=False,
                stdout="",
                stderr=f"Execution timed out after {EXEC_TIMEOUT}s (possible infinite loop).",
            )

        return ExecResult(
            ok=proc.returncode == 0,
            stdout=proc.stdout.strip(),
            stderr=proc.stderr.strip(),
        )