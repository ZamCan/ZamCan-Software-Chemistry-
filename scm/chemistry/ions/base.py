from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Ion:
    """
    Charged chemical species represented by its element identity
    and net charge.

    Positive charge means electrons have been removed.
    Negative charge means electrons have been added.
    """

    symbol: str
    charge_number: int

    def __post_init__(self) -> None:
        if not isinstance(self.symbol, str):
            raise TypeError("symbol must be a string")

        if not self.symbol.strip():
            raise ValueError("symbol must not be empty")

        if not isinstance(self.charge_number, int):
            raise TypeError("charge_number must be an integer")

    @property
    def charge_symbol(self) -> str:
        if self.charge_number == 0:
            return "0"

        if self.charge_number == 1:
            return "+"

        if self.charge_number == -1:
            return "-"

        return f"{self.charge_number:+d}"

    @property
    def electron_delta(self) -> int:
        """
        Change in electron count relative to the neutral atom.

        Positive values mean electrons were gained.
        Negative values mean electrons were lost.
        """
        return -self.charge_number

    def electron_count(self, atomic_number: int) -> int:
        if not isinstance(atomic_number, int):
            raise TypeError("atomic_number must be an integer")

        if atomic_number < 1:
            raise ValueError(
                "atomic_number must be at least 1"
            )

        count = atomic_number + self.electron_delta

        if count < 0:
            raise ValueError(
                "ion cannot have a negative electron count"
            )

        return count

    def __str__(self) -> str:
        return f"{self.symbol}{self.charge_symbol}"
