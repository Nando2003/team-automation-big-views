import inspect
import traceback
from logging import Logger
from typing import Any, List

from PySide6.QtCore import QObject, Signal, Slot

from big_views.exceptions.pipeline_expected_error import PipelineExceptedError
from big_views.types import FinishFn


class PipelineWorker(QObject):
    progress = Signal(int)
    status = Signal(str)
    error = Signal(str)
    finished = Signal(dict)

    def __init__(
        self,
        ctx: dict[str, Any],
        pipeline: List[FinishFn],
        logger: Logger,
    ):
        super().__init__()
        self.ctx = ctx
        self.pipeline = pipeline
        self.logger = logger

    def _call_step(
        self,
        fn: FinishFn,
        progress_percentage: int,
        step_of: str,
        step_name: str,
        full_step_name: str,
    ) -> None:
        sig = inspect.signature(fn)
        params = sig.parameters

        kwargs: dict[str, Any] = {}

        if 'kwargs' in params:
            kwargs = {
                'status': self.status.emit,
                'progress': self.progress.emit,
                'progress_percentage': progress_percentage,
                'step_of': step_of,
                'step_name': step_name,
                'full_step_name': full_step_name,
            }

        fn(self.ctx, self.logger, **kwargs)

    @Slot()
    def run(self):
        try:
            total = len(self.pipeline)
            self.logger.info('Pipeline iniciado (%d etapas)', total)

            self.progress.emit(0)
            self.status.emit('Iniciando')

            for i, fn in enumerate(self.pipeline, start=1):
                pct = int((i - 1) / total * 100)
                step_of = f'Etapa {i} de {total}:'
                step_name = f'{fn.__name__}'
                full_step_name = f'{step_of} {step_name}'

                self.logger.info(full_step_name)
                self.status.emit(full_step_name)
                self.progress.emit(pct)

                self._call_step(fn, pct, step_of, step_name, full_step_name)

            self.status.emit('Concluído')
            self.progress.emit(100)
            self.logger.info('Pipeline concluído com sucesso')
            self.finished.emit(self.ctx)

        except Exception as e:
            tb = traceback.format_exc()
            self.logger.warning('Erro no pipeline: %s', tb)

            if isinstance(e, PipelineExceptedError):
                popup_msg = e.popup_message
                self.error.emit(popup_msg)
            else:
                self.error.emit(tb)
