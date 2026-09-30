from __future__ import annotations

from dataclasses import dataclass

from scm.core import PropertyKind


@dataclass(frozen=True)
class PropertyIdentity:
    """
    Stable identity for a scientific element property.

    The identity describes what kind of property is being represented
    for which element. Conditions and evidence are intentionally kept
    outside this identity because multiple measurements or references
    may legitimately describe the same property.
    """

    atomic_number: int
    kind: PropertyKind

    def __post_init__(self) -> None:
        if not isinstance(
            self.atomic_number,
            int,
        ):
            raise TypeError(
                "atomic number must be an integer"
            )

        if not 1 <= self.atomic_number <= 118:
            raise ValueError(
                "atomic number must be between 1 and 118"
            )

        if not isinstance(
            self.kind,
            PropertyKind,
        ):
            raise TypeError(
                "kind must be a PropertyKind"
            )


__all__ = [
    "PropertyIdentity",
]
