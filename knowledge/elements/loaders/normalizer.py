from __future__ import annotations

from typing import Any


class ElementNormalizer:
    """
    Generic normalization boundary.

    Source adapters should convert source-specific records into
    dictionaries containing only scientifically identified fields.
    Missing scientific values remain missing; they are never guessed.
    """

    @staticmethod
    def normalize_record(record: Any) -> dict[str, Any]:
        if not isinstance(record, dict):
            raise TypeError(
                "raw element record must be a dictionary"
            )

        if "atomic_number" not in record:
            raise ValueError(
                "raw element record requires atomic_number"
            )

        normalized = dict(record)

        for key, value in normalized.items():
            if value is None:
                continue

            if isinstance(value, str):
                normalized[key] = value.strip()

        return normalized

    @classmethod
    def normalize(
        cls,
        records: tuple[dict[str, Any], ...],
    ) -> tuple[dict[str, Any], ...]:
        return tuple(
            cls.normalize_record(record)
            for record in records
        )
