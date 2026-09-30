from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class NuclearStateType(str, Enum):
    GROUND = "ground"
    EXCITED = "excited"
    ISOMERIC = "isomeric"


@dataclass(frozen=True)
class NuclearState:
    """
    State of a nuclide's nucleus.

    The state is distinct from isotope identity.
    A nuclide may have a ground state and one or more
    excited or metastable/isomeric states.
    """

    state_type: NuclearStateType
    excitation_energy: float | None = None
    excitation_energy_unit: str | None = None
    label: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.state_type, NuclearStateType):
            raise TypeError(
                "state_type must be a NuclearStateType"
            )

        if self.excitation_energy is not None:
            if self.excitation_energy < 0:
                raise ValueError(
                    "excitation_energy cannot be negative"
                )

        if (
            self.excitation_energy is not None
            and not self.excitation_energy_unit
        ):
            raise ValueError(
                "excitation_energy_unit is required when "
                "excitation_energy is provided"
            )

        if (
            self.state_type is NuclearStateType.GROUND
            and self.excitation_energy is not None
            and self.excitation_energy != 0
        ):
            raise ValueError(
                "ground state excitation energy must be zero"
            )
