from __future__ import annotations

from pathlib import Path


def get_hook_dirs():
    return [str(Path(__file__).resolve().parent)]
