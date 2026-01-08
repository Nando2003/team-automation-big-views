from dataclasses import dataclass, field
from logging import Logger
from typing import Any, Callable, Optional, Type

from PySide6.QtWidgets import QWidget

StatusCb = Callable[[str], None]
ProgressCb = Callable[[int], None]

Validator = Callable[[Any], tuple[bool, str]]
FinishFn = Callable[[dict[str, Any], Logger, StatusCb, ProgressCb], None]


@dataclass(frozen=True)
class StepSpec:
    key: str
    title: str
    widget_cls: Type[QWidget]
    validator: Optional[Validator] = field(default=None)
    qss_string: Optional[str] = field(default=None)


@dataclass
class FlowSpec:
    name: str
    steps: list[StepSpec]
    on_finish: list[FinishFn] = field(default_factory=list)
    qss_string: Optional[str] = field(default=None)
