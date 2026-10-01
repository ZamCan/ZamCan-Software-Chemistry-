from __future__ import annotations

from dataclasses import dataclass

from scm.matter.species import ChemicalSpecies

from .types import BondComponent, BondOrder, BondType


@dataclass(frozen=True)
class Bond:
    """
    Structural relationship between two chemical species.

    A Bond records a structural relationship only. It does not by itself
    claim that the relationship is physically stable, energetically favorable,
    or experimentally observed.
    """

    first: ChemicalSpecies
    second: ChemicalSpecies
    order: BondOrder = BondOrder.SINGLE
    bond_type: BondType = BondType.COVALENT
    components: tuple[BondComponent, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.first, ChemicalSpecies):
            raise TypeError("first must be a ChemicalSpecies")

        if not isinstance(self.second, ChemicalSpecies):
            raise TypeError("second must be a ChemicalSpecies")

        if self.first is self.second:
            raise ValueError("a bond cannot connect a species instance to itself")

        if not isinstance(self.order, BondOrder):
            try:
                object.__setattr__(self, "order", BondOrder(self.order))
            except ValueError as exc:
                raise ValueError(f"invalid bond order: {self.order!r}") from exc

        if not isinstance(self.components, tuple):
            object.__setattr__(self, "components", tuple(self.components))
        normalized_components: list[BondComponent] = []
        for component in self.components:
            if not isinstance(component, BondComponent):
                component = BondComponent(component)
            if component not in normalized_components:
                normalized_components.append(component)
        object.__setattr__(self, "components", tuple(normalized_components))

        if not isinstance(self.bond_type, BondType):
            try:
                object.__setattr__(self, "bond_type", BondType(self.bond_type))
            except ValueError as exc:
                raise ValueError(
                    f"invalid bond type: {self.bond_type!r}"
                ) from exc

    @property
    def component_count(self) -> int:
        return len(self.components)

    @property
    def sigma_count(self) -> int:
        return int(BondComponent.SIGMA in self.components)

    @property
    def pi_count(self) -> int:
        return int(BondComponent.PI in self.components) + int(BondComponent.DELOCALIZED_PI in self.components)

    @property
    def endpoints(self) -> tuple[ChemicalSpecies, ChemicalSpecies]:
        return self.first, self.second

    @property
    def is_covalent(self) -> bool:
        return self.bond_type is BondType.COVALENT

    @property
    def is_coordinate(self) -> bool:
        return self.bond_type is BondType.COORDINATE

    @property
    def is_ionic(self) -> bool:
        return self.bond_type is BondType.IONIC

    @property
    def is_aromatic(self) -> bool:
        return self.order is BondOrder.AROMATIC

    @property
    def is_intramolecular(self) -> bool:
        """Whether this is represented as a primary chemical bond.

        Hydrogen bonding and van der Waals attraction are modeled as
        intermolecular/secondary interactions by default.
        """
        return self.bond_type not in {
            BondType.HYDROGEN,
            BondType.VAN_DER_WAALS,
        }

    @property
    def is_primary_bond(self) -> bool:
        return self.bond_type in {
            BondType.COVALENT,
            BondType.IONIC,
            BondType.METALLIC,
            BondType.COORDINATE,
        }

    @property
    def order_value(self) -> float | None:
        values = {
            BondOrder.SINGLE: 1.0,
            BondOrder.DOUBLE: 2.0,
            BondOrder.TRIPLE: 3.0,
            BondOrder.QUADRUPLE: 4.0,
            BondOrder.AROMATIC: 1.5,
            BondOrder.PARTIAL: 0.5,
        }
        return values.get(self.order)

    def connects(self, species: ChemicalSpecies) -> bool:
        return species is self.first or species is self.second

    def other(self, species: ChemicalSpecies) -> ChemicalSpecies:
        if species is self.first:
            return self.second
        if species is self.second:
            return self.first
        raise ValueError("species is not an endpoint of this bond")

    def reversed(self) -> Bond:
        return Bond(
            first=self.second,
            second=self.first,
            order=self.order,
            bond_type=self.bond_type,
            components=self.components,
        )
