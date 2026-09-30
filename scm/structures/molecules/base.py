from __future__ import annotations

from dataclasses import dataclass

from scm.matter.species import ChemicalSpecies
from scm.structures.connectivity import Connectivity


@dataclass(frozen=True)
class Molecule:
    """
    Molecular structure composed of chemical-species instances
    connected through a Connectivity graph.

    This layer represents molecular composition and structural
    connectivity. It does not yet determine geometry, stability,
    reactivity, nomenclature, or electronic wavefunctions.
    """

    species: tuple[ChemicalSpecies, ...]
    connectivity: Connectivity
    charge: int = 0

    def __post_init__(self) -> None:
        species = tuple(self.species)

        for item in species:
            if not isinstance(item, ChemicalSpecies):
                raise TypeError("every molecule species must be a ChemicalSpecies")

        if not isinstance(self.connectivity, Connectivity):
            raise TypeError("connectivity must be a Connectivity")

        if not isinstance(self.charge, int) or isinstance(self.charge, bool):
            raise TypeError("charge must be an integer")

        if len(species) == 0:
            raise ValueError("molecule must contain at least one species")

        if len(species) != len(self.connectivity.nodes):
            raise ValueError(
                "molecule species and connectivity nodes must have the same size"
            )

        for item in species:
            if not any(node is item for node in self.connectivity.nodes):
                raise ValueError(
                    "every molecule species must be present in connectivity"
                )

        for node in self.connectivity.nodes:
            if not any(item is node for item in species):
                raise ValueError(
                    "every connectivity node must be present in molecule species"
                )

        calculated_charge = sum(item.charge_number for item in species)

        if self.charge != calculated_charge:
            raise ValueError(
                "molecule charge does not match the sum of species charges"
            )

        object.__setattr__(self, "species", species)

    @property
    def atom_count(self) -> int:
        return len(self.species)

    @property
    def formula_counts(self) -> dict[str, int]:
        """
        Return elemental composition derived from the actual species.

        The result is calculated through the public ChemicalSpecies
        element_counts interface.
        """
        counts: dict[str, int] = {}

        for item in self.species:
            for symbol, count in item.element_counts.items():
                counts[symbol] = counts.get(symbol, 0) + count

        return dict(sorted(counts.items()))

    @property
    def formula(self) -> str:
        parts: list[str] = []

        for symbol, count in self.formula_counts.items():
            parts.append(symbol)
            if count != 1:
                parts.append(str(count))

        return "".join(parts)

    def contains(self, species: ChemicalSpecies) -> bool:
        return any(item is species for item in self.species)

    def count(self, species: ChemicalSpecies) -> int:
        return sum(item is species for item in self.species)

    def neighbors(
        self,
        species: ChemicalSpecies,
    ) -> tuple[ChemicalSpecies, ...]:
        return self.connectivity.neighbors(species)

    def bonds_for(self, species: ChemicalSpecies):
        return self.connectivity.bonds_for(species)

    @property
    def connected(self) -> bool:
        return self.connectivity.is_connected

    @property
    def component_count(self) -> int:
        return self.connectivity.component_count

    @property
    def net_charge(self) -> int:
        return self.charge
