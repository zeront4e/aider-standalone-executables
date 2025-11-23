"""
Minimal launcher for Aider CLI, suitable for PyInstaller onefile builds.
This defers to the installed Aider package entry point.
"""

def main():
    # Import inside function to reduce import-time failures during analysis
    from aider.main import main as aider_main
    aider_main()

if __name__ == "__main__":
    main()
