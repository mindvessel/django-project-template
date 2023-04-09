#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import shutil
import subprocess
import sys
import typing as T
import venv
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
dev_in = PROJECT_DIR / "requirements-dev.in"
base_in = PROJECT_DIR / "requirements.in"
dev_reqs = PROJECT_DIR / "requirements-dev.txt"
base_reqs = PROJECT_DIR / "requirements.txt"


def get_django_package():
    """A simple hueristic to find the main package for this Django project."""
    for item in PROJECT_DIR.iterdir():
        if not item.is_dir():
            continue
        if item.joinpath("settings.py").exists():
            # Found it
            return item.name

    # If we fall through the loop, there is no settings.py, or this file is in the
    # wrong place.
    raise Exception(
        "Unable to locate a Django settings file (searched */settings.py)."
        "This script cannot continue without a settings file."
    )


def get_python_binary_from(VENV: Path):
    for maybe in [VENV / "bin" / "python", VENV / "Scripts" / "python.exe"]:
        if maybe.exists():
            return maybe
    raise Exception(f"Unable to locate Python binary in {VENV}")


def in_virtualenv():
    """Return true if running inside a virtualenv"""
    return sys.prefix != sys.base_prefix


def create_venv(
    path: Path, prompt: T.Union[str, None] = None, clear: bool = False
) -> str:
    """
    Create a virtual env in the given path and return a pathlib.Path instance
    representing the python executable.
    """
    venv.create(str(path), clear=clear, with_pip=True, prompt=prompt)
    return get_python_binary_from(path)


def _compile(PYTHON, *args):
    cmd = [
        PYTHON,
        "-m",
        "piptools",
        "compile",
        "--resolver=backtracking",
        "-qq",
        "--allow-unsafe",
    ]
    cmd.extend(args)
    subprocess.check_call(cmd, cwd=str(PROJECT_DIR))


def _pip(PYTHON, *args):
    cmd = [PYTHON, "-m", "pip", "-q"]
    cmd.extend(args)
    subprocess.check_call(cmd, cwd=str(PROJECT_DIR))


def _sync(PYTHON, *args):
    cmd = [PYTHON, "-m", "piptools", "sync", "-q"]
    cmd.extend(args)
    subprocess.check_call(cmd, cwd=str(PROJECT_DIR))


class Commands:
    """
    This class is a container for commands that are not part of Django, but that we want
    to run occasionally. It exists here because it includes the setup command that we
    run to setup our virtualenv and bootstrap it.
    """

    @staticmethod
    def devsetup(pkg, args):
        # First, ensure we have a virtualenv and know where it is
        VENV = PROJECT_DIR / ".venv"
        if in_virtualenv():
            # Already running in the virtual env
            VENV = Path(sys.prefix)
            PYTHON = sys.executable
        elif VENV.exists():
            # venv exists but we're not running in it
            PYTHON = get_python_binary_from(VENV)
        else:
            print("Creating new virtual environment")
            PYTHON = create_venv(VENV, prompt=pkg, clear=True)

        print(f"Using virtual environment in {VENV}")

        print("Installing dependencies. May take a bit. Grab a coffee.")
        # Next, ensure pip and piptools are up to date in the venv
        _pip(PYTHON, "install", "--upgrade", "pip", "pip-tools")

        # Then, use piptools sync to install requirements
        _compile(PYTHON, "-o", str(base_reqs), str(base_in))
        _compile(PYTHON, "-o", str(dev_reqs), str(dev_in))
        _sync(PYTHON, str(dev_reqs))

        # Finally, make sure we have .env file
        # If no .env, copy example.env to .env
        dotenv = PROJECT_DIR / ".env"
        example = PROJECT_DIR / "example.env"
        if not dotenv.exists() and example.exists():
            shutil.copy(example, dotenv)

        print(
            "Setup complete. Activate your virtual environment, then update your database with:"
        )
        print("  python manage.py migrate")

    @staticmethod
    def pipsync(pkg, args):
        if not in_virtualenv():
            print("Activate your virtual environment before running this command.")
            exit(1)
        PYTHON = sys.executable
        # Ensure pip and piptools are up to date in the venv
        print("Checking for the latest pip updates.")
        _pip(PYTHON, "install", "--upgrade", "pip", "pip-tools")

        # Then, use piptools sync to install requirements
        print("Checking for requirements changes.")
        _compile(PYTHON, "-o", str(base_reqs), *args, str(base_in))
        _compile(PYTHON, "-o", str(dev_reqs), *args, str(dev_in))
        print("Updating the current virtual environment.")
        _sync(PYTHON, str(dev_reqs))

    @staticmethod
    def upgrade_requirements(pkg, args):
        Commands.pipsync(pkg, args=["--upgrade"])


def django_command():
    """Run administrative tasks."""
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    package = get_django_package()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{package}.settings")
    command = sys.argv[1]  # argv[0] is manage.py
    if hasattr(Commands, command):
        cmd = getattr(Commands, command)
        cmd(package, args=sys.argv[2:])
    else:
        django_command()
