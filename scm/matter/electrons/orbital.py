from __future__ import annotations

from dataclasses import dataclass

from .subshell import define_subshell

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .spin import OrbitalElectron


@dataclass(frozen=True)
class ElectronOrbital:
    principal_level: int
    subshell: str
    magnetic_quantum_number: int
    electron_count: int = 0

    def __post_init__(self) -> None:
        definition = define_subshell(
            self.principal_level,
            self.subshell,
        )

        if (
            not isinstance(self.magnetic_quantum_number, int)
            or isinstance(self.magnetic_quantum_number, bool)
        ):
            raise TypeError(
                "magnetic_quantum_number must be an integer"
            )

        if (
            self.magnetic_quantum_number
            not in definition.magnetic_quantum_numbers
        ):
            raise ValueError(
                f"magnetic quantum number must be one of "
                f"{definition.magnetic_quantum_numbers}"
            )

        if (
            not isinstance(self.electron_count, int)
            or isinstance(self.electron_count, bool)
        ):
            raise TypeError("electron_count must be an integer")

        if not 0 <= self.electron_count <= 2:
            raise ValueError(
                "an orbital can contain 0 to 2 electrons"
            )

        object.__setattr__(
            self,
            "subshell",
            definition.designation,
        )

    @property
    def angular_momentum_quantum_number(self) -> int:
        return define_subshell(
            self.principal_level,
            self.subshell,
        ).angular_momentum_quantum_number

    @property
    def capacity(self) -> int:
        return 2

    @property
    def label(self) -> str:
        return (
            f"{self.principal_level}"
            f"{self.subshell}"
            f"(m={self.magnetic_quantum_number})"
        )

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
    def possible_spins(self) -> tuple[OrbitalElectron, ...]:
        from .spin import ElectronSpin, OrbitalElectron

        if self.electron_count == 0:
            return ()

        if self.electron_count == 1:
            return (
                OrbitalElectron(ElectronSpin.UP),
            )

        return (
            OrbitalElectron(ElectronSpin.UP),
            OrbitalElectron(ElectronSpin.DOWN),
        )


__all__ = ["ElectronOrbital"]
