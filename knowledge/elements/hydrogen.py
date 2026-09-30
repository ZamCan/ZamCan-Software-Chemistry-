from scm.core import (
    Evidence,
    EvidenceType,
    PropertyKind,
    ScientificProperty,
    ScientificStatus,
    Quantity,
    QuantityRange,
)
from scm.matter.elements import Element

from .base import ElementRecord
from .categories import ElementCategory


hydrogen = ElementRecord(
    element=Element(1),
    name="Hydrogen",
    symbol="H",
    period=1,
    group=1,
    block="s",
    category=ElementCategory.NONMETAL,
    properties=(
        ScientificProperty(
            name="standard atomic weight",
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
                    "Conventional tabulated value. Natural hydrogen "
                    "isotopic composition can vary, so this scalar value "
                    "does not represent every natural terrestrial sample."
                ),
            ),
        ),
    ),
)


__all__ = [
    "hydrogen",
]
