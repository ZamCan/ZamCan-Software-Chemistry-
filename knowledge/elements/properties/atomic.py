from __future__ import annotations

from scm.core import PropertyKind

from .base import ElementPropertyData
from .identity import PropertyIdentity


_ATOMIC_PROPERTIES: dict[
    int,
    tuple[ElementPropertyData, ...],
] = {}


def register_atomic_property(
    property_data: ElementPropertyData,
) -> None:
    """
    Register one atomic-related property record.

    Multiple records with the same PropertyIdentity are allowed.
    They may represent different conditions, evidence, uncertainty,
    measurements, or reference sources.
    """

    if not isinstance(
        property_data,
        ElementPropertyData,
    ):
        raise TypeError(
            "property_data must be an ElementPropertyData"
        )

    atomic_number = property_data.atomic_number

    existing = _ATOMIC_PROPERTIES.get(
        atomic_number,
        (),
    )

    _ATOMIC_PROPERTIES[atomic_number] = (
        *existing,
        property_data,
    )


def get_atomic_properties(
    atomic_number: int,
) -> tuple[ElementPropertyData, ...]:
    if not isinstance(atomic_number, int):
        raise TypeError(
            "atomic number must be an integer"
        )

    if not 1 <= atomic_number <= 118:
        raise ValueError(
            "atomic number must be between 1 and 118"
        )

    return _ATOMIC_PROPERTIES.get(
        atomic_number,
        (),
    )


def get_atomic_properties_by_kind(
    atomic_number: int,
    kind: PropertyKind,
) -> tuple[ElementPropertyData, ...]:
    """
    Return all property records matching an element and PropertyKind.

    Multiple records are allowed because they may represent
    different conditions, evidence, uncertainty, measurements,
    or reference sources.
    """

    if not isinstance(
        kind,
        PropertyKind,
    ):
        raise TypeError(
            "kind must be a PropertyKind"
        )

    return tuple(
        property_data
        for property_data in get_atomic_properties(
            atomic_number
        )
        if property_data.kind is kind
    )


def get_atomic_properties_matching_conditions(
    atomic_number: int,
    kind: PropertyKind,
    conditions,
) -> tuple[ElementPropertyData, ...]:
    """
    Return all property records of a given kind that are
    compatible with the requested conditions.

    Condition matching is delegated to ElementPropertyData
    so the scientific compatibility rules remain centralized.
    """

    if not isinstance(
        kind,
        PropertyKind,
    ):
        raise TypeError(
            "kind must be a PropertyKind"
        )

    return tuple(
        property_data
        for property_data in get_atomic_properties_by_kind(
            atomic_number,
            kind,
        )
        if property_data.matches_conditions(
            conditions
        )
    )


def get_atomic_property(
    atomic_number: int,
    kind: PropertyKind,
) -> ElementPropertyData | None:
    if not isinstance(
        kind,
        PropertyKind,
    ):
        raise TypeError(
            "kind must be a PropertyKind"
        )

    properties = get_atomic_properties(
        atomic_number
    )

    for property_data in properties:
        if property_data.kind is kind:
            return property_data

    return None


def get_atomic_properties_by_identity(
    identity: PropertyIdentity,
) -> tuple[ElementPropertyData, ...]:
    """
    Return all property records sharing the same stable identity.
    """

    if not isinstance(
        identity,
        PropertyIdentity,
    ):
        raise TypeError(
            "identity must be a PropertyIdentity"
        )

    return tuple(
        property_data
        for property_data in get_atomic_properties(
            identity.atomic_number
        )
        if property_data.identity == identity
    )


def get_atomic_properties_by_identity_and_conditions(
    identity: PropertyIdentity,
    conditions,
) -> tuple[ElementPropertyData, ...]:
    """
    Return all property records matching a PropertyIdentity
    and compatible with the requested conditions.
    """

    if not isinstance(
        identity,
        PropertyIdentity,
    ):
        raise TypeError(
            "identity must be a PropertyIdentity"
        )

    return tuple(
        property_data
        for property_data in get_atomic_properties_by_identity(
            identity
        )
        if property_data.matches_conditions(
            conditions
        )
    )


def all_atomic_properties() -> tuple[
    ElementPropertyData,
    ...,
]:
    return tuple(
        property_data
        for properties in _ATOMIC_PROPERTIES.values()
        for property_data in properties
    )


__all__ = [
    "register_atomic_property",
    "get_atomic_properties",
    "get_atomic_properties_by_kind",
    "get_atomic_properties_matching_conditions",
    "get_atomic_properties_by_identity_and_conditions",
    "get_atomic_property",
    "get_atomic_properties_by_identity",
    "all_atomic_properties",
]
