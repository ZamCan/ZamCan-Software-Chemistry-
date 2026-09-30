from __future__ import annotations

from dataclasses import dataclass

from .subshell import define_subshell


@dataclass(frozen=True)
class ElectronShell:
    principal_level: int
    electron_count: int

    def __post_init__(self) -> None:
        if (
            not isinstance(self.principal_level, int)
            or isinstance(self.principal_level, bool)
        ):
            raise TypeError("principal_level must be an integer")

        if self.principal_level < 1:
            raise ValueError("principal_level must be at least 1")

        if (
            not isinstance(self.electron_count, int)
            or isinstance(self.electron_count, bool)
        ):
            raise TypeError("electron_count must be an integer")

        if self.electron_count < 0:
            raise ValueError("electron_count cannot be negative")


@dataclass(frozen=True)
class ElectronSubshell:
    principal_level: int
    subshell: str
    electron_count: int

    def __post_init__(self) -> None:
        definition = define_subshell(
            self.principal_level,
            self.subshell,
        )

        if (
            not isinstance(self.electron_count, int)
            or isinstance(self.electron_count, bool)
        ):
            raise TypeError("electron_count must be an integer")

        if self.electron_count < 0:
            raise ValueError("electron_count cannot be negative")

        if self.electron_count > definition.electron_capacity:
            raise ValueError(
                f"{definition.label} can contain at most "
                f"{definition.electron_capacity} electrons"
            )

        object.__setattr__(
            self,
            "subshell",
            definition.designation,
        )

    @property
    def definition(self):
        return define_subshell(
            self.principal_level,
            self.subshell,
        )

    @property
    def angular_momentum_quantum_number(self) -> int:
        return self.definition.angular_momentum_quantum_number

    @property
    def orbital_count(self) -> int:
        return self.definition.orbital_count

    @property
    def capacity(self) -> int:
        return self.definition.electron_capacity

    @property
    def orbitals(self):
        from .orbital import ElectronOrbital

        return tuple(
            ElectronOrbital(
                principal_level=self.principal_level,
                subshell=self.subshell,
                magnetic_quantum_number=m,
            )
            for m in self.definition.magnetic_quantum_numbers
        )

    @property
    def label(self) -> str:
        return self.definition.label


__all__ = [
    "ElectronShell",
    "ElectronSubshell",
]
