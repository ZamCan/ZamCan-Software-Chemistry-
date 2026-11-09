"""CIAAW 2024 atomic weights for normal materials.

Source: https://ciaaw.org/atomic-weights.htm
Values are (value or lower endpoint, upper endpoint, tabulated uncertainty).
Original CIAAW note codes appear alongside the values.
"""

from scm.core import (
    Evidence, EvidenceType, PropertyKind, Quantity, QuantityRange, ScientificStatus, Uncertainty,
)

from .atomic import register_atomic_property
from .base import ElementPropertyData


STANDARD_ATOMIC_WEIGHTS = {
    1: (1.00784, 1.00811, None),  # H m
    2: (4.002602, None, 2e-6),  # He g r
    3: (6.938, 6.997, None),  # Li m
    4: (9.0121831, None, 5e-7),  # Be
    5: (10.806, 10.821, None),  # B m
    6: (12.0096, 12.0116, None),  # C
    7: (14.00643, 14.00728, None),  # N m
    8: (15.99903, 15.99977, None),  # O m
    9: (18.998403162, None, 5e-9),  # F
    10: (20.1797, None, 6e-4),  # Ne g m
    11: (22.98976928, None, 2e-8),  # Na
    12: (24.304, 24.307, None),  # Mg
    13: (26.9815384, None, 3e-7),  # Al
    14: (28.084, 28.086, None),  # Si
    15: (30.973761998, None, 5e-9),  # P
    16: (32.059, 32.076, None),  # S
    17: (35.446, 35.457, None),  # Cl m
    18: (39.792, 39.963, None),  # Ar
    19: (39.0983, None, 1e-4),  # K
    20: (40.078, None, 4e-3),  # Ca g
    21: (44.955907, None, 4e-6),  # Sc
    22: (47.867, None, 1e-3),  # Ti
    23: (50.9415, None, 1e-4),  # V
    24: (51.9961, None, 6e-4),  # Cr
    25: (54.938043, None, 2e-6),  # Mn
    26: (55.845, None, 2e-3),  # Fe
    27: (58.933194, None, 3e-6),  # Co
    28: (58.6934, None, 4e-4),  # Ni r
    29: (63.546, None, 3e-3),  # Cu r
    30: (65.38, None, 2e-2),  # Zn r
    31: (69.723, None, 1e-3),  # Ga
    32: (72.630, None, 8e-3),  # Ge
    33: (74.921595, None, 6e-6),  # As
    34: (78.971, None, 8e-3),  # Se r
    35: (79.901, 79.907, None),  # Br
    36: (83.798, None, 2e-3),  # Kr g m
    37: (85.4678, None, 3e-4),  # Rb g
    38: (87.62, None, 1e-2),  # Sr g r
    39: (88.905838, None, 2e-6),  # Y
    40: (91.222, None, 3e-3),  # Zr g
    41: (92.90637, None, 1e-5),  # Nb
    42: (95.95, None, 1e-2),  # Mo g
    44: (101.07, None, 2e-2),  # Ru g
    45: (102.90549, None, 2e-5),  # Rh
    46: (106.42, None, 1e-2),  # Pd g
    47: (107.8682, None, 2e-4),  # Ag g
    48: (112.414, None, 4e-3),  # Cd g
    49: (114.818, None, 1e-3),  # In
    50: (118.710, None, 7e-3),  # Sn g
    51: (121.760, None, 1e-3),  # Sb g
    52: (127.60, None, 3e-2),  # Te g
    53: (126.90447, None, 3e-5),  # I
    54: (131.293, None, 6e-3),  # Xe g m
    55: (132.90545196, None, 6e-8),  # Cs
    56: (137.327, None, 7e-3),  # Ba
    57: (138.90547, None, 7e-5),  # La g
    58: (140.116, None, 1e-3),  # Ce g
    59: (140.90766, None, 1e-5),  # Pr
    60: (144.242, None, 3e-3),  # Nd g
    62: (150.36, None, 2e-2),  # Sm g
    63: (151.964, None, 1e-3),  # Eu g
    64: (157.249, None, 2e-3),  # Gd g
    65: (158.925354, None, 7e-6),  # Tb
    66: (162.500, None, 1e-3),  # Dy g
    67: (164.930329, None, 5e-6),  # Ho
    68: (167.259, None, 3e-3),  # Er g
    69: (168.934219, None, 5e-6),  # Tm
    70: (173.045, None, 10e-3),  # Yb g
    71: (174.96669, None, 5e-5),  # Lu g
    72: (178.486, None, 6e-3),  # Hf g
    73: (180.94788, None, 2e-5),  # Ta
    74: (183.84, None, 1e-2),  # W
    75: (186.207, None, 1e-3),  # Re
    76: (190.23, None, 3e-2),  # Os g
    77: (192.217, None, 2e-3),  # Ir
    78: (195.084, None, 9e-3),  # Pt
    79: (196.966570, None, 4e-6),  # Au
    80: (200.592, None, 3e-3),  # Hg
    81: (204.382, 204.385, None),  # Tl
    82: (206.14, 207.94, None),  # Pb
    83: (208.98040, None, 1e-5),  # Bi
    90: (232.0377, None, 4e-4),  # Th g
    91: (231.03588, None, 1e-5),  # Pa
    92: (238.02891, None, 3e-5),  # U g m
}


def _record(atomic_number, lower, upper, uncertainty):
    quantity = Quantity(lower, "1")
    if upper is not None:
        quantity = QuantityRange(quantity, Quantity(upper, "1"))
    return ElementPropertyData(
        atomic_number=atomic_number,
        kind=PropertyKind.STANDARD_ATOMIC_WEIGHT,
        quantity=quantity,
        status=ScientificStatus.KNOWN,
        uncertainty=Uncertainty(absolute=uncertainty) if uncertainty is not None else None,
        evidence=Evidence(
            evidence_type=EvidenceType.REFERENCE,
            source="CIAAW, Standard Atomic Weights 2024",
            reference="https://ciaaw.org/atomic-weights.htm",
        ),
    )


RECORDS = {
    number: _record(number, *entry) for number, entry in STANDARD_ATOMIC_WEIGHTS.items()
}
for record in RECORDS.values():
    register_atomic_property(record)
