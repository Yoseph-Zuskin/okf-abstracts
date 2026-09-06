"""Shared test helpers: load repo scripts without packaging."""

import importlib.util
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def load_module(name):
    """Import okf-abstracts/scripts/<name>.py as a module."""
    spec = importlib.util.spec_from_file_location(name, REPO / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
