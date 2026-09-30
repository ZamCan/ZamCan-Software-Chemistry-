from __future__ import annotations

from dataclasses import dataclass

from scm.core import Conditions, Phase
from scm.matter.states import ChemicalState


@dataclass(frozen=True)
class ResolvedState:
    """
    Read-only resolved view of a ChemicalState.

    This does not create a second chemical-state model.
    It provides the chemistry engine with a convenient,
    normalized view of the existing SCM ChemicalState.
    """

    state: ChemicalState
    species: tuple
    phase: Phase
    conditions: Conditions | None
    total_moles: float
    element_counts: dict[str, int]

    @property
    def component_count(self) -> int:
        return self.state.component_count

    def contains_species(self, species) -> bool:
        return any(candidate is species for candidate in self.species)

    def moles_of(self, species) -> float:
        for component in self.state.components:
            if component.species is species:
                return component.moles
        return 0.0


class StateResolver:
    """
    Resolve a ChemicalState into information required by
    chemistry reasoning modules.

    The resolver is intentionally conservative:
    it reads existing SCM structures and does not invent
    chemical properties or reaction outcomes.
    """

    @staticmethod
    def resolve(state: ChemicalState) -> ResolvedState:
        if not isinstance(state, ChemicalState):
            raise TypeError("state must be a ChemicalState")

        element_counts: dict[str, int] = {}

        for component in state.components:
            for symbol, count in component.species.element_counts.items():
                element_counts[symbol] = element_counts.get(symbol, 0) + count

        return ResolvedState(
            state=state,
            species=state.species,
            phase=state.phase,
            conditions=state.conditions,
            total_moles=state.total_moles,
            element_counts=dict(sorted(element_counts.items())),
        )
