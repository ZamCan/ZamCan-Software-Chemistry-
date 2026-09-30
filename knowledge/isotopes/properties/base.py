from __future__ import annotations

from dataclasses import dataclass

from scm.core import (
    Conditions,
    Evidence,
    PropertyKind,
    ScientificProperty,
    ScientificStatus,
    Uncertainty,
    normalize_evidence,
)
from scm.core.quantity import Quantity
from scm.core.quantity_range import QuantityRange

from knowledge.isotopes.base import IsotopeRecord

from .identity import IsotopePropertyIdentity


PropertyQuantity = Quantity | QuantityRange


@dataclass(frozen=True)
class IsotopePropertyData:
    """
    Structured scientific property data associated with
    a specific isotope.

    This is the knowledge-layer representation used before
    conversion into an SCM ScientificProperty.

    Isotope identity is represented by (Z, A), while conditions
    and evidence remain separate so multiple scientific records
    can describe the same property.
    """

    isotope: IsotopeRecord
    kind: PropertyKind
    quantity: PropertyQuantity
    status: ScientificStatus
    conditions: Conditions | None = None
    uncertainty: Uncertainty | None = None
    evidence: Evidence | tuple[Evidence, ...] | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.isotope, IsotopeRecord):
            raise TypeError(
                "isotope must be an IsotopeRecord"
            )

        if not isinstance(
            self.kind,
            PropertyKind,
        ):
            raise TypeError(
                "kind must be a PropertyKind"
            )

        if not isinstance(
            self.quantity,
            (Quantity, QuantityRange),
        ):
            raise TypeError(
                "quantity must be a Quantity "
                "or QuantityRange"
            )

        if not isinstance(
            self.status,
            ScientificStatus,
        ):
            raise TypeError(
                "status must be a ScientificStatus"
            )

        if (
            self.conditions is not None
            and not isinstance(
                self.conditions,
                Conditions,
            )
        ):
            raise TypeError(
                "conditions must be a Conditions instance"
            )

        if (
            self.uncertainty is not None
            and not isinstance(
                self.uncertainty,
                Uncertainty,
            )
        ):
            raise TypeError(
                "uncertainty must be an Uncertainty instance"
            )

        normalized = normalize_evidence(
            self.evidence
        )

        object.__setattr__(
            self,
            "evidence",
            normalized,
        )

        if (
            self.notes is not None
            and not isinstance(
                self.notes,
                str,
            )
        ):
            raise TypeError(
                "notes must be a string or None"
            )

    @property
    def identity(self) -> IsotopePropertyIdentity:
        """
        Return the stable identity of this isotope property.
        """
        return IsotopePropertyIdentity(
            atomic_number=self.isotope.atomic_number,
            mass_number=self.isotope.mass_number,
            kind=self.kind,
        )

    @property
    def primary_evidence(self) -> Evidence | None:
        """
        Return the first evidence record, if one exists.
        """
        if not self.evidence:
            return None

        return self.evidence[0]

    def matches_conditions(
        self,
        requested: Conditions | None,
    ) -> bool:
        """
        Return whether this property record is compatible
        with requested conditions.

        Missing stored conditions are treated as unspecified,
        not contradictory.
        """

        if requested is None:
            return True

        if not isinstance(
            requested,
            Conditions,
        ):
            raise TypeError(
                "requested must be a Conditions instance "
                "or None"
            )

        if self.conditions is None:
            return True

        stored = self.conditions

        if (
            stored.temperature is not None
            and requested.temperature is not None
        ):
            if (
                stored.temperature.dimension
                != requested.temperature.dimension
            ):
                return False

            if (
                stored.temperature.to(
                    requested.temperature.unit
                ).value
                != requested.temperature.value
            ):
                return False

        if (
            stored.pressure is not None
            and requested.pressure is not None
        ):
            if (
                stored.pressure.dimension
                != requested.pressure.dimension
            ):
                return False

            if (
                stored.pressure.to(
                    requested.pressure.unit
                ).value
                != requested.pressure.value
            ):
                return False

        if (
            stored.volume is not None
            and requested.volume is not None
        ):
            if (
                stored.volume.dimension
                != requested.volume.dimension
            ):
                return False

            if (
                stored.volume.to(
                    requested.volume.unit
                ).value
                != requested.volume.value
            ):
                return False

        if (
            stored.pH is not None
            and requested.pH is not None
            and stored.pH != requested.pH
        ):
            return False

        if (
            stored.solvent is not None
            and requested.solvent is not None
            and stored.solvent.casefold()
            != requested.solvent.casefold()
        ):
            return False

        if (
            stored.atmosphere is not None
            and requested.atmosphere is not None
            and stored.atmosphere.casefold()
            != requested.atmosphere.casefold()
        ):
            return False

        return True

    def to_scientific_property(
        self,
        name: str,
    ) -> ScientificProperty:
        """
        Convert this knowledge-layer record into an SCM
        ScientificProperty.
        """

        if not isinstance(name, str):
            raise TypeError(
                "name must be a string"
            )

        if not name.strip():
            raise ValueError(
                "property name must not be empty"
            )

        return ScientificProperty(
            name=name,
            quantity=self.quantity,
            status=self.status,
            kind=self.kind,
            conditions=self.conditions,
            uncertainty=self.uncertainty,
            evidence=self.evidence,
            notes=self.notes,
        )


__all__ = [
    "IsotopePropertyData",
    "PropertyQuantity",
]
