from dataclasses import dataclass, field
from logging import Logger
from typing import Any, Callable, Optional, Protocol, Type, TypedDict, Unpack

from PySide6.QtWidgets import QWidget

Validator = Callable[[Any], tuple[bool, str]]


class FinishFn(Protocol):
    def __name__(self) -> str: ...

    def __call__(
        self,
        context: dict[str, Any],
        logger: Logger,
        **kwargs: Unpack['FinishFnKwargs'],
    ) -> None: ...


class FinishFnKwargs(TypedDict):
    status: Callable[[str], None]
    progress: Callable[[int], None]
    progress_percentage: int
    step_of: str
    step_name: str
    full_step_name: str


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
