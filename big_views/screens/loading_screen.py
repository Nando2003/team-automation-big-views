import os

from PySide6.QtCore import QSize, Qt, Slot
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from big_views.helpers.asset_helpers import get_asset_path
from big_views.helpers.style_helpers import get_qss_string


class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(get_qss_string('loading_screen.qss'))

        gif_label = QLabel(self)
        gif_label.setProperty('role', 'loading_icon')
        movie = QMovie(os.path.join(get_asset_path(), 'loading.gif'))
        movie.setScaledSize(QSize(64, 64))
        gif_label.setMovie(movie)
        movie.start()

        title_lbl = QLabel('Processo em andamento', self)
        title_lbl.setProperty('role', 'loading_title')

        header = QHBoxLayout()
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.addWidget(gif_label)
        header.addSpacing(10)
        header.addWidget(title_lbl)

        self.status_lbl = QLabel('', self)
        self.status_lbl.setProperty('role', 'loading_status')

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setProperty('role', 'loading_progress')

        progress_col = QVBoxLayout()
        progress_col.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_col.setSpacing(6)
        progress_col.addWidget(self.status_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        progress_col.addWidget(self.progress_bar)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 24, 0, 0)
        layout.addLayout(header)
        layout.addSpacerItem(
            QSpacerItem(0, 32, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        )
        layout.addLayout(progress_col)
        layout.addStretch()

    @Slot(int)
    def set_progress(self, value: int):
        self.progress_bar.setValue(max(0, min(value, 100)))

    @Slot(str)
    def set_status(self, text: str):
        self.status_lbl.setText(text)
