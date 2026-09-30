from __future__ import annotations

from knowledge.isotopes.schema.isotope_data import IsotopeData
from scm.core.scientific_values import ScientificValue

from .base import RawIsotopeRecord
from .validation import validate_raw_isotope


def normalize_isotope(
    record: RawIsotopeRecord,
) -> IsotopeData:
    """
    Convert a validated raw isotope record into normalized SCM data.
    """

    validate_raw_isotope(record)

    half_life = None

    if (
        record.half_life is not None
        and record.half_life_unit is not None
    ):
        half_life = ScientificValue(
            value=record.half_life,
            unit=record.half_life_unit,
        )

    isotopic_mass = None

    if record.isotopic_mass is not None:
        isotopic_mass = ScientificValue(
            value=record.isotopic_mass,
            unit="u",
            uncertainty=record.isotopic_mass_uncertainty,
        )

    natural_abundance = None

    if record.natural_abundance is not None:
        natural_abundance = ScientificValue(
            value=record.natural_abundance,
            unit="1",
            uncertainty=record.natural_abundance_uncertainty,
        )

    mass_excess = None

    if record.mass_excess is not None:
        mass_excess = ScientificValue(
            value=record.mass_excess,
            unit="MeV",
            uncertainty=record.mass_excess_uncertainty,
        )

    binding_energy = None

    if record.binding_energy is not None:
        binding_energy = ScientificValue(
            value=record.binding_energy,
            unit="MeV",
            uncertainty=record.binding_energy_uncertainty,
        )

    return IsotopeData(
        atomic_number=record.atomic_number,
        mass_number=record.mass_number,
        name=record.name,
        symbol=record.symbol,
        isotopic_mass=isotopic_mass,
        stable=record.stable,
        naturally_occurring=record.naturally_occurring,
        natural_abundance=natural_abundance,
        half_life=half_life,
        spin=record.spin,
        parity=record.parity,
        mass_excess=mass_excess,
        binding_energy=binding_energy,
        notes=record.notes,
    )
