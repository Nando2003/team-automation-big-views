import os
from logging import Logger
from typing import Any, Optional

from PySide6.QtCore import Qt, QThread, Slot
from PySide6.QtGui import QCloseEvent, QIcon
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from big_views.helpers.asset_helpers import get_asset_path
from big_views.helpers.style_helpers import get_qss_string
from big_views.logger import configure_logger
from big_views.screens.initial_screen import InitialScreen
from big_views.screens.loading_screen import LoadingScreen
from big_views.types import FinishFn, FlowSpec, StepSpec
from big_views.workers.pipeline_worker import PipelineWorker


class FlowManager(QWidget):
    def __init__(self, flow: FlowSpec, *, logger: Optional[Logger] = None):
        super().__init__()
        self.flow = flow
        self.logger = logger if logger else configure_logger()

        qss_string = flow.qss_string if flow.qss_string else get_qss_string('app.qss')

        self.setStyleSheet(qss_string)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.context: dict[str, Any] = {}
        self.steps: list[StepSpec] = []
        self.pipeline: list[FinishFn] = []

        self._thread: Optional[QThread] = None
        self._worker: Optional[PipelineWorker] = None

        self.wizard_page = QWidget()
        self.wizard_page.setObjectName('wizard')
        wizard_layout = QVBoxLayout(self.wizard_page)

        self.stack = QStackedWidget()
        self.back_btn = QPushButton('Voltar')
        self.next_btn = QPushButton('Continuar')
        self.back_btn.setProperty('role', 'nav')
        self.next_btn.setProperty('role', 'primary')

        self.back_btn.clicked.connect(self.go_back)
        self.next_btn.clicked.connect(self.go_forward)

        icon_path = os.path.join(get_asset_path(), 'icon_tim.png')
        qicon = QIcon(icon_path)
        self.setWindowIcon(qicon)

        nav_container = QWidget()
        nav_container.setObjectName('nav_container')
        nav = QHBoxLayout(nav_container)
        nav.setContentsMargins(0, 0, 0, 0)
        nav.addWidget(self.back_btn)
        nav.addStretch()
        nav.addWidget(self.next_btn)

        nav_divider = QWidget()
        nav_divider.setObjectName('nav_divider')
        nav_divider.setFixedHeight(1)

        center_container = QWidget()
        center_layout = QVBoxLayout(center_container)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.addWidget(self.stack, 1)
        center_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        wizard_layout.addWidget(center_container, 1)
        wizard_layout.addSpacerItem(
            QSpacerItem(
                0,
                10,
                QSizePolicy.Policy.Minimum,
                QSizePolicy.Policy.Fixed,
            )
        )

        wizard_layout.addWidget(nav_divider, 0)
        wizard_layout.addSpacerItem(
            QSpacerItem(
                0,
                10,
                QSizePolicy.Policy.Minimum,
                QSizePolicy.Policy.Fixed,
            )
        )
        wizard_layout.addWidget(nav_container, 0)

        self.loading_page = LoadingScreen()
        self.initial_page = InitialScreen(flow_name=flow.name, on_start=self.go_to_wizard_page)

        self.root_stack = QStackedWidget()
        self.root_stack.addWidget(self.initial_page)
        self.root_stack.addWidget(self.wizard_page)
        self.root_stack.addWidget(self.loading_page)

        layout = QVBoxLayout(self)
        layout.addWidget(self.root_stack)

        self.load_flow(self.flow)
        self.root_stack.setCurrentIndex(0)

    def current_index(self) -> int:
        return self.stack.currentIndex()

    def current_spec(self) -> StepSpec:
        return self.steps[self.current_index()]

    def load_flow(self, flow: FlowSpec):
        self.context = {}
        self.pipeline = list(flow.on_finish)
        self.steps = list(flow.steps)
        self.rebuild_pages(go_to=0)

    def rebuild_pages(self, go_to: int = 0):
        while self.stack.count():
            w = self.stack.widget(0)
            self.stack.removeWidget(w)
            w.deleteLater()

        for spec in self.steps:
            self.stack.addWidget(self.make_page(spec))

        self.stack.setCurrentIndex(max(0, min(go_to, self.stack.count() - 1)))
        self.update_nav()

    def make_page(self, spec: StepSpec) -> QWidget:
        return spec.widget_cls(spec=spec)  # type: ignore

    def update_nav(self):
        i = self.current_index()
        self.back_btn.setEnabled(i > 0)
        last = self.stack.count() > 0 and i == self.stack.count() - 1
        self.next_btn.setText('Finalizar' if last else 'Continuar')

    def show_warn(self, msg: str):
        QMessageBox.warning(self, 'Aviso', msg)

    def show_success(self, msg: str):
        QMessageBox.information(self, 'Sucesso', msg)

    def show_error(self, msg: str):
        QMessageBox.critical(self, 'Erro', msg)

    def go_back(self):
        i = self.current_index()
        if i > 0:
            self.stack.setCurrentIndex(i - 1)
            self.update_nav()

    def go_forward(self):
        spec = self.current_spec()

        page = self.stack.currentWidget()
        val = page.value() if hasattr(page, 'value') else None  # type: ignore

        if spec.validator:
            ok, err = spec.validator(val)
            if not ok:
                self.show_warn(err)
                return

        self.context[spec.key] = val

        if self.current_index() == self.stack.count() - 1:
            reply = QMessageBox(self)

            reply.setWindowTitle('Confirmar')
            reply.setText('O robô irá iniciar a execução do fluxo agora.\n\nDeseja continuar?\n')

            pt_yes_button = reply.addButton('Sim', QMessageBox.ButtonRole.YesRole)
            pt_no_button = reply.addButton('Não', QMessageBox.ButtonRole.NoRole)

            reply.setDefaultButton(pt_no_button)

            reply.setIcon(QMessageBox.Icon.Question)
            reply.exec()

            if reply.clickedButton() == pt_yes_button:
                self.run_pipeline_threaded()
            return

        self.stack.setCurrentIndex(self.current_index() + 1)
        self.update_nav()

    def run_pipeline_threaded(self):
        if not self.pipeline:
            self.show_success('Fluxo concluído com sucesso!')
            return

        self.next_btn.setEnabled(False)
        self.back_btn.setEnabled(False)

        self.root_stack.setCurrentIndex(2)

        ctx_copy = self.context.copy()

        self._thread = QThread(self)
        self._worker = PipelineWorker(ctx_copy, self.pipeline, self.logger)
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self.loading_page.set_progress)
        self._worker.status.connect(self.loading_page.set_status)
        self._worker.finished.connect(self.on_finished)
        self._worker.error.connect(self.on_error)

        self._worker.finished.connect(self._thread.quit)
        self._worker.error.connect(self._thread.quit)
        self._thread.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)

        self._thread.start()

    @Slot(dict)
    def on_finished(self, ctx: dict[str, Any]):
        self.context.update(ctx)
        self.next_btn.setEnabled(True)
        self.back_btn.setEnabled(True)
        self.show_success('Fluxo concluído com sucesso!')
        self.restart_to_beginning()

    @Slot(str)
    def on_error(self, error_msg: str):
        self.next_btn.setEnabled(True)
        self.back_btn.setEnabled(True)
        self.show_error(f'Ocorreu um erro durante a execução do fluxo:\n\n{error_msg}')
        self.restart_to_beginning()

    def restart_to_beginning(self):
        self.load_flow(self.flow)
        self.root_stack.setCurrentIndex(1)

    def go_to_wizard_page(self):
        self.root_stack.setCurrentIndex(1)

    def closeEvent(self, event: QCloseEvent):  # noqa: N802
        if not event.spontaneous():
            event.accept()
            return

        reply = QMessageBox(self)
        reply.setWindowTitle('Encerrar')
        reply.setText('Deseja finalizar e encerrar o robô?\n')
        pt_yes_button = reply.addButton('Sim', QMessageBox.ButtonRole.YesRole)
        pt_no_button = reply.addButton('Não', QMessageBox.ButtonRole.NoRole)
        reply.setDefaultButton(pt_no_button)
        reply.setIcon(QMessageBox.Icon.Question)

        reply.exec()

        if reply.clickedButton() != pt_yes_button:
            event.ignore()
            return

        event.accept()
