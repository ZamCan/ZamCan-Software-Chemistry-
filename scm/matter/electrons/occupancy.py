from __future__ import annotations

from dataclasses import dataclass

from .orbital import ElectronOrbital
from .spin import ElectronSpin, OrbitalElectron
from .subshell import SubshellDefinition, define_subshell


@dataclass(frozen=True)
class OrbitalOccupancy:
    """Explicit electron occupancy of one atomic orbital."""

    orbital: ElectronOrbital
    electrons: tuple[OrbitalElectron, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.orbital, ElectronOrbital):
            raise TypeError("orbital must be an ElectronOrbital")

        if not isinstance(self.electrons, tuple):
            raise TypeError("electrons must be a tuple")

        for electron in self.electrons:
            if not isinstance(electron, OrbitalElectron):
                raise TypeError(
                    "every orbital electron must be an OrbitalElectron"
                )

        if len(self.electrons) > 2:
            raise ValueError(
                "an orbital cannot contain more than two electrons"
            )

        if len(self.electrons) == 2:
            spins = tuple(e.spin for e in self.electrons)

            if spins[0] is spins[1]:
                raise ValueError(
                    "two electrons in one orbital must have opposite spins"
                )

        if len(self.electrons) != self.orbital.electron_count:
            raise ValueError(
                "electron occupancy does not match orbital electron_count"
            )

    @classmethod
    def empty(cls, orbital: ElectronOrbital) -> "OrbitalOccupancy":
        if not isinstance(orbital, ElectronOrbital):
            raise TypeError("orbital must be an ElectronOrbital")

        return cls(
            orbital=orbital,
            electrons=(),
        )

    @classmethod
    def single(
        cls,
        orbital: ElectronOrbital,
        spin: ElectronSpin = ElectronSpin.UP,
    ) -> "OrbitalOccupancy":
        if not isinstance(orbital, ElectronOrbital):
            raise TypeError("orbital must be an ElectronOrbital")

        if not isinstance(spin, ElectronSpin):
            raise TypeError("spin must be an ElectronSpin")

        if orbital.electron_count != 1:
            raise ValueError(
                "single occupancy requires orbital.electron_count == 1"
            )

        return cls(
            orbital=orbital,
            electrons=(OrbitalElectron(spin),),
        )

    @classmethod
    def double(cls, orbital: ElectronOrbital) -> "OrbitalOccupancy":
        if not isinstance(orbital, ElectronOrbital):
            raise TypeError("orbital must be an ElectronOrbital")

        if orbital.electron_count != 2:
            raise ValueError(
                "double occupancy requires orbital.electron_count == 2"
            )

        return cls(
            orbital=orbital,
            electrons=(
                OrbitalElectron(ElectronSpin.UP),
                OrbitalElectron(ElectronSpin.DOWN),
            ),
        )

    @property
    def electron_count(self) -> int:
        return len(self.electrons)

    @property
    def is_empty(self) -> bool:
        return self.electron_count == 0

    @property
    def is_singly_occupied(self) -> bool:
        return self.electron_count == 1

    @property
    def is_doubly_occupied(self) -> bool:
        return self.electron_count == 2

    @property
    def spins(self) -> tuple[ElectronSpin, ...]:
        return tuple(
            electron.spin
            for electron in self.electrons
        )


@dataclass(frozen=True)
class SubshellOccupancy:
    """Explicit orbital-by-orbital occupancy of an atomic subshell."""

    principal_level: int
    subshell: str
    orbitals: tuple[OrbitalOccupancy, ...]

    def __post_init__(self) -> None:
        definition = define_subshell(
            self.principal_level,
            self.subshell,
        )

        if not isinstance(self.orbitals, tuple):
            raise TypeError("orbitals must be a tuple")

        if len(self.orbitals) != definition.orbital_count:
            raise ValueError(
                f"{definition.label} requires "
                f"{definition.orbital_count} orbitals"
            )

        magnetic_numbers = []

        for occupancy in self.orbitals:
            if not isinstance(occupancy, OrbitalOccupancy):
                raise TypeError(
                    "every item must be an OrbitalOccupancy"
                )

            orbital = occupancy.orbital

            if orbital.principal_level != definition.principal_level:
                raise ValueError(
                    "orbital principal level mismatch"
                )

            if orbital.subshell != definition.designation:
                raise ValueError(
                    "orbital subshell mismatch"
                )

            magnetic_numbers.append(
                orbital.magnetic_quantum_number
            )

        if tuple(magnetic_numbers) != definition.magnetic_quantum_numbers:
            raise ValueError(
                "orbitals must contain each magnetic quantum number "
                "exactly once in canonical order"
            )

        if not self.validate_pauli():
            raise ValueError(
                "occupancy violates the Pauli exclusion principle"
            )

    @property
    def definition(self) -> SubshellDefinition:
        return define_subshell(
            self.principal_level,
            self.subshell,
        )

    @classmethod
    def from_electron_count(
        cls,
        principal_level: int,
        subshell: str,
        electron_count: int,
        *,
        enforce_hund: bool = True,
    ) -> "SubshellOccupancy":
        definition = define_subshell(
            principal_level,
            subshell,
        )

        if (
            not isinstance(electron_count, int)
            or isinstance(electron_count, bool)
        ):
            raise TypeError(
                "electron_count must be an integer"
            )

        if not 0 <= electron_count <= definition.electron_capacity:
            raise ValueError(
                f"{definition.label} can contain "
                f"0 to {definition.electron_capacity} electrons"
            )

        orbitals = tuple(
            OrbitalOccupancy.empty(
                ElectronOrbital(
                    principal_level=definition.principal_level,
                    subshell=definition.designation,
                    magnetic_quantum_number=m,
                    electron_count=0,
                )
            )
            for m in definition.magnetic_quantum_numbers
        )

        remaining = electron_count

        if enforce_hund:
            for index in range(definition.orbital_count):
                if remaining <= 0:
                    break

                orbital = orbitals[index].orbital

                orbitals = (
                    orbitals[:index]
                    + (
                        OrbitalOccupancy.single(
                            ElectronOrbital(
                                principal_level=orbital.principal_level,
                                subshell=orbital.subshell,
                                magnetic_quantum_number=(
                                    orbital.magnetic_quantum_number
                                ),
                                electron_count=1,
                            )
                        ),
                    )
                    + orbitals[index + 1:]
                )

                remaining -= 1

            for index in range(definition.orbital_count):
                if remaining <= 0:
                    break

                orbital = orbitals[index].orbital

                orbitals = (
                    orbitals[:index]
                    + (
                        OrbitalOccupancy.double(
                            ElectronOrbital(
                                principal_level=orbital.principal_level,
                                subshell=orbital.subshell,
                                magnetic_quantum_number=(
                                    orbital.magnetic_quantum_number
                                ),
                                electron_count=2,
                            )
                        ),
                    )
                    + orbitals[index + 1:]
                )

                remaining -= 1

        else:
            for index in range(definition.orbital_count):
                if remaining <= 0:
                    break

                amount = min(2, remaining)
                orbital = orbitals[index].orbital

                if amount == 1:
                    replacement = OrbitalOccupancy.single(
                        ElectronOrbital(
                            principal_level=orbital.principal_level,
                            subshell=orbital.subshell,
                            magnetic_quantum_number=(
                                orbital.magnetic_quantum_number
                            ),
                            electron_count=1,
                        )
                    )
                else:
                    replacement = OrbitalOccupancy.double(
                        ElectronOrbital(
                            principal_level=orbital.principal_level,
                            subshell=orbital.subshell,
                            magnetic_quantum_number=(
                                orbital.magnetic_quantum_number
                            ),
                            electron_count=2,
                        )
                    )

                orbitals = (
                    orbitals[:index]
                    + (replacement,)
                    + orbitals[index + 1:]
                )

                remaining -= amount

        return cls(
            principal_level=definition.principal_level,
            subshell=definition.designation,
            orbitals=orbitals,
        )

    @property
    def electron_count(self) -> int:
        return sum(
            orbital.electron_count
            for orbital in self.orbitals
        )

    @property
    def orbital_count(self) -> int:
        return self.definition.orbital_count

    @property
    def capacity(self) -> int:
        return self.definition.electron_capacity

    @property
    def unpaired_electron_count(self) -> int:
        return sum(
            1
            for orbital in self.orbitals
            if orbital.is_singly_occupied
        )

    @property
    def spin_multiplicity(self) -> int:
        return self.unpaired_electron_count + 1

    def validate_pauli(self) -> bool:
        for orbital in self.orbitals:
            if orbital.electron_count > 2:
                return False

            if orbital.electron_count == 2:
                if len(set(orbital.spins)) != 2:
                    return False

        return True

    def validate_hund(self) -> bool:
        """
        Return whether the occupancy is compatible with Hund's rule.

        Degenerate orbitals are singly occupied with parallel spins before
        additional electrons pair.
        """
        electron_count = self.electron_count
        orbital_count = self.orbital_count

        if electron_count == 0:
            return True

        singly_occupied = sum(
            1
            for orbital in self.orbitals
            if orbital.is_singly_occupied
        )

        doubly_occupied = sum(
            1
            for orbital in self.orbitals
            if orbital.is_doubly_occupied
        )

        empty = sum(
            1
            for orbital in self.orbitals
            if orbital.is_empty
        )

        expected_doubly_occupied = max(
            0,
            electron_count - orbital_count,
        )

        expected_singly_occupied = min(
            electron_count,
            2 * orbital_count - electron_count,
        )

        expected_empty = max(
            0,
            orbital_count - electron_count,
        )

        if doubly_occupied != expected_doubly_occupied:
            return False

        if singly_occupied != expected_singly_occupied:
            return False

        if empty != expected_empty:
            return False

        singly_spins = [
            orbital.spins[0]
            for orbital in self.orbitals
            if orbital.is_singly_occupied
        ]

        return len(set(singly_spins)) <= 1

    @property
    def is_hund_ground_state(self) -> bool:
        return self.validate_hund()

    @property
    def notation(self) -> str:
        return (
            f"{self.principal_level}"
            f"{self.subshell}"
            f"{self.electron_count}"
        )


__all__ = [
    "OrbitalOccupancy",
    "SubshellOccupancy",
]
