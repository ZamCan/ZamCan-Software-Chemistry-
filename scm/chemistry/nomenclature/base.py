from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class NameType(str, Enum):
    SYSTEMATIC = "systematic"
    IUPAC = "iupac"
    COMMON = "common"
    TRADITIONAL = "traditional"
    INDUSTRIAL = "industrial"
    HISTORICAL = "historical"
    OTHER = "other"


@dataclass(frozen=True)
class ChemicalName:
    name: str
    name_type: NameType
    language: str = "en"
    preferred: bool = False
    source: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("chemical name must not be empty")

        if not isinstance(self.name_type, NameType):
            raise TypeError("name_type must be a NameType")

        if not isinstance(self.language, str) or not self.language.strip():
            raise ValueError("language must not be empty")


@dataclass(frozen=True)
class ChemicalIdentity:
    formula: str
    names: tuple[ChemicalName, ...] = ()
    identity_key: Any | None = None
    source: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.formula, str) or not self.formula.strip():
            raise ValueError("formula must not be empty")

        if self.identity_key is None:
            raise ValueError("identity_key must be provided")
        
        for name in self.names:
            if not isinstance(name, ChemicalName):
                raise TypeError(
                    "names must contain ChemicalName instances"
                )

    def names_of_type(
        self,
        name_type: NameType,
    ) -> tuple[ChemicalName, ...]:
        return tuple(
            name
            for name in self.names
            if name.name_type is name_type
        )

    def preferred_name(self) -> ChemicalName | None:
        for name in self.names:
            if name.preferred:
                return name

        return self.names[0] if self.names else None
