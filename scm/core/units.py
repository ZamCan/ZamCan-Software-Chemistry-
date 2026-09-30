from dataclasses import dataclass
from enum import Enum
from typing import Dict


@dataclass(frozen=True)
class Dimension:
    mass: int = 0
    length: int = 0
    time: int = 0
    temperature: int = 0
    amount: int = 0
    current: int = 0
    angle: int = 0

    def __mul__(self, other: "Dimension") -> "Dimension":
        return Dimension(
            self.mass + other.mass,
            self.length + other.length,
            self.time + other.time,
            self.temperature + other.temperature,
            self.amount + other.amount,
            self.current + other.current,
            self.angle + other.angle,
        )

    def __truediv__(self, other: "Dimension") -> "Dimension":
        return Dimension(
            self.mass - other.mass,
            self.length - other.length,
            self.time - other.time,
            self.temperature - other.temperature,
            self.amount - other.amount,
            self.current - other.current,
            self.angle - other.angle,
        )


class ConversionType(str, Enum):
    MULTIPLICATIVE = "multiplicative"
    AFFINE = "affine"


@dataclass(frozen=True)
class UnitDefinition:
    """
    Definition of an SCM unit.

    Conversion to the canonical unit of the same dimension is:

        base_value = value * scale + offset

    Most units are ordinary scale-only units and therefore use
    offset=0. Temperature scales such as Celsius and Fahrenheit
    require an offset.
    """

    symbol: str
    dimension: Dimension
    scale: float = 1.0
    offset: float = 0.0
    conversion_type: ConversionType = ConversionType.MULTIPLICATIVE


MASS = Dimension(mass=1)
LENGTH = Dimension(length=1)
TIME = Dimension(time=1)
TEMPERATURE = Dimension(temperature=1)
AMOUNT = Dimension(amount=1)
INVERSE_AMOUNT = Dimension(amount=-1)
CURRENT = Dimension(current=1)

ANGLE = Dimension(angle=1)

CHARGE = CURRENT * TIME
DIMENSIONLESS = Dimension()


UNIT_REGISTRY: Dict[str, UnitDefinition] = {
    # Mass
    "kg": UnitDefinition("kg", MASS, 1.0),
    "g": UnitDefinition("g", MASS, 1e-3),
    "mg": UnitDefinition("mg", MASS, 1e-6),

    # Length
    "m": UnitDefinition("m", LENGTH, 1.0),
    "cm": UnitDefinition("cm", LENGTH, 1e-2),
    "mm": UnitDefinition("mm", LENGTH, 1e-3),
    "nm": UnitDefinition("nm", LENGTH, 1e-9),

    # Time
    "s": UnitDefinition("s", TIME, 1.0),
    "min": UnitDefinition("min", TIME, 60.0),
    "h": UnitDefinition("h", TIME, 3600.0),

    # Temperature
    #
    # Kelvin is the canonical absolute-temperature unit.
    "K": UnitDefinition("K", TEMPERATURE, 1.0, 0.0, ConversionType.AFFINE),

    # Celsius:
    # K = °C + 273.15
    "degC": UnitDefinition(
        "degC",
        TEMPERATURE,
        1.0,
        273.15,
        ConversionType.AFFINE,
    ),

    # Fahrenheit:
    # K = °F × 5/9 + 255.372222...
    "degF": UnitDefinition(
        "degF",
        TEMPERATURE,
        5.0 / 9.0,
        255.3722222222222,
        ConversionType.AFFINE,
    ),

    # Amount of substance
    "mol": UnitDefinition("mol", AMOUNT, 1.0),
    "mol⁻¹": UnitDefinition("mol⁻¹", INVERSE_AMOUNT, 1.0),
    "1": UnitDefinition("1", DIMENSIONLESS, 1.0),

    # Molar mass
    "kg/mol": UnitDefinition(
        "kg/mol",
        MASS / AMOUNT,
        1.0,
    ),
    "g/mol": UnitDefinition(
        "g/mol",
        MASS / AMOUNT,
        1e-3,
    ),

    # Angle
    "rad": UnitDefinition("rad", ANGLE, 1.0),
    "deg": UnitDefinition(
        "deg",
        ANGLE,
        3.141592653589793 / 180.0,
    ),

    # Electric current
    "A": UnitDefinition("A", CURRENT, 1.0),

    # Electric charge
    "C": UnitDefinition("C", CHARGE, 1.0),

    # Area
    "m²": UnitDefinition("m²", LENGTH * LENGTH, 1.0),
    "cm²": UnitDefinition("cm²", LENGTH * LENGTH, 1e-4),
    "mm²": UnitDefinition("mm²", LENGTH * LENGTH, 1e-6),
    "nm²": UnitDefinition("nm²", LENGTH * LENGTH, 1e-18),

    # Volume
    "L": UnitDefinition(
        "L",
        LENGTH * LENGTH * LENGTH,
        1e-3,
    ),
    "mL": UnitDefinition(
        "mL",
        LENGTH * LENGTH * LENGTH,
        1e-6,
    ),

    # Pressure
    "Pa": UnitDefinition(
        "Pa",
        MASS / (LENGTH * TIME * TIME),
        1.0,
    ),

    # Energy
    "J": UnitDefinition(
        "J",
        MASS * LENGTH * LENGTH / (TIME * TIME),
        1.0,
    ),
    "kJ": UnitDefinition(
        "kJ",
        MASS * LENGTH * LENGTH / (TIME * TIME),
        1000.0,
    ),

    # Action / angular momentum
    "J·s": UnitDefinition(
        "J·s",
        MASS * LENGTH * LENGTH / TIME,
        1.0,
    ),
}


def get_unit(symbol: str) -> UnitDefinition:
    try:
        return UNIT_REGISTRY[symbol]
    except KeyError as exc:
        raise ValueError(
            f"Unknown SCM unit: {symbol}"
        ) from exc


def _normalize_float(value: float) -> float:
    """
    Remove harmless floating-point noise from conversions.
    """
    if value != 0:
        nearest = round(value)
        if abs(value - nearest) <= abs(value) * 1e-15:
            return float(nearest)

    return value


def to_base(value: float, unit: str) -> float:
    """
    Convert a numeric value to the canonical base representation
    of its dimension.
    """
    definition = get_unit(unit)

    return _normalize_float(
        value * definition.scale + definition.offset
    )


def from_base(value: float, unit: str) -> float:
    """
    Convert a canonical base value to the requested unit.
    """
    definition = get_unit(unit)

    converted = (
        value - definition.offset
    ) / definition.scale

    return _normalize_float(converted)


def convert(
    value: float,
    from_unit: str,
    to_unit: str,
) -> float:
    """
    Convert a value between compatible SCM units.
    """
    source = get_unit(from_unit)
    target = get_unit(to_unit)

    if source.dimension != target.dimension:
        raise ValueError(
            f"Incompatible dimensions: "
            f"{from_unit} -> {to_unit}"
        )

    base_value = to_base(value, from_unit)

    return from_base(base_value, to_unit)
