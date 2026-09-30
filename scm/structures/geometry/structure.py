from __future__ import annotations

from dataclasses import dataclass

from scm.matter.species import ChemicalSpecies
from scm.structures.molecules import Molecule

from .vector import Vector3D


@dataclass(frozen=True)
class MolecularGeometry:
    """
    Spatial representation of a molecule.

    Geometry assigns Cartesian positions to the exact species instances
    already present in a Molecule.

    It does not predict geometry, optimize coordinates, or determine
    equilibrium structure.
    """

    molecule: Molecule
    positions: tuple[tuple[ChemicalSpecies, Vector3D], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.molecule, Molecule):
            raise TypeError("molecule must be a Molecule")

        positions = tuple(self.positions)

        seen: list[ChemicalSpecies] = []

        for species, position in positions:
            if not isinstance(species, ChemicalSpecies):
                raise TypeError(
                    "position species must be a ChemicalSpecies"
                )

            if not isinstance(position, Vector3D):
                raise TypeError(
                    "position must be a Vector3D"
                )

            if not self.molecule.contains(species):
                raise ValueError(
                    "position species must belong to the molecule"
                )

            if any(existing is species for existing in seen):
                raise ValueError(
                    "a species instance may have only one position"
                )

            seen.append(species)

        if len(positions) != self.molecule.atom_count:
            raise ValueError(
                "every molecule species must have exactly one position"
            )

        for species in self.molecule.species:
            if not any(item is species for item, _ in positions):
                raise ValueError(
                    "every molecule species must have a position"
                )

        object.__setattr__(self, "positions", positions)

    def position_of(self, species: ChemicalSpecies) -> Vector3D:
        for item, position in self.positions:
            if item is species:
                return position

        raise ValueError(
            "species does not have a position in this geometry"
        )

    def contains(self, species: ChemicalSpecies) -> bool:
        return any(item is species for item, _ in self.positions)

    @property
    def dimensionality(self) -> int:
        """
        Return the number of spatial axes represented.

        Geometry v1 uses Cartesian x/y/z coordinates, therefore this is 3.
        """
        return 3
