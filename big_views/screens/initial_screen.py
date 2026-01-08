import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from big_views.helpers.asset_helpers import get_asset_path
from big_views.helpers.style_helpers import get_qss_string


class InitialScreen(QWidget):
    def __init__(self, flow_name: str, on_start=None):
        super().__init__()
        self.setStyleSheet(get_qss_string('initial_screen.qss'))

        icon_label = QLabel()
        icon_label.setProperty('role', 'initial_icon')
        icon_pixmap = QIcon(os.path.join(get_asset_path(), 'icon_tim.png')).pixmap(96, 96)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(flow_name)
        title_label.setProperty('role', 'initial_title')
        title_label.setWordWrap(True)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(10)
        row.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        row.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignVCenter)

        row_container = QWidget()
        row_container.setLayout(row)

        start_btn = QPushButton('Iniciar')
        start_btn.setProperty('role', 'initial_button')
        start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        if on_start:
            start_btn.clicked.connect(on_start)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addStretch()  # espaço acima
        main_layout.addWidget(row_container, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addSpacing(24)  # espaço entre texto e botão
        main_layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()
