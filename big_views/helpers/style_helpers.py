import os
import sys
from typing import Optional


def get_style_path() -> str:
    try:
        base = sys._MEIPASS  # type: ignore[attr-defined]
    except AttributeError:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, 'styles')


def get_qss_string(*filenames: str, style_path: Optional[str] = None) -> str:
    style_dir = style_path if style_path else get_style_path()
    qss_content = ''

    for filename in filenames:
        filepath_total = os.path.join(style_dir, filename)
        if not filepath_total.endswith('.qss'):
            raise ValueError('The file must have a .qss extension')

        with open(filepath_total, 'r', encoding='utf-8') as f:
            qss_content += f.read() + '\n'

    return qss_content
