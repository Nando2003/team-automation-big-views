from dataclasses import dataclass, field

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from big_views.helpers.style_helpers import get_qss_string
from big_views.types import StepSpec


@dataclass(frozen=True)
class FileStepSpec(StepSpec):
    dialog_title: str = field(default='Selecionar arquivo')
    file_filter: str = field(default='All Files (*)')


class FileStepWidget(QWidget):
    def __init__(self, spec: FileStepSpec):
        super().__init__()
        self.spec = spec

        qss_string = spec.qss_string or get_qss_string('file_widget.qss')
        self.setStyleSheet(qss_string)

        title = QLabel(spec.title)
        title.setProperty('role', 'step_title')
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.input = QLineEdit()
        self.input.setProperty('role', 'file_input')
        self.input.setReadOnly(True)
        self.input.setPlaceholderText('Nenhum arquivo selecionado')

        btn = QPushButton('Procurar')
        btn.setProperty('role', 'browse_button')
        btn.clicked.connect(self.pick)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)
        row.addWidget(self.input, 1)
        row.addWidget(btn)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addLayout(row)

        wrapper = QWidget()
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.addStretch()
        wrapper_layout.addWidget(content)
        wrapper_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # só horizontal
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setWidget(wrapper)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(title)
        layout.addItem(QSpacerItem(0, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        layout.addWidget(scroll, 1)

    def pick(self):
        path, _ = QFileDialog.getOpenFileName(
            self, self.spec.dialog_title, filter=self.spec.file_filter
        )
        if path:
            self.input.setText(path)

    def value(self) -> str:
        return self.input.text().strip()
