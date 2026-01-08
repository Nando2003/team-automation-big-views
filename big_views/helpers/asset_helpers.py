import os
import sys


def get_asset_path() -> str:
    try:
        base = sys._MEIPASS  # type: ignore[attr-defined]
    except AttributeError:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, 'assets')
