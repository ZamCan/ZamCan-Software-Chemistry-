from __future__ import annotations

from enum import Enum


class PropertyKind(str, Enum):
    """
    Controlled scientific-property categories used by SCM.

    These describe what a property represents without
    prescribing its numerical value or unit.
    """

    STANDARD_ATOMIC_WEIGHT = "standard_atomic_weight"
    RELATIVE_ATOMIC_MASS = "relative_atomic_mass"
    ISOTOPIC_ATOMIC_MASS = "isotopic_atomic_mass"
    MOLAR_MASS = "molar_mass"
    ATOMIC_MASS = "atomic_mass"
    DENSITY = "density"
    MELTING_POINT = "melting_point"
    BOILING_POINT = "boiling_point"
    IONIZATION_ENERGY = "ionization_energy"
    ELECTRON_AFFINITY = "electron_affinity"
    ELECTRONEGATIVITY = "electronegativity"
    ATOMIC_RADIUS = "atomic_radius"
    COVALENT_RADIUS = "covalent_radius"
    ELECTRICAL_CONDUCTIVITY = "electrical_conductivity"
    THERMAL_CONDUCTIVITY = "thermal_conductivity"
    HEAT_CAPACITY = "heat_capacity"
    ENTHALPY = "enthalpy"
    ENTROPY = "entropy"
    GIBBS_FREE_ENERGY = "gibbs_free_energy"
    OTHER = "other"


__all__ = [
    "PropertyKind",
]
