from __future__ import annotations

from .base import IsotopePropertyData
from .identity import IsotopePropertyIdentity


_ISOTOPE_PROPERTIES: dict[
    tuple[int, int],
    tuple[IsotopePropertyData, ...],
] = {}


def register_isotope_property(
    property_data: IsotopePropertyData,
) -> None:
    """
    Register one scientific property record for an isotope.

    Multiple records sharing the same property identity are allowed.
    They may represent different conditions, evidence, uncertainty,
    measurements, or reference sources.
    """

    if not isinstance(
        property_data,
        IsotopePropertyData,
    ):
        raise TypeError(
            "property_data must be an IsotopePropertyData"
        )

    isotope_identity = property_data.isotope.identity

    existing = _ISOTOPE_PROPERTIES.get(
        isotope_identity,
        (),
    )

    _ISOTOPE_PROPERTIES[isotope_identity] = (
        *existing,
        property_data,
    )


def get_isotope_properties(
    isotope_identity: tuple[int, int],
) -> tuple[IsotopePropertyData, ...]:
    """
    Return all scientific property records for an isotope.

    The isotope identity is:
        (atomic number Z, mass number A)
    """

    if not isinstance(
        isotope_identity,
        tuple,
    ):
        raise TypeError(
            "isotope identity must be a (Z, A) tuple"
        )

    if len(isotope_identity) != 2:
        raise ValueError(
            "isotope identity must be a (Z, A) tuple"
        )

    atomic_number, mass_number = isotope_identity

    if not isinstance(atomic_number, int):
        raise TypeError(
            "atomic number must be an integer"
        )

    if not isinstance(mass_number, int):
        raise TypeError(
            "mass number must be an integer"
        )

    if not 1 <= atomic_number <= 118:
        raise ValueError(
            "atomic number must be between 1 and 118"
        )

    if mass_number < atomic_number:
        raise ValueError(
            "mass number cannot be less than atomic number"
        )

    return _ISOTOPE_PROPERTIES.get(
        isotope_identity,
        (),
    )


def get_isotope_properties_by_identity(
    identity: IsotopePropertyIdentity,
) -> tuple[IsotopePropertyData, ...]:
    """
    Return all records sharing the same stable property identity.
    """

    if not isinstance(
        identity,
        IsotopePropertyIdentity,
    ):
        raise TypeError(
            "identity must be an IsotopePropertyIdentity"
        )

    return tuple(
        property_data
        for property_data in get_isotope_properties(
            (
                identity.atomic_number,
                identity.mass_number,
            )
        )
        if property_data.identity == identity
    )


def get_isotope_properties_by_kind(
    isotope_identity: tuple[int, int],
    kind,
) -> tuple[IsotopePropertyData, ...]:
    """
    Return all property records of a given PropertyKind
    for one isotope.
    """

    from scm.core import PropertyKind

    if not isinstance(
        kind,
        PropertyKind,
    ):
        raise TypeError(
            "kind must be a PropertyKind"
        )

    return tuple(
        property_data
        for property_data in get_isotope_properties(
            isotope_identity
        )
        if property_data.kind is kind
    )


def get_isotope_properties_matching_conditions(
    isotope_identity: tuple[int, int],
    kind,
    conditions,
) -> tuple[IsotopePropertyData, ...]:
    """
    Return isotope property records of a given kind that
    are compatible with requested conditions.
    """

    from scm.core import PropertyKind

    if not isinstance(
        kind,
        PropertyKind,
    ):
        raise TypeError(
            "kind must be a PropertyKind"
        )

    return tuple(
        property_data
        for property_data in get_isotope_properties_by_kind(
            isotope_identity,
            kind,
        )
        if property_data.matches_conditions(
            conditions
        )
    )


def get_isotope_property(
    isotope_identity: tuple[int, int],
    kind,
) -> IsotopePropertyData | None:
    """
    Return the first property record of the requested kind,
    if one exists.
    """

    properties = get_isotope_properties_by_kind(
        isotope_identity,
        kind,
    )

    if not properties:
        return None

    return properties[0]


def all_isotope_properties() -> tuple[
    IsotopePropertyData,
    ...,
]:
    """
    Return every registered isotope property record.
    """

    return tuple(
        property_data
        for properties in _ISOTOPE_PROPERTIES.values()
        for property_data in properties
    )


__all__ = [
    "register_isotope_property",
    "get_isotope_properties",
    "get_isotope_properties_by_identity",
    "get_isotope_properties_by_kind",
    "get_isotope_properties_matching_conditions",
    "get_isotope_property",
    "all_isotope_properties",
]
