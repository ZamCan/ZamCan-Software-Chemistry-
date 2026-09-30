from __future__ import annotations

from knowledge.elements.loaders.records import RawElementRecord
from knowledge.elements.properties.base import ElementPropertyData
from scm.core import (
    Conditions,
    Evidence,
    PropertyKind,
    Quantity,
    ScientificStatus,
    Uncertainty,
    EvidenceType,
)


class ElementPropertyAdapter:
    """
    Converts source-neutral element records into the existing
    SCM ElementPropertyData representation.

    This layer performs no scientific guessing.
    """

    @staticmethod
    def _status(value: str) -> ScientificStatus:
        try:
            return ScientificStatus(value)
        except ValueError as exc:
            raise ValueError(
                f"unsupported scientific status: {value}"
            ) from exc

    @staticmethod
    def _kind(value: str) -> PropertyKind:
        normalized = value.strip().upper()

        aliases = {
            "STANDARD_ATOMIC_WEIGHT":
                PropertyKind.STANDARD_ATOMIC_WEIGHT,
            "RELATIVE_ATOMIC_MASS":
                PropertyKind.RELATIVE_ATOMIC_MASS,
            "ISOTOPIC_ATOMIC_MASS":
                PropertyKind.ISOTOPIC_ATOMIC_MASS,
            "MOLAR_MASS":
                PropertyKind.MOLAR_MASS,
            "ATOMIC_MASS":
                PropertyKind.ATOMIC_MASS,
            "DENSITY":
                PropertyKind.DENSITY,
            "MELTING_POINT":
                PropertyKind.MELTING_POINT,
            "BOILING_POINT":
                PropertyKind.BOILING_POINT,
            "IONIZATION_ENERGY":
                PropertyKind.IONIZATION_ENERGY,
            "ELECTRON_AFFINITY":
                PropertyKind.ELECTRON_AFFINITY,
            "ELECTRONEGATIVITY":
                PropertyKind.ELECTRONEGATIVITY,
            "ATOMIC_RADIUS":
                PropertyKind.ATOMIC_RADIUS,
            "COVALENT_RADIUS":
                PropertyKind.COVALENT_RADIUS,
            "ELECTRICAL_CONDUCTIVITY":
                PropertyKind.ELECTRICAL_CONDUCTIVITY,
            "THERMAL_CONDUCTIVITY":
                PropertyKind.THERMAL_CONDUCTIVITY,
            "HEAT_CAPACITY":
                PropertyKind.HEAT_CAPACITY,
            "ENTHALPY":
                PropertyKind.ENTHALPY,
            "ENTROPY":
                PropertyKind.ENTROPY,
            "GIBBS_FREE_ENERGY":
                PropertyKind.GIBBS_FREE_ENERGY,
        }

        if normalized not in aliases:
            return PropertyKind.OTHER

        return aliases[normalized]

    @classmethod
    def convert_property(
        cls,
        record,
    ) -> ElementPropertyData:
        if record.value is None:
            raise ValueError(
                "cannot convert a property without a value"
            )

        if record.unit is None:
            raise ValueError(
                "cannot convert a valued property without a unit"
            )

        quantity = Quantity(
            record.value,
            record.unit,
        )

        evidence = ()

        if record.source or record.reference:
            evidence = (
                Evidence(
                    evidence_type=EvidenceType.REFERENCE,
                    source=record.source,
                    reference=record.reference,
                ),
            )

        uncertainty = None

        if record.uncertainty is not None:
            uncertainty = Uncertainty(
                absolute=record.uncertainty,
            )

        conditions = None

        if record.conditions:
            conditions = Conditions(
                atmosphere="; ".join(record.conditions)
            )

        return ElementPropertyData(
            atomic_number=record.atomic_number,
            kind=cls._kind(record.property_name),
            quantity=quantity,
            status=cls._status(record.status),
            conditions=conditions,
            uncertainty=uncertainty,
            evidence=evidence,
            notes=record.notes,
        )

    @classmethod
    def convert(
        cls,
        record: RawElementRecord,
    ) -> tuple[ElementPropertyData, ...]:
        return tuple(
            cls.convert_property(property_record)
            for property_record in record.properties
        )
