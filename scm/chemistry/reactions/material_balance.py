from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from scm.core import Quantity
from scm.matter.species import ChemicalSpecies
from scm.matter.states import ChemicalState

from .extent import ReactionExtentCalculator
from .stoichiometry import ReactionStoichiometry


class MaterialRole(str, Enum):
    """Role of a species in a reaction material balance."""

    REACTANT = "reactant"
    PRODUCT = "product"


@dataclass(frozen=True)
class SpeciesMaterialBalance:
    """Material accounting for one species at a selected reaction extent."""

    species: ChemicalSpecies
    role: MaterialRole
    initial_amount: Quantity
    change: Quantity
    final_amount: Quantity

    def __post_init__(self) -> None:
        if not isinstance(self.species, ChemicalSpecies):
            raise TypeError("species must be a ChemicalSpecies")

        if not isinstance(self.role, MaterialRole):
            raise TypeError("role must be a MaterialRole")

        for name, value in (
            ("initial_amount", self.initial_amount),
            ("change", self.change),
            ("final_amount", self.final_amount),
        ):
            if not isinstance(value, Quantity):
                raise TypeError(f"{name} must be a Quantity")

            if value.dimension != Quantity(1.0, "mol").dimension:
                raise ValueError(
                    f"{name} must have amount-of-substance dimension"
                )

        initial_moles = self.initial_amount.to("mol").value
        change_moles = self.change.to("mol").value
        final_moles = self.final_amount.to("mol").value

        expected_final = initial_moles + change_moles

        tolerance = max(
            1e-12,
            abs(expected_final) * 1e-12,
        )

        if abs(final_moles - expected_final) > tolerance:
            raise ValueError(
                "final_amount must equal initial_amount + change"
            )

        if initial_moles < -tolerance:
            raise ValueError(
                "initial_amount cannot be negative"
            )

        if final_moles < -tolerance:
            raise ValueError(
                "final_amount cannot be negative"
            )

    @property
    def initial_moles(self) -> float:
        return self.initial_amount.to("mol").value

    @property
    def change_moles(self) -> float:
        return self.change.to("mol").value

    @property
    def final_moles(self) -> float:
        return max(0.0, self.final_amount.to("mol").value)

    @property
    def consumed(self) -> bool:
        return self.change_moles < 0

    @property
    def generated(self) -> bool:
        return self.change_moles > 0

    @property
    def unchanged(self) -> bool:
        return self.change_moles == 0


@dataclass(frozen=True)
class ReactionMaterialBalance:
    """Complete mole-based material accounting for a reaction extent.

    This represents stoichiometric material accounting only.

    It does not establish:
    - whether the reaction actually occurs,
    - reaction rate,
    - equilibrium,
    - thermodynamic feasibility,
    - kinetic feasibility,
    - phase transfer,
    - material losses,
    - gas escape,
    - dissolution,
    - measurement uncertainty,
    - competing reactions.
    """

    reaction: ReactionStoichiometry
    initial_state: ChemicalState
    extent: Quantity
    species_balances: tuple[SpeciesMaterialBalance, ...]
    limiting_species: ChemicalSpecies | None = None

    def __post_init__(self) -> None:
        if not isinstance(
            self.reaction,
            ReactionStoichiometry,
        ):
            raise TypeError(
                "reaction must be a ReactionStoichiometry"
            )

        if not isinstance(
            self.initial_state,
            ChemicalState,
        ):
            raise TypeError(
                "initial_state must be a ChemicalState"
            )

        if not isinstance(self.extent, Quantity):
            raise TypeError("extent must be a Quantity")

        if self.extent.dimension != Quantity(1.0, "mol").dimension:
            raise ValueError(
                "extent must have amount-of-substance dimension"
            )

        if self.extent.value < 0:
            raise ValueError("extent cannot be negative")

        if not isinstance(self.species_balances, tuple):
            raise TypeError(
                "species_balances must be a tuple"
            )

        if not all(
            isinstance(balance, SpeciesMaterialBalance)
            for balance in self.species_balances
        ):
            raise TypeError(
                "all species balances must be "
                "SpeciesMaterialBalance instances"
            )

        if self.limiting_species is not None:
            if not isinstance(
                self.limiting_species,
                ChemicalSpecies,
            ):
                raise TypeError(
                    "limiting_species must be a ChemicalSpecies"
                )

    def balance_for(
        self,
        species: ChemicalSpecies,
    ) -> SpeciesMaterialBalance:
        if not isinstance(species, ChemicalSpecies):
            raise TypeError(
                "species must be a ChemicalSpecies"
            )

        for balance in self.species_balances:
            if balance.species == species:
                return balance

        raise KeyError(
            "species is not part of this material balance"
        )

    @property
    def consumed_species(
        self,
    ) -> tuple[SpeciesMaterialBalance, ...]:
        return tuple(
            balance
            for balance in self.species_balances
            if balance.consumed
        )

    @property
    def generated_species(
        self,
    ) -> tuple[SpeciesMaterialBalance, ...]:
        return tuple(
            balance
            for balance in self.species_balances
            if balance.generated
        )

    @property
    def remaining_species(
        self,
    ) -> tuple[SpeciesMaterialBalance, ...]:
        return tuple(
            balance
            for balance in self.species_balances
            if balance.final_moles > 0
        )


class ReactionMaterialBalanceCalculator:
    """Build material accounting from an initial chemical state.

    The calculator combines:
        ChemicalState
        + ReactionStoichiometry
        + selected reaction extent

    It performs mole accounting only.
    """

    name = "reaction_material_balance"

    def __init__(
        self,
        extent_calculator: ReactionExtentCalculator | None = None,
    ) -> None:
        self.extent_calculator = (
            extent_calculator
            if extent_calculator is not None
            else ReactionExtentCalculator()
        )

    def calculate(
        self,
        reaction: ReactionStoichiometry,
        state: ChemicalState,
        extent: Quantity | None = None,
    ) -> ReactionMaterialBalance:
        if not isinstance(
            reaction,
            ReactionStoichiometry,
        ):
            raise TypeError(
                "reaction must be a ReactionStoichiometry"
            )

        if not isinstance(state, ChemicalState):
            raise TypeError(
                "state must be a ChemicalState"
            )

        if extent is None:
            extent_limit = self.extent_calculator.maximum_extent(
                reaction,
                state,
            )
            extent = extent_limit.extent
            limiting_species = extent_limit.limiting_species
        else:
            if not isinstance(extent, Quantity):
                raise TypeError(
                    "extent must be a Quantity"
                )

            if extent.dimension != Quantity(
                1.0,
                "mol",
            ).dimension:
                raise ValueError(
                    "extent must have amount-of-substance dimension"
                )

            if extent.value < 0:
                raise ValueError(
                    "extent cannot be negative"
                )

            maximum = self.extent_calculator.maximum_extent(
                reaction,
                state,
            )

            if extent.to("mol").value > (
                maximum.extent.to("mol").value
            ):
                raise ValueError(
                    "selected extent exceeds the "
                    "stoichiometrically available extent"
                )

            limiting_species = maximum.limiting_species

        extent_moles = extent.to("mol").value

        changes = self.extent_calculator.changes_at_extent(
            reaction,
            extent,
        )

        change_by_species = {
            change.species: change
            for change in changes
        }

        balances: list[SpeciesMaterialBalance] = []

        for term in reaction.reactants:
            initial_moles = self._moles_of(
                state,
                term.species,
            )

            change = change_by_species[term.species].change
            change_moles = change.to("mol").value

            final_moles = initial_moles + change_moles

            if final_moles < -1e-12:
                raise ValueError(
                    "reaction extent produces a negative "
                    "amount for a reactant"
                )

            balances.append(
                SpeciesMaterialBalance(
                    species=term.species,
                    role=MaterialRole.REACTANT,
                    initial_amount=Quantity(
                        initial_moles,
                        "mol",
                    ),
                    change=change,
                    final_amount=Quantity(
                        max(0.0, final_moles),
                        "mol",
                    ),
                )
            )

        for term in reaction.products:
            initial_moles = self._moles_of(
                state,
                term.species,
            )

            change = change_by_species[term.species].change
            final_moles = initial_moles + change.to(
                "mol"
            ).value

            balances.append(
                SpeciesMaterialBalance(
                    species=term.species,
                    role=MaterialRole.PRODUCT,
                    initial_amount=Quantity(
                        initial_moles,
                        "mol",
                    ),
                    change=change,
                    final_amount=Quantity(
                        final_moles,
                        "mol",
                    ),
                )
            )

        return ReactionMaterialBalance(
            reaction=reaction,
            initial_state=state,
            extent=extent,
            species_balances=tuple(balances),
            limiting_species=limiting_species,
        )

    @staticmethod
    def _moles_of(
        state: ChemicalState,
        species: ChemicalSpecies,
    ) -> float:
        total = 0.0

        for component in state.components:
            if component.species == species:
                total += component.moles

        return total


reaction_material_balance_calculator = (
    ReactionMaterialBalanceCalculator()
)
