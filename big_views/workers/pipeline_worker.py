import traceback
from logging import Logger
from typing import Any, List

from PySide6.QtCore import QObject, Signal, Slot

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

    @Slot()
    def run(self):
        try:
            total = len(self.pipeline)
            self.logger.info('Pipeline iniciado (%d etapas)', total)

            self.progress.emit(0)
            self.status.emit('Iniciando')

            for i, fn in enumerate(self.pipeline, start=1):
                pct = int((i - 1) / total * 100)
                etapa_txt = f'Etapa {i} de {total}: {fn.__name__}'

                self.logger.info(etapa_txt)
                self.status.emit(etapa_txt)
                self.progress.emit(pct)

                fn(self.ctx, self.logger)

            self.status.emit('Concluído')
            self.progress.emit(100)
            self.logger.info('Pipeline concluído com sucesso')
            self.finished.emit(self.ctx)

        except Exception:
            tb = traceback.format_exc()
            self.logger.exception('Erro no pipeline')
            self.error.emit(tb)
