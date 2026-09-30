from __future__ import annotations

from scm.core import (
    Evidence,
    EvidenceType,
    PropertyKind,
    Quantity,
    QuantityRange,
    ScientificStatus,
)

from .atomic import register_atomic_property
from .base import ElementPropertyData


oxygen_standard_atomic_weight = ElementPropertyData(
    atomic_number=8,
    kind=PropertyKind.STANDARD_ATOMIC_WEIGHT,
    quantity=QuantityRange(
        minimum=Quantity(15.999, "1"),
        maximum=Quantity(16.000, "1"),
    ),
    status=ScientificStatus.KNOWN,
    evidence=Evidence(
        evidence_type=EvidenceType.REFERENCE,
        source="IUPAC / CIAAW",
        reference="IUPAC Periodic Table of the Elements, 4 May 2022",
        notes=(
            "Standard atomic weight interval for oxygen. "
            "The atomic weight of oxygen varies with natural "
            "terrestrial isotopic composition."
        ),
    ),
)


register_atomic_property(
    oxygen_standard_atomic_weight
)


__all__ = [
    "oxygen_standard_atomic_weight",
]
