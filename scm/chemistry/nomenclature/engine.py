from __future__ import annotations

from .base import ChemicalIdentity, ChemicalName, NameType
from scm.chemistry.formulas import parse_formula
from scm.chemistry.identity_key import identity_key
from scm.matter.composition import Composition
from scm.matter.species import ChemicalSpecies


class NomenclatureEngine:
    name = "nomenclature"

    def identify(
        self,
        formula: str,
        names: tuple[ChemicalName, ...] = (),
    ) -> ChemicalIdentity:
        parsed = parse_formula(formula)
        composition = Composition.from_mapping(
            {
                component.element: component.count
                for component in parsed.components
            }
        )
        species = ChemicalSpecies(composition=composition)
        return ChemicalIdentity(
            formula=str(composition),
            names=names,
            identity_key=identity_key(species),
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
