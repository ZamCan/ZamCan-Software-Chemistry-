from __future__ import annotations

from scm.core import (
    Evidence,
    EvidenceType,
    PropertyKind,
    QuantityRange,
    ScientificStatus,
    Quantity,
)

from .base import ElementPropertyData
from .atomic import register_atomic_property


hydrogen_standard_atomic_weight = ElementPropertyData(
    atomic_number=1,
    kind=PropertyKind.STANDARD_ATOMIC_WEIGHT,
    quantity=QuantityRange(
        minimum=Quantity(1.00784, "1"),
        maximum=Quantity(1.00811, "1"),
    ),
    status=ScientificStatus.KNOWN,
    evidence=Evidence(
        evidence_type=EvidenceType.REFERENCE,
        source="IUPAC / CIAAW",
        reference="IUPAC Periodic Table of the Elements, 4 May 2022",
        notes=(
            "Conventional tabulated value represented as a range "
            "because natural hydrogen isotopic composition varies."
        ),
    ),
)


register_atomic_property(
    hydrogen_standard_atomic_weight
)


__all__ = [
    "hydrogen_standard_atomic_weight",
]
