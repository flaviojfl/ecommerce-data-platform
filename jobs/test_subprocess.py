"""Teste se Python consegue spawnar subprocesso (workers do Spark fazem isso)."""
import subprocess
import sys


def main() -> None:
    print(f"Python atual: {sys.executable}")
    result = subprocess.run(
        [sys.executable, "-c", "print('hello from worker')"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    print(f"stdout: {result.stdout!r}")
    print(f"stderr: {result.stderr!r}")
    print(f"returncode: {result.returncode}")


if __name__ == "__main__":
    main()