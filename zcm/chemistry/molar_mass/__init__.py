from __future__ import annotations

from scm.chemistry.quantities.molar_mass import MolarMassCalculator
from scm.chemistry.reactions import parse_formula
from scm.matter.composition import Composition
from scm.matter.species import ChemicalSpecies
from scm.chemistry.engine import ChemistryModule


class MolarMassWorkspace(ChemistryModule):
    name = "molar_mass"

    def capabilities(self) -> frozenset[str]:
        return frozenset({"molar_mass", "composition_molar_mass"})

    def calculate(self, formula: str):
        if not isinstance(formula, str):
            raise TypeError("formula must be a string")

        counts = parse_formula(formula)
        species = ChemicalSpecies(
            composition=Composition.from_mapping(counts),
        )
        return MolarMassCalculator().calculate(species)


molar_mass_workspace = MolarMassWorkspace()

__all__ = ["MolarMassWorkspace", "molar_mass_workspace"]
