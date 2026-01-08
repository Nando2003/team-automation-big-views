from dataclasses import dataclass, field

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from big_views.helpers.style_helpers import get_qss_string
from big_views.types import StepSpec


@dataclass(frozen=True)
class FormInput:
    key: str
    label: str
    placeholder: str = field(default='')


@dataclass(frozen=True)
class FormStepSpec(StepSpec):
    inputs: list[FormInput] = field(default_factory=list)


class FormStepWidget(QWidget):
    def __init__(self, spec: FormStepSpec):
        super().__init__()
        self.spec = spec
        self._inputs: dict[str, QLineEdit] = {}

        qss_string = spec.qss_string if spec.qss_string else get_qss_string('form_widget.qss')
        self.setStyleSheet(qss_string)

        title = QLabel(spec.title)
        title.setProperty('role', 'step_title')
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(10)

        form = QFormLayout()
        form.setContentsMargins(0, 0, 0, 0)
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        form.setFormAlignment(Qt.AlignmentFlag.AlignTop)

        for inp in spec.inputs:
            lbl = QLabel(inp.label)
            lbl.setProperty('role', 'form_label')

            edit = QLineEdit()
            edit.setProperty('role', 'form_input')
            edit.setPlaceholderText(inp.placeholder)

            self._inputs[inp.key] = edit
            form.addRow(lbl, edit)

        content_layout.addLayout(form)

        wrapper = QWidget()
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.addStretch()
        wrapper_layout.addWidget(content)
        wrapper_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setWidget(wrapper)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(title)
        layout.addItem(QSpacerItem(0, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        layout.addWidget(scroll, 1)

    def value(self) -> dict[str, str]:
        return {k: w.text().strip() for k, w in self._inputs.items()}
