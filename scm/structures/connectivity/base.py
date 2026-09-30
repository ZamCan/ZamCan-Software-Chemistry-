from __future__ import annotations

from dataclasses import dataclass

from scm.matter.species import ChemicalSpecies
from scm.structures.bonds import Bond


@dataclass(frozen=True)
class Connectivity:
    """
    Structural graph of chemical-species instances connected by bonds.

    Connectivity describes which species are structurally connected.
    It does not by itself determine molecular identity, geometry,
    stability, bonding energetics, or chemical reactivity.
    """

    nodes: tuple[ChemicalSpecies, ...] = ()
    bonds: tuple[Bond, ...] = ()

    def __post_init__(self) -> None:
        nodes = tuple(self.nodes)
        bonds = tuple(self.bonds)

        for node in nodes:
            if not isinstance(node, ChemicalSpecies):
                raise TypeError("every node must be a ChemicalSpecies")

        for bond in bonds:
            if not isinstance(bond, Bond):
                raise TypeError("every bond must be a Bond")

            if not self._contains_identity(nodes, bond.first):
                raise ValueError("bond endpoint is not present in nodes")

            if not self._contains_identity(nodes, bond.second):
                raise ValueError("bond endpoint is not present in nodes")

        for i, first in enumerate(nodes):
            for second in nodes[i + 1:]:
                if first is second:
                    raise ValueError("duplicate node instance")

        for i, first in enumerate(bonds):
            for second in bonds[i + 1:]:
                if (
                    first.first is second.first
                    and first.second is second.second
                    or
                    first.first is second.second
                    and first.second is second.first
                ):
                    raise ValueError("duplicate bond between the same endpoints")

        object.__setattr__(self, "nodes", nodes)
        object.__setattr__(self, "bonds", bonds)

    @staticmethod
    def _contains_identity(
        nodes: tuple[ChemicalSpecies, ...],
        target: ChemicalSpecies,
    ) -> bool:
        return any(node is target for node in nodes)

    def contains(self, species: ChemicalSpecies) -> bool:
        """Return whether this exact species instance is a node."""
        return self._contains_identity(self.nodes, species)

    def neighbors(
        self,
        species: ChemicalSpecies,
    ) -> tuple[ChemicalSpecies, ...]:
        """Return directly bonded species instances."""
        if not self.contains(species):
            raise ValueError("species is not a node in this connectivity graph")

        result: list[ChemicalSpecies] = []

        for bond in self.bonds:
            if bond.first is species:
                result.append(bond.second)
            elif bond.second is species:
                result.append(bond.first)

        return tuple(result)

    def bonds_for(
        self,
        species: ChemicalSpecies,
    ) -> tuple[Bond, ...]:
        """Return all bonds attached to a species instance."""
        if not self.contains(species):
            raise ValueError("species is not a node in this connectivity graph")

        return tuple(
            bond
            for bond in self.bonds
            if bond.first is species or bond.second is species
        )

    def degree(self, species: ChemicalSpecies) -> int:
        """Return the number of directly connected neighbors."""
        return len(self.neighbors(species))

    def connected_components(
        self,
    ) -> tuple[tuple[ChemicalSpecies, ...], ...]:
        """
        Return connected components using graph traversal.

        Components preserve the node ordering supplied to this object.
        """
        remaining = list(self.nodes)
        components: list[tuple[ChemicalSpecies, ...]] = []

        while remaining:
            start = remaining.pop(0)
            component: list[ChemicalSpecies] = [start]
            queue: list[ChemicalSpecies] = [start]

            while queue:
                current = queue.pop(0)

                for neighbor in self.neighbors(current):
                    if any(neighbor is item for item in component):
                        continue

                    component.append(neighbor)

                    remaining = [
                        item
                        for item in remaining
                        if item is not neighbor
                    ]

                    queue.append(neighbor)

            components.append(tuple(component))

        return tuple(components)

    @property
    def component_count(self) -> int:
        return len(self.connected_components())

    @property
    def is_connected(self) -> bool:
        return bool(self.nodes) and self.component_count == 1

    def add_node(self, species: ChemicalSpecies) -> Connectivity:
        """Return a new graph containing the additional node instance."""
        if not isinstance(species, ChemicalSpecies):
            raise TypeError("species must be a ChemicalSpecies")

        if self.contains(species):
            raise ValueError("species instance is already present")

        return Connectivity(
            nodes=self.nodes + (species,),
            bonds=self.bonds,
        )

    def add_bond(self, bond: Bond) -> Connectivity:
        """Return a new graph containing the additional bond."""
        if not isinstance(bond, Bond):
            raise TypeError("bond must be a Bond")

        if not self.contains(bond.first):
            raise ValueError("first bond endpoint is not present")

        if not self.contains(bond.second):
            raise ValueError("second bond endpoint is not present")

        return Connectivity(
            nodes=self.nodes,
            bonds=self.bonds + (bond,),
        )
