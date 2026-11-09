"""Amount concentration and solute-conserving dilution."""
from fractions import Fraction
from math import isfinite

from scm.core import Quantity, QuantityRange


def _normalized(quantity: Quantity, unit: str, *, positive: bool = False) -> float:
    if not isinstance(quantity, Quantity):
        raise TypeError(f"Expected a quantity convertible to {unit}.")
    if isinstance(quantity.value, bool) or not isinstance(quantity.value, (int, float)):
        raise ValueError(f"Quantity in {unit} must be numeric.")
    if not isfinite(quantity.value) or quantity.value < 0:
        raise ValueError(f"Quantity in {unit} must be finite and nonnegative.")
    try:
        value = quantity.value if quantity.unit == unit else quantity.to(unit).value
    except OverflowError as exc:
        raise ValueError(f"Quantity in {unit} exceeds the numeric range.") from exc
    if not isfinite(value):
        raise ValueError(f"Quantity in {unit} exceeds the numeric range.")
    if quantity.value and value == 0:
        raise ValueError(f"Quantity in {unit} is below the numeric range.")
    if positive and value <= 0:
        raise ValueError(f"Quantity in {unit} must be positive.")
    return value


def molarity(amount: Quantity, final_volume: Quantity) -> Quantity:
    """Divide solute amount by the final solution volume."""
    moles = _normalized(amount, "mol")
    litres = _normalized(final_volume, "L", positive=True)
    return Quantity(_representable(Fraction(moles) / Fraction(litres), "Molarity"), "mol/L")


def molarity_from_mass(
    solute_mass: Quantity, molar_mass: Quantity | QuantityRange, final_volume: Quantity
) -> Quantity | QuantityRange:
    """Preserve a composition-derived molar-mass interval through n = m / M."""
    grams = Fraction(_normalized(solute_mass, "g"))
    litres = Fraction(_normalized(final_volume, "L", positive=True))

    def concentration(mass_per_mole: Quantity) -> Quantity:
        weight = Fraction(_normalized(mass_per_mole, "g/mol", positive=True))
        return Quantity(_representable(grams / (weight * litres), "Molarity"), "mol/L")

    if isinstance(molar_mass, QuantityRange):
        return QuantityRange(concentration(molar_mass.maximum), concentration(molar_mass.minimum))
    return concentration(molar_mass)


def diluted_molarity(
    stock: Quantity, aliquot: Quantity, final_volume: Quantity
) -> Quantity:
    """Calculate concentration after solvent addition with conserved solute."""
    concentration = _normalized(stock, "mol/L")
    aliquot_l = _normalized(aliquot, "L", positive=True)
    final_l = _normalized(final_volume, "L", positive=True)
    if aliquot_l > final_l:
        raise ValueError("Final volume must be at least the stock aliquot volume.")
    return Quantity(
        _representable(Fraction(concentration) * Fraction(aliquot_l) / Fraction(final_l), "Molarity"),
        "mol/L",
    )


def equivalence_amount(
    titrant: Quantity, delivered: Quantity, analyte_per_titrant: float
) -> Quantity:
    """Compute analyte amount from titrant delivered at equivalence."""
    concentration = _normalized(titrant, "mol/L")
    litres = _normalized(delivered, "L")
    ratio = _normalized(Quantity(analyte_per_titrant, "1"), "1")
    amount = Fraction(concentration) * Fraction(litres) * Fraction(ratio)
    return Quantity(_representable(amount, "Analyte amount"), "mol")


def _representable(value: Fraction, name: str) -> float:
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} exceeds the numeric range.") from exc
    if value and result == 0:
        raise ValueError(f"{name} is below the numeric range.")
    return result
