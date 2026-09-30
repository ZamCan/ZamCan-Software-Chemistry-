from __future__ import annotations

from scm.core import ScientificProperty

from .base import ElementPropertyData
from .atomic import get_atomic_properties


def atomic_property_name(
    property_data: ElementPropertyData,
) -> str:
    """
    Convert a PropertyKind into the canonical
    human-readable property name used by SCM.
    """

    if not isinstance(
        property_data,
        ElementPropertyData,
    ):
        raise TypeError(
            "property_data must be an ElementPropertyData"
        )

    return property_data.kind.value.replace(
        "_",
        " ",
    )


def convert_atomic_property(
    property_data: ElementPropertyData,
) -> ScientificProperty:
    """
    Convert one atomic data-layer property
    into the common SCM ScientificProperty.
    """

    if not isinstance(
        property_data,
        ElementPropertyData,
    ):
        raise TypeError(
            "property_data must be an ElementPropertyData"
        )

    return property_data.to_scientific_property(
        atomic_property_name(property_data)
    )


def convert_atomic_properties(
    atomic_number: int,
) -> tuple[ScientificProperty, ...]:
    """
    Convert all registered atomic properties for
    one element into SCM ScientificProperty objects.
    """

    return tuple(
        convert_atomic_property(
            property_data
        )
        for property_data in get_atomic_properties(
            atomic_number
        )
    )


__all__ = [
    "atomic_property_name",
    "convert_atomic_property",
    "convert_atomic_properties",
]
