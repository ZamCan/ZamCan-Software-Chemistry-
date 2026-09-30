from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar


RawT = TypeVar("RawT")
NormalizedT = TypeVar("NormalizedT")


class ElementDataLoader(
    ABC,
    Generic[RawT, NormalizedT],
):
    """
    Source-independent interface for element-data ingestion.

    Raw source formats must be converted into normalized SCM
    scientific data before entering the authoritative knowledge
    registry.
    """

    name: str = "unnamed"

    @abstractmethod
    def load(self) -> tuple[RawT, ...]:
        """Load raw records from an authoritative source."""
        raise NotImplementedError

    @abstractmethod
    def normalize(
        self,
        records: tuple[RawT, ...],
    ) -> tuple[NormalizedT, ...]:
        """Normalize raw records into SCM-compatible records."""
        raise NotImplementedError

    def run(self) -> tuple[NormalizedT, ...]:
        records = self.load()
        return self.normalize(records)
