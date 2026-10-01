from enum import Enum


class BondOrder(str, Enum):
    """Formal/effective bond-order descriptors.

    Bond order is not universally identical to bond strength. In delocalized
    or multicentre systems an effective/fractional value may be appropriate.
    """

    SINGLE = "single"
    DOUBLE = "double"
    TRIPLE = "triple"
    QUADRUPLE = "quadruple"
    AROMATIC = "aromatic"
    PARTIAL = "partial"
    UNKNOWN = "unknown"


class BondType(str, Enum):
    """Primary interaction classification.

    Real bonds form a continuum of ionic/covalent character. These labels
    describe dominant bonding regimes or chemically useful interaction modes.
    """

    COVALENT = "covalent"
    POLAR_COVALENT = "polar_covalent"
    IONIC = "ionic"
    METALLIC = "metallic"
    COORDINATE = "coordinate"
    MULTICENTER = "multicenter"
    HYDROGEN = "hydrogen"
    HALOGEN = "halogen"
    VAN_DER_WAALS = "van_der_waals"
    UNKNOWN = "unknown"


class BondComponent(str, Enum):
    """Directional components used to describe covalent bonding."""

    SIGMA = "sigma"
    PI = "pi"
    DELOCALIZED_PI = "delocalized_pi"
    DELocalized_PI = "delocalized_pi"
    THREE_CENTER = "three_center"
    FOUR_ELECTRON = "four_electron"
    UNKNOWN = "unknown"
