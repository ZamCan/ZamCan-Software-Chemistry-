from enum import Enum


class BondOrder(str, Enum):
    SINGLE = "single"
    DOUBLE = "double"
    TRIPLE = "triple"
    QUADRUPLE = "quadruple"
    AROMATIC = "aromatic"
    UNKNOWN = "unknown"


class BondType(str, Enum):
    COVALENT = "covalent"
    IONIC = "ionic"
    METALLIC = "metallic"
    COORDINATE = "coordinate"
    HYDROGEN = "hydrogen"
    VAN_DER_WAALS = "van_der_waals"
    UNKNOWN = "unknown"
