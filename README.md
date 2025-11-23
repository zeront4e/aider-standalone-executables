# Aider redistributable builds

This repository builds standalone, redistributable binaries of the Aider CLI for Windows and Linux using PyInstaller, and publishes them as a GitHub release through a manually triggered workflow.

## What it does

- Installs the most recent Aider using `python -m pip install aider-install`.
- Builds single-file binaries via PyInstaller for Windows and Linux.
- Publishes the binaries as release assets under a tag like `aider-<version>-<YYYYMMDD>` (falls back to `aider-latest-<YYYYMMDD>` if version detection fails).

## Triggering a build

1. Push this repository to GitHub.
2. Go to Actions → “Build and release Aider redistributables”.
3. Click “Run workflow” to trigger a manual build. You can optionally add a tag suffix.
4. When it completes, check the newly created Release for:
    - `aider-win64.exe`
    - `aider-linux-x86_64`

## Notes

- The build uses a minimal launcher (`src/run_aider.py`) that invokes Aider’s main entry point.
- PyInstaller is invoked with `--collect-all aider` to include relevant package data; adjust the build script if your environment requires additional hidden imports or data files.
- If Aider changes its internal module structure or entry point, update `src/run_aider.py` accordingly.
