from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SubshellDefinition:
    """Canonical quantum definition of an atomic subshell."""

    principal_level: int
    designation: str
    angular_momentum_quantum_number: int

    def __post_init__(self) -> None:
        if (
            not isinstance(self.principal_level, int)
            or isinstance(self.principal_level, bool)
        ):
            raise TypeError("principal_level must be an integer")

        if self.principal_level < 1:
            raise ValueError("principal_level must be at least 1")

        if not isinstance(self.designation, str):
            raise TypeError("designation must be a string")

        designation = self.designation.strip().lower()

        expected_l = {
            "s": 0,
            "p": 1,
            "d": 2,
            "f": 3,
        }

        if designation not in expected_l:
            raise ValueError("designation must be one of: s, p, d, f")

        l = self.angular_momentum_quantum_number

        if (
            not isinstance(l, int)
            or isinstance(l, bool)
        ):
            raise TypeError(
                "angular_momentum_quantum_number must be an integer"
            )

        if l != expected_l[designation]:
            raise ValueError(
                "angular momentum quantum number does not match "
                "subshell designation"
            )

        if l >= self.principal_level:
            raise ValueError(
                f"{self.principal_level}{designation} "
                "is not a valid atomic subshell"
            )

        object.__setattr__(self, "designation", designation)

    @property
    def label(self) -> str:
        return f"{self.principal_level}{self.designation}"

    @property
    def orbital_count(self) -> int:
        return 2 * self.angular_momentum_quantum_number + 1

    @property
    def electron_capacity(self) -> int:
        return 2 * self.orbital_count

    @property
    def magnetic_quantum_numbers(self) -> tuple[int, ...]:
        l = self.angular_momentum_quantum_number
        return tuple(range(-l, l + 1))


def define_subshell(
    principal_level: int,
    designation: str,
) -> SubshellDefinition:
    designation = designation.strip().lower()

    mapping = {
        "s": 0,
        "p": 1,
        "d": 2,
        "f": 3,
    }

    if designation not in mapping:
        raise ValueError("designation must be one of: s, p, d, f")

    return SubshellDefinition(
        principal_level=principal_level,
        designation=designation,
        angular_momentum_quantum_number=mapping[designation],
    )


__all__ = [
    "SubshellDefinition",
    "define_subshell",
]
