"""Amount concentration and solute-conserving dilution."""
from math import isfinite

from scm.core import Quantity, QuantityRange


def _normalized(quantity: Quantity, unit: str, *, positive: bool = False) -> float:
    if not isinstance(quantity, Quantity) or isinstance(quantity.value, bool):
        raise TypeError(f"Expected a numeric quantity convertible to {unit}.")
    if not isfinite(quantity.value) or quantity.value < 0:
        raise ValueError(f"Quantity in {unit} must be finite and nonnegative.")
    try:
        value = quantity.to(unit).value
    except OverflowError as exc:
        raise ValueError(f"Quantity in {unit} exceeds the numeric range.") from exc
    if not isfinite(value):
        raise ValueError(f"Quantity in {unit} exceeds the numeric range.")
    if positive and value <= 0:
        raise ValueError(f"Quantity in {unit} must be positive.")
    return value


def molarity(amount: Quantity, final_volume: Quantity) -> Quantity:
    """Divide solute amount by the final solution volume."""
    moles = _normalized(amount, "mol")
    litres = _normalized(final_volume, "L", positive=True)
    value = moles / litres
    if not isfinite(value):
        raise ValueError("Molarity exceeds the numeric range.")
    return Quantity(value, "mol/L")


def molarity_from_mass(
    solute_mass: Quantity, molar_mass: Quantity | QuantityRange, final_volume: Quantity
) -> Quantity | QuantityRange:
    """Preserve a composition-derived molar-mass interval through n = m / M."""
    grams = _normalized(solute_mass, "g")

    def concentration(mass_per_mole: Quantity) -> Quantity:
        moles = grams / _normalized(mass_per_mole, "g/mol", positive=True)
        return molarity(Quantity(moles, "mol"), final_volume)

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
    # Form the volume ratio first to avoid overflow in concentration × volume.
    return Quantity(concentration * (aliquot_l / final_l), "mol/L")
