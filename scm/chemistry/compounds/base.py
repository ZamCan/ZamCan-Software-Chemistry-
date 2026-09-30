from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Compound:
    formula: str
    name: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.formula, str) or not self.formula.strip():
            raise ValueError("compound formula must not be empty")

        if self.name is not None:
            if not isinstance(self.name, str) or not self.name.strip():
                raise ValueError("compound name must not be empty when provided")

    def __str__(self) -> str:
        if self.name:
            return f"{self.name} ({self.formula})"

        return self.formula
