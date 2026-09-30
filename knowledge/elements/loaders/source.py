from __future__ import annotations

from abc import ABC, abstractmethod

from knowledge.elements.loaders.records import RawElementRecord


class ElementDataSource(ABC):
    """
    Contract for authoritative element-data providers.

    Providers must return source records without inventing or
    filling missing scientific values.
    """

    name: str = "unnamed"
    authority: str = "unknown"

    @abstractmethod
    def records(self) -> tuple[RawElementRecord, ...]:
        raise NotImplementedError

    def validate(self) -> None:
        records = self.records()

        if not records:
            raise ValueError(
                f"{self.name} returned no element records"
            )

        numbers = [
            record.atomic_number
            for record in records
        ]

        if len(numbers) != len(set(numbers)):
            raise ValueError(
                f"{self.name} contains duplicate elements"
            )
