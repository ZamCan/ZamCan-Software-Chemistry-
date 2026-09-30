from __future__ import annotations

from .base import ChemicalIdentity, ChemicalName, NameType


class NomenclatureEngine:
    name = "nomenclature"

    def identify(
        self,
        formula: str,
        names: tuple[ChemicalName, ...] = (),
    ) -> ChemicalIdentity:
        return ChemicalIdentity(
            formula=formula,
            names=names,
        )

    def names(
        self,
        identity: ChemicalIdentity,
    ) -> tuple[ChemicalName, ...]:
        return identity.names

    def preferred_name(
        self,
        identity: ChemicalIdentity,
    ) -> ChemicalName | None:
        return identity.preferred_name()


nomenclature_engine = NomenclatureEngine()
