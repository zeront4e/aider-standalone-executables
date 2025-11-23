import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
DIST = PROJECT_ROOT / "dist"

LAUNCHER = SRC / "run_aider.py"

def run(cmd, check=True):
    print(f"+ Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=check)

def main():
    DIST.mkdir(exist_ok=True)
    # Ensure aider is installed via aider-install
    run([sys.executable, "-m", "pip", "install", "--upgrade", "aider-install"])

    # Optional: print aider version
    try:
        import importlib.metadata as m
        ver = m.version("aider")
        print(f"Aider version detected: {ver}")
    except Exception as e:
        print(f"Could not detect Aider version: {e}")

    # Build with PyInstaller
    target_name = "aider"
    system = platform.system().lower()

    if system == "windows":
        artifact_name = "aider-win64.exe"
    elif system == "linux":
        artifact_name = "aider-linux-x86_64"
    elif system == "darwin":
        # Build both Intel and ARM variants
        artifact_name_x86 = "aider-macos-x86_64"
        artifact_name_arm = "aider-macos-arm64"

        # Default build (runner arch, usually x86_64)
        run([
            sys.executable, "-m", "PyInstaller",
            "--name", "aider",
            "--onefile",
            "--noconfirm",
            "--console",
            "--collect-all", "aider",
            "--hidden-import", "backports",
            "--hidden-import", "backports.cached_property",
            str(LAUNCHER),
        ])
        built = PROJECT_ROOT / "dist" / "aider"
        shutil.move(str(built), str(DIST / artifact_name_x86))

        # Optional: cross‑compile for arm64 if Python supports it
        # Requires universal2 Python or arm64 environment
        try:
            run([
                sys.executable, "-m", "PyInstaller",
                "--name", "aider",
                "--onefile",
                "--noconfirm",
                "--console",
                "--collect-all", "aider",
                "--target-arch", "arm64",   # 👈 key flag
                str(LAUNCHER),
            ])
            built_arm = PROJECT_ROOT / "dist" / "aider"
            shutil.move(str(built_arm), str(DIST / artifact_name_arm))
        except Exception as e:
            print("Skipping arm64 build (requires arm64 Python):", e)
    else:
        raise RuntimeError(f"Unsupported OS for build: {system}")

    # Clean previous build dirs
    for p in ["build", "dist"]:
        p = PROJECT_ROOT / p
        if p.exists():
            shutil.rmtree(p)

    # PyInstaller command
    # --collect-all aider attempts to include any package data/hooks needed by Aider.
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", target_name,
        "--onefile",
        "--noconfirm",
        "--console",
        "--collect-all", "aider",
        str(LAUNCHER),
    ]
    run(cmd)

    # Move/rename artifact
    built = PROJECT_ROOT / "dist" / (f"{target_name}.exe" if system == "windows" else target_name)
    if not built.exists():
        raise FileNotFoundError(f"Expected build artifact not found: {built}")

    final = DIST / artifact_name
    if final.exists():
        final.unlink()
    shutil.move(str(built), str(final))
    # Ensure executable bit on *nix
    if system != "windows":
        final.chmod(0o755)

    print(f"Build complete: {final}")

if __name__ == "__main__":
    main()
