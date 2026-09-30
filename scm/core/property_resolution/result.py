from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar


T = TypeVar("T")


class ResolutionStatus(str, Enum):
    """
    Scientific property-resolution states.

    A resolver must distinguish successful resolution from
    absence of data and unresolved ambiguity.
    """

    RESOLVED = "resolved"
    AMBIGUOUS = "ambiguous"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class PropertyResolution(Generic[T]):
    """
    Result of a scientific property-resolution attempt.

    The candidate records are preserved so downstream systems
    can inspect provenance and explain why a resolution occurred
    or failed.
    """

    status: ResolutionStatus
    value: T | None = None
    candidates: tuple[T, ...] = ()
    reasons: tuple[str, ...] = ()

    @property
    def resolved(self) -> bool:
        return self.status is ResolutionStatus.RESOLVED

    @property
    def usable(self) -> bool:
        return self.resolved and self.value is not None


__all__ = [
    "ResolutionStatus",
    "PropertyResolution",
]
