import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv"

REQUIREMENTS = [
    "PyQt6",
    "PyQt6-WebEngine",
    "python-lsp-jsonrpc",
    "python-lsp-server",
    "RapidFuzz",
    "screeninfo",
    "ujson",
]


def run(cmd):
    print(f"\n>>> {' '.join(map(str, cmd))}")
    subprocess.check_call(cmd)


def create_venv():
    if VENV_DIR.exists():
        print("✓ Virtual environment already exists")
        return

    print("Creating virtual environment...")
    run([sys.executable, "-m", "venv", str(VENV_DIR)])


def get_pip():
    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / "pip.exe"
    return VENV_DIR / "bin" / "pip"


def install_python_packages():
    pip = str(get_pip())

    print("\nInstalling Python packages...")

    run([pip, "install", "--upgrade", "pip"])

    for package in REQUIREMENTS:
        print(f"\nInstalling {package}")
        run([pip, "install", package])


def install_font():
    font_file = ROOT / "Assets" / "Fonts" / "JetBrainsMono.ttf"

    if not font_file.exists():
        print("\nJetBrains Mono font not found:")
        print(font_file)
        return

    system = platform.system()

    try:
        if system == "Linux":
            font_dir = Path.home() / ".local/share/fonts"
            font_dir.mkdir(parents=True, exist_ok=True)

            target = font_dir / font_file.name
            shutil.copy2(font_file, target)

            subprocess.run(["fc-cache", "-fv"])

            print("✓ Font installed")

        elif system == "Darwin":
            font_dir = Path.home() / "Library/Fonts"
            font_dir.mkdir(parents=True, exist_ok=True)

            target = font_dir / font_file.name
            shutil.copy2(font_file, target)

            print("✓ Font installed")

        elif system == "Windows":
            windows_fonts = Path(r"C:\Windows\Fonts")
            target = windows_fonts / font_file.name

            shutil.copy2(font_file, target)

            print(
                "✓ Font copied to Windows Fonts directory "
                "(may require Administrator privileges)"
            )

    except Exception as e:
        print(f"Font installation failed: {e}")


def install_clangd():
    answer = input("\nInstall clangd? [Y/n]: ").strip().lower()

    if answer == "n":
        return

    system = platform.system()

    try:
        if system == "Linux":

            if shutil.which("apt"):
                run(["sudo", "apt", "install", "-y", "clangd"])

            elif shutil.which("dnf"):
                run(["sudo", "dnf", "install", "-y", "clang-tools-extra"])

            elif shutil.which("pacman"):
                run(["sudo", "pacman", "-S", "--noconfirm", "clang"])

            else:
                print(
                    "Unsupported Linux package manager.\n"
                    "Please install clangd manually."
                )

        elif system == "Darwin":

            if shutil.which("brew"):
                run(["brew", "install", "llvm"])
            else:
                print("Homebrew not found. Install LLVM manually.")

        elif system == "Windows":

            if shutil.which("winget"):
                run(["winget", "install", "LLVM.LLVM"])
            else:
                print(
                    "\nwinget not found.\n"
                    "Download LLVM manually:\n"
                    "https://github.com/llvm/llvm-project/releases"
                )

    except Exception as e:
        print(f"clangd installation failed: {e}")


def main():
    print("=" * 50)
    print("CodeDock Installer")
    print("=" * 50)

    create_venv()
    install_python_packages()
    install_font()
    install_clangd()

    print("\n✓ Installation completed")

    if platform.system() == "Windows":
        activate = ".venv\\Scripts\\activate"
    else:
        activate = "source .venv/bin/activate"

    print("\nActivate environment:")
    print(activate)


if __name__ == "__main__":
    main()
