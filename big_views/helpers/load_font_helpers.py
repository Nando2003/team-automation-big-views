import os

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication

from big_views.helpers.asset_helpers import get_asset_path


def load_fonts(*font_file: str, app: QApplication, font_name: str) -> None:
    for fname in font_file:
        path = os.path.join(get_asset_path(), 'fonts', fname)
        fid = QFontDatabase.addApplicationFont(path)

        if fid >= 0:
            QFontDatabase.applicationFontFamilies(fid)

    app.setFont(QFont(font_name))
