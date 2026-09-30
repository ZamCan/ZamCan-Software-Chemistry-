from dataclasses import dataclass

import pytest

from knowledge.elements.loaders.validation import (
    validate_atomic_numbers,
    validate_complete_periodic_table,
)


@dataclass(frozen=True)
class Record:
    atomic_number: int


def test_valid_atomic_numbers():
    validate_atomic_numbers(
        (
            Record(1),
            Record(6),
            Record(118),
        )
    )


def test_duplicate_atomic_numbers_rejected():
    with pytest.raises(ValueError):
        validate_atomic_numbers(
            (
                Record(1),
                Record(1),
            )
        )


def test_complete_periodic_table_requires_all_118():
    records = tuple(
        Record(number)
        for number in range(1, 119)
    )

    validate_complete_periodic_table(records)


def test_incomplete_periodic_table_rejected():
    records = tuple(
        Record(number)
        for number in range(1, 118)
    )

    with pytest.raises(ValueError):
        validate_complete_periodic_table(records)
