from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from scm.core import (
    Conditions,
    Evidence,
    Phase,
    ScientificProperty,
    ScientificStatus,
    Uncertainty,
    normalize_evidence,
)
from scm.matter.species import ChemicalSpecies

from .component import StateComponent


@dataclass(frozen=True)
class ChemicalState:
    """
    Scientific state of a chemical system.

    A ChemicalState represents one or more chemical species together
    with their amounts, phase classification, environmental conditions,
    scientific properties, evidence, uncertainty, and scientific status.

    Chemical identity is owned by ChemicalSpecies.
    Physical amount is owned by AmountOfSubstance through StateComponent.
    """

    components: tuple[StateComponent, ...]
    phase: Phase = Phase.UNKNOWN
    conditions: Conditions | None = None
    properties: tuple[ScientificProperty, ...] = ()
    evidence: Evidence | tuple[Evidence, ...] | None = None
    uncertainty: Uncertainty | None = None
    status: ScientificStatus = ScientificStatus.KNOWN

    def __post_init__(self) -> None:
        components = tuple(self.components)

        if not components:
            raise ValueError(
                "chemical state must contain at least one component"
            )

        if not all(
            isinstance(component, StateComponent)
            for component in components
        ):
            raise TypeError(
                "all state components must be StateComponent instances"
            )

        if not isinstance(self.phase, Phase):
            raise TypeError("phase must be a Phase")

        if self.conditions is not None and not isinstance(
            self.conditions,
            Conditions,
        ):
            raise TypeError(
                "conditions must be a Conditions instance or None"
            )

        properties = tuple(self.properties)

        if not all(
            isinstance(prop, ScientificProperty)
            for prop in properties
        ):
            raise TypeError(
                "all properties must be ScientificProperty instances"
            )

        normalized_evidence = normalize_evidence(self.evidence)

        if self.uncertainty is not None and not isinstance(
            self.uncertainty,
            Uncertainty,
        ):
            raise TypeError(
                "uncertainty must be an Uncertainty instance or None"
            )

        if not isinstance(self.status, ScientificStatus):
            raise TypeError(
                "status must be a ScientificStatus"
            )

        object.__setattr__(self, "components", components)
        object.__setattr__(self, "properties", properties)
        object.__setattr__(self, "evidence", normalized_evidence)

    @classmethod
    def from_components(
        cls,
        components: Iterable[StateComponent],
        **kwargs,
    ) -> "ChemicalState":
        """Construct a state from any iterable of StateComponent objects."""
        return cls(
            components=tuple(components),
            **kwargs,
        )

    @property
    def species(self) -> tuple[ChemicalSpecies, ...]:
        """Return the chemical species represented by this state."""
        return tuple(
            component.species
            for component in self.components
        )

    @property
    def component_count(self) -> int:
        return len(self.components)

    @property
    def total_moles(self) -> float:
        """Return the sum of all component amounts in mol."""
        return sum(
            component.moles
            for component in self.components
        )

    def contains(self, species: ChemicalSpecies) -> bool:
        """Return whether this state contains the exact species instance."""
        return any(
            component.species is species
            for component in self.components
        )

    def components_for(
        self,
        species: ChemicalSpecies,
    ) -> tuple[StateComponent, ...]:
        """Return components belonging to the exact species instance."""
        return tuple(
            component
            for component in self.components
            if component.species is species
        )

    def property(self, name: str) -> ScientificProperty | None:
        """Return the first property with the requested name."""
        if not isinstance(name, str):
            raise TypeError("name must be a string")

        target = name.strip()

        if not target:
            raise ValueError("name must not be empty")

        for prop in self.properties:
            if prop.name == target:
                return prop

        return None
