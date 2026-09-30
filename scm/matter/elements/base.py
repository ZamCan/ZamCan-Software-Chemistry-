from __future__ import annotations

from dataclasses import dataclass

from scm.matter.isotopes import Isotope


@dataclass(frozen=True)
class Element:
    """
    Identity model of a chemical element.

    An element is uniquely defined by its atomic number Z,
    which is the number of protons in its nucleus.
    """

    atomic_number: int

    def __post_init__(self) -> None:
        if self.atomic_number < 1:
            raise ValueError(
                "atomic number must be at least 1"
            )

    @property
    def proton_count(self) -> int:
        """Number of protons defining this element."""
        return self.atomic_number

    @property
    def identity(self) -> int:
        """
        Machine-safe element identity.

        The atomic number Z uniquely identifies an element.
        """
        return self.atomic_number

    def contains_isotope(self, isotope: Isotope) -> bool:
        """
        Return True when the isotope belongs to this element.

        Element identity is determined exclusively by Z.
        """
        return self.atomic_number == isotope.atomic_number

    def same_element(self, other: "Element") -> bool:
        """Return True when both objects represent the same element."""
        return self.identity == other.identity

    def __str__(self) -> str:
        return f"Element(Z={self.atomic_number})"
