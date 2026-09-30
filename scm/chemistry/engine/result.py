from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar


T = TypeVar("T")


class ResultStatus(str, Enum):
    SUCCESS = "success"
    WARNING = "warning"
    INCONCLUSIVE = "inconclusive"
    FAILURE = "failure"


@dataclass(frozen=True)
class CalculationResult(Generic[T]):
    status: ResultStatus
    value: T | None = None
    message: str | None = None
    reasons: tuple[str, ...] = ()

    @property
    def successful(self) -> bool:
        return self.status is ResultStatus.SUCCESS

    @property
    def usable(self) -> bool:
        return self.status in {
            ResultStatus.SUCCESS,
            ResultStatus.WARNING,
        }
