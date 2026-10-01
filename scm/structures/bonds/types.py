from enum import Enum


class BondOrder(str, Enum):
    """Formal bond order representation.

    Bond order is a structural/electronic descriptor, not a universal measure
    of bond strength. Delocalized systems may require fractional/effective
    orders, and some interactions have no meaningful integer bond order.
    """

    SINGLE = "single"
    DOUBLE = "double"
    TRIPLE = "triple"
    QUADRUPLE = "quadruple"
    AROMATIC = "aromatic"
    PARTIAL = "partial"
    UNKNOWN = "unknown"


class BondType(str, Enum):
    """Chemical interaction/bonding regime.

    These categories are intentionally not mutually exclusive in real
    chemistry. For example, a polar covalent bond has covalent character with
    charge separation, while coordinate bonding is a mode of electron-pair
    donation within covalent/coordination chemistry.
    """

    COVALENT = "covalent"
    IONIC = "ionic"
    METALLIC = "metallic"
    COORDINATE = "coordinate"
    HYDROGEN = "hydrogen"
    VAN_DER_WAALS = "van_der_waals"
    UNKNOWN = "unknown"
