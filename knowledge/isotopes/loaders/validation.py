from __future__ import annotations

from .base import RawIsotopeRecord


def validate_raw_isotope(record: RawIsotopeRecord) -> None:
    """
    Validate structural constraints of a raw isotope record.

    This validates structure only. It does not judge scientific truth.
    """

    if not isinstance(record, RawIsotopeRecord):
        raise TypeError("record must be a RawIsotopeRecord")

    if not 1 <= record.atomic_number <= 118:
        raise ValueError(
            "atomic_number must be between 1 and 118"
        )

    if record.mass_number < record.atomic_number:
        raise ValueError(
            "mass_number cannot be less than atomic_number"
        )

    if record.natural_abundance is not None:
        if not 0 <= record.natural_abundance <= 1:
            raise ValueError(
                "natural_abundance must be between 0 and 1"
            )

    for field_name in (
        "isotopic_mass_uncertainty",
        "natural_abundance_uncertainty",
        "mass_excess_uncertainty",
        "binding_energy_uncertainty",
    ):
        value = getattr(record, field_name)

        if value is not None and value < 0:
            raise ValueError(
                f"{field_name} cannot be negative"
            )

    if record.stable is not None and not isinstance(
        record.stable,
        bool,
    ):
        raise TypeError("stable must be a bool or None")

    if (
        record.naturally_occurring is not None
        and not isinstance(record.naturally_occurring, bool)
    ):
        raise TypeError(
            "naturally_occurring must be a bool or None"
        )
