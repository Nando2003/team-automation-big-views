import sys
from logging import Logger
from typing import Optional

from PySide6.QtWidgets import QApplication

from big_views.helpers.load_font_helpers import load_fonts
from big_views.manager import FlowManager
from big_views.types import FlowSpec


def start(
    flow_spec: FlowSpec,
    logger: Optional[Logger] = None,
    *,
    window_title: Optional[str] = None,
    size: tuple[int, int] = (720, 300),
):
    window_title = flow_spec.name if window_title is None else window_title

    width = size[0]
    height = size[1]

    app = QApplication(sys.argv)

    load_fonts(
        'Roboto-Regular.ttf',
        'Roboto-Bold.ttf',
        'Roboto-Light.ttf',
        'Roboto-Italic.ttf',
        'Roboto-SemiBold.ttf',
        app=app,
        font_name='Roboto',
    )

    manager = FlowManager(flow_spec, logger=logger)
    manager.setWindowTitle(window_title)
    manager.resize(width, height)
    manager.show()

    sys.exit(app.exec())
