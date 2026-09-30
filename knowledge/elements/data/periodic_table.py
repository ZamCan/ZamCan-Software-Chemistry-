from __future__ import annotations

from dataclasses import dataclass
import re

from ..categories import ElementCategory


_VALID_BLOCKS = frozenset({
    "s",
    "p",
    "d",
    "f",
})

_SYMBOL_PATTERN = re.compile(
    r"^[A-Z][a-z]?$"
)


@dataclass(frozen=True)
class PeriodicElementData:
    """
    Structured periodic-table data for one chemical element.

    Chemical identity is defined by atomic number.
    Periodic classification is represented separately.
    """

    atomic_number: int
    name: str
    symbol: str
    period: int
    group: int | None
    block: str
    category: ElementCategory

    def __post_init__(self) -> None:
        if not 1 <= self.atomic_number <= 118:
            raise ValueError(
                "atomic number must be between 1 and 118"
            )

        if not self.name.strip():
            raise ValueError(
                "element name must not be empty"
            )

        if not _SYMBOL_PATTERN.fullmatch(self.symbol):
            raise ValueError(
                "element symbol must contain one uppercase "
                "letter optionally followed by one lowercase letter"
            )

        if not 1 <= self.period <= 7:
            raise ValueError(
                "period must be between 1 and 7"
            )

        if self.group is not None and not 1 <= self.group <= 18:
            raise ValueError(
                "group must be between 1 and 18"
            )

        if self.block not in _VALID_BLOCKS:
            raise ValueError(
                "block must be one of: s, p, d, f"
            )

        if not isinstance(
            self.category,
            ElementCategory,
        ):
            raise TypeError(
                "category must be an ElementCategory"
            )


PERIODIC_TABLE: tuple[PeriodicElementData, ...] = (

    # PERIOD 1
    PeriodicElementData(
        1, "Hydrogen", "H", 1, 1, "s",
        ElementCategory.NONMETAL,
    ),
    PeriodicElementData(
        2, "Helium", "He", 1, 18, "s",
        ElementCategory.NOBLE_GAS,
    ),

    # PERIOD 2
    PeriodicElementData(
        3, "Lithium", "Li", 2, 1, "s",
        ElementCategory.ALKALI_METAL,
    ),
    PeriodicElementData(
        4, "Beryllium", "Be", 2, 2, "s",
        ElementCategory.ALKALINE_EARTH_METAL,
    ),
    PeriodicElementData(
        5, "Boron", "B", 2, 13, "p",
        ElementCategory.METALLOID,
    ),
    PeriodicElementData(
        6, "Carbon", "C", 2, 14, "p",
        ElementCategory.NONMETAL,
    ),
    PeriodicElementData(
        7, "Nitrogen", "N", 2, 15, "p",
        ElementCategory.NONMETAL,
    ),
    PeriodicElementData(
        8, "Oxygen", "O", 2, 16, "p",
        ElementCategory.NONMETAL,
    ),
    PeriodicElementData(
        9, "Fluorine", "F", 2, 17, "p",
        ElementCategory.HALOGEN,
    ),
    PeriodicElementData(
        10, "Neon", "Ne", 2, 18, "p",
        ElementCategory.NOBLE_GAS,
    ),

    # PERIOD 3
    PeriodicElementData(
        11, "Sodium", "Na", 3, 1, "s",
        ElementCategory.ALKALI_METAL,
    ),
    PeriodicElementData(
        12, "Magnesium", "Mg", 3, 2, "s",
        ElementCategory.ALKALINE_EARTH_METAL,
    ),
    PeriodicElementData(
        13, "Aluminium", "Al", 3, 13, "p",
        ElementCategory.POST_TRANSITION_METAL,
    ),
    PeriodicElementData(
        14, "Silicon", "Si", 3, 14, "p",
        ElementCategory.METALLOID,
    ),
    PeriodicElementData(
        15, "Phosphorus", "P", 3, 15, "p",
        ElementCategory.NONMETAL,
    ),
    PeriodicElementData(
        16, "Sulfur", "S", 3, 16, "p",
        ElementCategory.NONMETAL,
    ),
    PeriodicElementData(
        17, "Chlorine", "Cl", 3, 17, "p",
        ElementCategory.HALOGEN,
    ),
    PeriodicElementData(
        18, "Argon", "Ar", 3, 18, "p",
        ElementCategory.NOBLE_GAS,
    ),

    # PERIOD 4
    PeriodicElementData(
        19, "Potassium", "K", 4, 1, "s",
        ElementCategory.ALKALI_METAL,
    ),
    PeriodicElementData(
        20, "Calcium", "Ca", 4, 2, "s",
        ElementCategory.ALKALINE_EARTH_METAL,
    ),
    PeriodicElementData(
        21, "Scandium", "Sc", 4, 3, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        22, "Titanium", "Ti", 4, 4, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        23, "Vanadium", "V", 4, 5, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        24, "Chromium", "Cr", 4, 6, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        25, "Manganese", "Mn", 4, 7, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        26, "Iron", "Fe", 4, 8, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        27, "Cobalt", "Co", 4, 9, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        28, "Nickel", "Ni", 4, 10, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        29, "Copper", "Cu", 4, 11, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        30, "Zinc", "Zn", 4, 12, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        31, "Gallium", "Ga", 4, 13, "p",
        ElementCategory.POST_TRANSITION_METAL,
    ),
    PeriodicElementData(
        32, "Germanium", "Ge", 4, 14, "p",
        ElementCategory.METALLOID,
    ),
    PeriodicElementData(
        33, "Arsenic", "As", 4, 15, "p",
        ElementCategory.METALLOID,
    ),
    PeriodicElementData(
        34, "Selenium", "Se", 4, 16, "p",
        ElementCategory.NONMETAL,
    ),
    PeriodicElementData(
        35, "Bromine", "Br", 4, 17, "p",
        ElementCategory.HALOGEN,
    ),
    PeriodicElementData(
        36, "Krypton", "Kr", 4, 18, "p",
        ElementCategory.NOBLE_GAS,
    ),

    # PERIOD 5
    PeriodicElementData(
        37, "Rubidium", "Rb", 5, 1, "s",
        ElementCategory.ALKALI_METAL,
    ),
    PeriodicElementData(
        38, "Strontium", "Sr", 5, 2, "s",
        ElementCategory.ALKALINE_EARTH_METAL,
    ),
    PeriodicElementData(
        39, "Yttrium", "Y", 5, 3, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        40, "Zirconium", "Zr", 5, 4, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        41, "Niobium", "Nb", 5, 5, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        42, "Molybdenum", "Mo", 5, 6, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        43, "Technetium", "Tc", 5, 7, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        44, "Ruthenium", "Ru", 5, 8, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        45, "Rhodium", "Rh", 5, 9, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        46, "Palladium", "Pd", 5, 10, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        47, "Silver", "Ag", 5, 11, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        48, "Cadmium", "Cd", 5, 12, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        49, "Indium", "In", 5, 13, "p",
        ElementCategory.POST_TRANSITION_METAL,
    ),
    PeriodicElementData(
        50, "Tin", "Sn", 5, 14, "p",
        ElementCategory.POST_TRANSITION_METAL,
    ),
    PeriodicElementData(
        51, "Antimony", "Sb", 5, 15, "p",
        ElementCategory.METALLOID,
    ),
    PeriodicElementData(
        52, "Tellurium", "Te", 5, 16, "p",
        ElementCategory.METALLOID,
    ),
    PeriodicElementData(
        53, "Iodine", "I", 5, 17, "p",
        ElementCategory.HALOGEN,
    ),
    PeriodicElementData(
        54, "Xenon", "Xe", 5, 18, "p",
        ElementCategory.NOBLE_GAS,
    ),

    # PERIOD 6
    PeriodicElementData(
        55, "Caesium", "Cs", 6, 1, "s",
        ElementCategory.ALKALI_METAL,
    ),
    PeriodicElementData(
        56, "Barium", "Ba", 6, 2, "s",
        ElementCategory.ALKALINE_EARTH_METAL,
    ),
    PeriodicElementData(
        57, "Lanthanum", "La", 6, None, "f",
        ElementCategory.LANTHANIDE,
    ),
    PeriodicElementData(
        58, "Cerium", "Ce", 6, None, "f",
        ElementCategory.LANTHANIDE,
    ),
    PeriodicElementData(
        59, "Praseodymium", "Pr", 6, None, "f",
        ElementCategory.LANTHANIDE,
    ),
    PeriodicElementData(
        60, "Neodymium", "Nd", 6, None, "f",
        ElementCategory.LANTHANIDE,
    ),
    PeriodicElementData(
        61, "Promethium", "Pm", 6, None, "f",
        ElementCategory.LANTHANIDE,
    ),
    PeriodicElementData(
        62, "Samarium", "Sm", 6, None, "f",
        ElementCategory.LANTHANIDE,
    ),
    PeriodicElementData(
        63, "Europium", "Eu", 6, None, "f",
        ElementCategory.LANTHANIDE,
    ),
    PeriodicElementData(
        64, "Gadolinium", "Gd", 6, None, "f",
        ElementCategory.LANTHANIDE,
    ),
    PeriodicElementData(
        65, "Terbium", "Tb", 6, None, "f",
        ElementCategory.LANTHANIDE,
    ),
    PeriodicElementData(
        66, "Dysprosium", "Dy", 6, None, "f",
        ElementCategory.LANTHANIDE,
    ),
    PeriodicElementData(
        67, "Holmium", "Ho", 6, None, "f",
        ElementCategory.LANTHANIDE,
    ),
    PeriodicElementData(
        68, "Erbium", "Er", 6, None, "f",
        ElementCategory.LANTHANIDE,
    ),
    PeriodicElementData(
        69, "Thulium", "Tm", 6, None, "f",
        ElementCategory.LANTHANIDE,
    ),
    PeriodicElementData(
        70, "Ytterbium", "Yb", 6, None, "f",
        ElementCategory.LANTHANIDE,
    ),
    PeriodicElementData(
        71, "Lutetium", "Lu", 6, None, "f",
        ElementCategory.LANTHANIDE,
    ),
    PeriodicElementData(
        72, "Hafnium", "Hf", 6, 4, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        73, "Tantalum", "Ta", 6, 5, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        74, "Tungsten", "W", 6, 6, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        75, "Rhenium", "Re", 6, 7, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        76, "Osmium", "Os", 6, 8, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        77, "Iridium", "Ir", 6, 9, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        78, "Platinum", "Pt", 6, 10, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        79, "Gold", "Au", 6, 11, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        80, "Mercury", "Hg", 6, 12, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        81, "Thallium", "Tl", 6, 13, "p",
        ElementCategory.POST_TRANSITION_METAL,
    ),
    PeriodicElementData(
        82, "Lead", "Pb", 6, 14, "p",
        ElementCategory.POST_TRANSITION_METAL,
    ),
    PeriodicElementData(
        83, "Bismuth", "Bi", 6, 15, "p",
        ElementCategory.POST_TRANSITION_METAL,
    ),
    PeriodicElementData(
        84, "Polonium", "Po", 6, 16, "p",
        ElementCategory.POST_TRANSITION_METAL,
    ),
    PeriodicElementData(
        85, "Astatine", "At", 6, 17, "p",
        ElementCategory.HALOGEN,
    ),
    PeriodicElementData(
        86, "Radon", "Rn", 6, 18, "p",
        ElementCategory.NOBLE_GAS,
    ),

    # PERIOD 7
    PeriodicElementData(
        87, "Francium", "Fr", 7, 1, "s",
        ElementCategory.ALKALI_METAL,
    ),
    PeriodicElementData(
        88, "Radium", "Ra", 7, 2, "s",
        ElementCategory.ALKALINE_EARTH_METAL,
    ),
    PeriodicElementData(
        89, "Actinium", "Ac", 7, None, "f",
        ElementCategory.ACTINIDE,
    ),
    PeriodicElementData(
        90, "Thorium", "Th", 7, None, "f",
        ElementCategory.ACTINIDE,
    ),
    PeriodicElementData(
        91, "Protactinium", "Pa", 7, None, "f",
        ElementCategory.ACTINIDE,
    ),
    PeriodicElementData(
        92, "Uranium", "U", 7, None, "f",
        ElementCategory.ACTINIDE,
    ),
    PeriodicElementData(
        93, "Neptunium", "Np", 7, None, "f",
        ElementCategory.ACTINIDE,
    ),
    PeriodicElementData(
        94, "Plutonium", "Pu", 7, None, "f",
        ElementCategory.ACTINIDE,
    ),
    PeriodicElementData(
        95, "Americium", "Am", 7, None, "f",
        ElementCategory.ACTINIDE,
    ),
    PeriodicElementData(
        96, "Curium", "Cm", 7, None, "f",
        ElementCategory.ACTINIDE,
    ),
    PeriodicElementData(
        97, "Berkelium", "Bk", 7, None, "f",
        ElementCategory.ACTINIDE,
    ),
    PeriodicElementData(
        98, "Californium", "Cf", 7, None, "f",
        ElementCategory.ACTINIDE,
    ),
    PeriodicElementData(
        99, "Einsteinium", "Es", 7, None, "f",
        ElementCategory.ACTINIDE,
    ),
    PeriodicElementData(
        100, "Fermium", "Fm", 7, None, "f",
        ElementCategory.ACTINIDE,
    ),
    PeriodicElementData(
        101, "Mendelevium", "Md", 7, None, "f",
        ElementCategory.ACTINIDE,
    ),
    PeriodicElementData(
        102, "Nobelium", "No", 7, None, "f",
        ElementCategory.ACTINIDE,
    ),
    PeriodicElementData(
        103, "Lawrencium", "Lr", 7, None, "f",
        ElementCategory.ACTINIDE,
    ),
    PeriodicElementData(
        104, "Rutherfordium", "Rf", 7, 4, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        105, "Dubnium", "Db", 7, 5, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        106, "Seaborgium", "Sg", 7, 6, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        107, "Bohrium", "Bh", 7, 7, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        108, "Hassium", "Hs", 7, 8, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        109, "Meitnerium", "Mt", 7, 9, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        110, "Darmstadtium", "Ds", 7, 10, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        111, "Roentgenium", "Rg", 7, 11, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        112, "Copernicium", "Cn", 7, 12, "d",
        ElementCategory.TRANSITION_METAL,
    ),
    PeriodicElementData(
        113, "Nihonium", "Nh", 7, 13, "p",
        ElementCategory.POST_TRANSITION_METAL,
    ),
    PeriodicElementData(
        114, "Flerovium", "Fl", 7, 14, "p",
        ElementCategory.POST_TRANSITION_METAL,
    ),
    PeriodicElementData(
        115, "Moscovium", "Mc", 7, 15, "p",
        ElementCategory.POST_TRANSITION_METAL,
    ),
    PeriodicElementData(
        116, "Livermorium", "Lv", 7, 16, "p",
        ElementCategory.POST_TRANSITION_METAL,
    ),
    PeriodicElementData(
        117, "Tennessine", "Ts", 7, 17, "p",
        ElementCategory.HALOGEN,
    ),
    PeriodicElementData(
        118, "Oganesson", "Og", 7, 18, "p",
        ElementCategory.NOBLE_GAS,
    ),
)


def validate_periodic_table(
    elements: tuple[PeriodicElementData, ...],
) -> None:
    """
    Validate uniqueness, ordering, and complete coverage
    of the periodic-table dataset.
    """

    atomic_numbers: set[int] = set()
    symbols: set[str] = set()
    names: set[str] = set()

    previous_atomic_number = 0

    for element in elements:
        if element.atomic_number in atomic_numbers:
            raise ValueError(
                f"duplicate atomic number: "
                f"{element.atomic_number}"
            )

        symbol_key = element.symbol.casefold()

        if symbol_key in symbols:
            raise ValueError(
                f"duplicate element symbol: "
                f"{element.symbol}"
            )

        name_key = element.name.casefold()

        if name_key in names:
            raise ValueError(
                f"duplicate element name: "
                f"{element.name}"
            )

        if element.atomic_number <= previous_atomic_number:
            raise ValueError(
                "periodic-table elements must be ordered "
                "by increasing atomic number"
            )

        atomic_numbers.add(
            element.atomic_number
        )
        symbols.add(symbol_key)
        names.add(name_key)

        previous_atomic_number = (
            element.atomic_number
        )

    expected = set(range(1, 119))

    if atomic_numbers != expected:
        missing = sorted(
            expected - atomic_numbers
        )
        extra = sorted(
            atomic_numbers - expected
        )

        raise ValueError(
            f"periodic-table coverage error: "
            f"missing={missing}, extra={extra}"
        )


validate_periodic_table(
    PERIODIC_TABLE
)


def get_periodic_element(
    identifier: int | str,
) -> PeriodicElementData:
    """
    Find an element by atomic number, name, or symbol.
    """

    if isinstance(identifier, int):
        for element in PERIODIC_TABLE:
            if element.atomic_number == identifier:
                return element

    elif isinstance(identifier, str):
        key = identifier.strip().casefold()

        if not key:
            raise ValueError(
                "element identifier must not be empty"
            )

        for element in PERIODIC_TABLE:
            if (
                element.name.casefold() == key
                or element.symbol.casefold() == key
            ):
                return element

    else:
        raise TypeError(
            "element identifier must be an int or string"
        )

    raise KeyError(
        f"Unknown periodic-table element: {identifier!r}"
    )


def all_periodic_elements() -> tuple[
    PeriodicElementData,
    ...,
]:
    """Return all elements in atomic-number order."""

    return PERIODIC_TABLE


__all__ = [
    "PeriodicElementData",
    "PERIODIC_TABLE",
    "get_periodic_element",
    "all_periodic_elements",
    "validate_periodic_table",
]
