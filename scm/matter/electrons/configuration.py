from __future__ import annotations

from dataclasses import dataclass

from .occupancy import OrbitalOccupancy, SubshellOccupancy
from .structure import ElectronShell, ElectronSubshell


@dataclass(frozen=True, init=False)
class ElectronConfiguration:
    """
    Electronic configuration.

    Structured SubshellOccupancy objects are the canonical internal state.

    The legacy `subshells=` constructor remains supported so existing
    consumers do not break during the architectural migration.
    """

    _occupancies: tuple[SubshellOccupancy, ...]

    def __init__(
        self,
        occupancies: tuple[SubshellOccupancy, ...] | None = None,
        *,
        subshells: tuple[ElectronSubshell, ...] | None = None,
    ) -> None:
        if occupancies is not None and subshells is not None:
            raise TypeError(
                "provide either occupancies or subshells, not both"
            )

        if occupancies is None:
            if subshells is None:
                occupancies = ()
            else:
                occupancies = tuple(
                    SubshellOccupancy.from_electron_count(
                        item.principal_level,
                        item.subshell,
                        item.electron_count,
                    )
                    for item in subshells
                )

        occupancies = tuple(occupancies)

        for occupancy in occupancies:
            if not isinstance(occupancy, SubshellOccupancy):
                raise TypeError(
                    "all occupancies must be SubshellOccupancy instances"
                )

        object.__setattr__(self, "_occupancies", occupancies)

        if not self.validate_pauli:
            raise ValueError("configuration violates Pauli exclusion constraints")

        if not self.validate_hund:
            raise ValueError("configuration violates Hund occupation constraints")

    @classmethod
    def from_occupancies(
        cls,
        occupancies: tuple[SubshellOccupancy, ...],
    ) -> "ElectronConfiguration":
        return cls(occupancies=tuple(occupancies))

    @classmethod
    def from_subshell_counts(
        cls,
        subshells: tuple[tuple[int, str, int], ...],
        *,
        enforce_hund: bool = True,
    ) -> "ElectronConfiguration":
        occupancies = tuple(
            SubshellOccupancy.from_electron_count(
                n,
                subshell,
                electron_count,
                enforce_hund=enforce_hund,
            )
            for n, subshell, electron_count in subshells
        )

        return cls(occupancies=occupancies)

    @property
    def occupancies(self) -> tuple[SubshellOccupancy, ...]:
        return self._occupancies

    @property
    def subshells(self) -> tuple[ElectronSubshell, ...]:
        """
        Legacy compatibility projection.

        ElectronSubshell objects are derived from the authoritative
        structured occupancy state.
        """
        return tuple(
            ElectronSubshell(
                principal_level=occupancy.principal_level,
                subshell=occupancy.subshell,
                electron_count=occupancy.electron_count,
            )
            for occupancy in self._occupancies
        )

    @property
    def electron_count(self) -> int:
        return sum(
            occupancy.electron_count
            for occupancy in self._occupancies
        )

    @property
    def shells(self) -> tuple[ElectronShell, ...]:
        counts: dict[int, int] = {}

        for occupancy in self._occupancies:
            n = occupancy.principal_level
            counts[n] = counts.get(n, 0) + occupancy.electron_count

        return tuple(
            ElectronShell(
                principal_level=n,
                electron_count=count,
            )
            for n, count in sorted(counts.items())
        )

    @property
    def orbital_occupancies(self) -> tuple[OrbitalOccupancy, ...]:
        return tuple(
            orbital
            for occupancy in self._occupancies
            for orbital in occupancy.orbitals
        )

    @property
    def unpaired_electron_count(self) -> int:
        return sum(
            occupancy.unpaired_electron_count
            for occupancy in self._occupancies
        )

    @property
    def spin_multiplicity(self) -> int:
        return self.unpaired_electron_count + 1

    @property
    def valence_electron_count(self) -> int:
        if not self._occupancies:
            return 0

        highest_n = max(
            occupancy.principal_level
            for occupancy in self._occupancies
        )

        return sum(
            occupancy.electron_count
            for occupancy in self._occupancies
            if occupancy.principal_level == highest_n
        )

    @property
    def validate_pauli(self) -> bool:
        return all(
            occupancy.validate_pauli()
            for occupancy in self._occupancies
        )

    @property
    def validate_hund(self) -> bool:
        return all(
            occupancy.validate_hund()
            for occupancy in self._occupancies
        )

    def validate(self) -> bool:
        """
        Legacy validation entry point.

        Preserved for existing callers and tests.
        """
        return self.validate_pauli and self.validate_hund

    @property
    def is_hund_ground_state(self) -> bool:
        return self.validate_hund

    def notation(self) -> str:
        return " ".join(
            occupancy.notation
            for occupancy in self._occupancies
        )

    def __str__(self) -> str:
        return self.notation()
