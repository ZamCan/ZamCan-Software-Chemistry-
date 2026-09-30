from __future__ import annotations

from collections import Counter
from typing import Any


def validate_atomic_numbers(
    records: tuple[Any, ...],
) -> None:
    numbers = []

    for record in records:
        atomic_number = getattr(record, "atomic_number", None)

        if not isinstance(atomic_number, int):
            raise TypeError(
                "atomic_number must be an integer"
            )

        if not 1 <= atomic_number <= 118:
            raise ValueError(
                f"atomic_number must be between 1 and 118: "
                f"{atomic_number}"
            )

        numbers.append(atomic_number)

    duplicates = [
        number
        for number, count in Counter(numbers).items()
        if count > 1
    ]

    if duplicates:
        raise ValueError(
            f"duplicate atomic numbers: {duplicates}"
        )


def validate_complete_periodic_table(
    records: tuple[Any, ...],
) -> None:
    validate_atomic_numbers(records)

    numbers = {
        record.atomic_number
        for record in records
    }

    expected = set(range(1, 119))

    missing = sorted(expected - numbers)
    extra = sorted(numbers - expected)

    if missing:
        raise ValueError(
            f"missing atomic numbers: {missing}"
        )

    if extra:
        raise ValueError(
            f"unexpected atomic numbers: {extra}"
        )
