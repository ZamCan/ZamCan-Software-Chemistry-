from __future__ import annotations

from scm.core import PropertyKind, Quantity, QuantityRange
from scm.matter.species import ChemicalSpecies
from knowledge.elements import get_element
from knowledge.elements.properties import get_atomic_properties_by_kind

from ..molar import MolarMass
from .result import MolarMassCalculation, MolarMassTerm


MassQuantity = Quantity | QuantityRange


class MolarMassCalculator:
    """
    Calculate molar mass from a ChemicalSpecies composition.

    The fundamental calculation is:

        M = sum(n_i * M_i)

    where n_i is the number of atoms of element i in the
    composition and M_i is the corresponding atomic-mass value.

    Standard atomic weights are represented as dimensionless
    relative values in the current element knowledge layer.
    They are converted to kg/mol by multiplying by 1e-3.
    """

    def calculate(
        self,
        species: ChemicalSpecies,
    ) -> MolarMassCalculation:
        if not isinstance(species, ChemicalSpecies):
            raise TypeError(
                "species must be a ChemicalSpecies"
            )

        terms: list[MolarMassTerm] = []

        total: MassQuantity = Quantity(
            0.0,
            "kg/mol",
        )

        for symbol, count in species.element_counts.items():
            record = get_element(symbol)

            properties = get_atomic_properties_by_kind(
                record.atomic_number,
                PropertyKind.STANDARD_ATOMIC_WEIGHT,
            )

            if not properties:
                raise ValueError(
                    f"No standard atomic weight data available "
                    f"for element {symbol}"
                )

            if len(properties) != 1:
                raise ValueError(
                    f"Ambiguous standard atomic weight data for "
                    f"element {symbol}: {len(properties)} records"
                )

            atomic_mass = properties[0].quantity

            if isinstance(atomic_mass, Quantity):
                contribution = _scalar_contribution(
                    atomic_mass,
                    count,
                )
            elif isinstance(atomic_mass, QuantityRange):
                contribution = _range_contribution(
                    atomic_mass,
                    count,
                )
            else:
                raise TypeError(
                    f"Unsupported atomic-mass quantity for {symbol}: "
                    f"{type(atomic_mass).__name__}"
                )

            terms.append(
                MolarMassTerm(
                    element=symbol,
                    count=count,
                    atomic_mass=atomic_mass,
                    contribution=contribution,
                )
            )

            total = _add_mass_values(
                total,
                contribution,
            )

        return MolarMassCalculation(
            species=species,
            molar_mass=total,
            terms=tuple(terms),
        )


def _scalar_contribution(
    atomic_mass: Quantity,
    count: int,
) -> Quantity:
    """
    Convert a dimensionless standard atomic weight into kg/mol
    and multiply by the elemental count.
    """

    if atomic_mass.dimension != Quantity(1.0, "1").dimension:
        raise ValueError(
            "Standard atomic weight must be dimensionless"
        )

    atomic_molar_mass = Quantity(
        atomic_mass.value * 1e-3,
        "kg/mol",
    )

    return atomic_molar_mass * count


def _range_contribution(
    atomic_mass: QuantityRange,
    count: int,
) -> QuantityRange:
    """
    Propagate an inclusive atomic-weight interval through
    positive stoichiometric multiplication.
    """

    if atomic_mass.dimension != Quantity(1.0, "1").dimension:
        raise ValueError(
            "Standard atomic weight must be dimensionless"
        )

    minimum = Quantity(
        atomic_mass.minimum.value * 1e-3,
        "kg/mol",
    ) * count

    maximum = Quantity(
        atomic_mass.maximum.value * 1e-3,
        "kg/mol",
    ) * count

    return QuantityRange(
        minimum=minimum,
        maximum=maximum,
    )


def _add_mass_values(
    left: MassQuantity,
    right: MassQuantity,
) -> MassQuantity:
    """
    Add scalar and/or interval molar-mass contributions.

    Interval arithmetic is conservative:
        [a,b] + [c,d] = [a+c, b+d]
    """

    if isinstance(left, Quantity) and isinstance(right, Quantity):
        return left + right

    if isinstance(left, QuantityRange) and isinstance(right, Quantity):
        return QuantityRange(
            minimum=left.minimum + right,
            maximum=left.maximum + right,
        )

    if isinstance(left, Quantity) and isinstance(right, QuantityRange):
        return QuantityRange(
            minimum=left + right.minimum,
            maximum=left + right.maximum,
        )

    if isinstance(left, QuantityRange) and isinstance(right, QuantityRange):
        return QuantityRange(
            minimum=left.minimum + right.minimum,
            maximum=left.maximum + right.maximum,
        )

    raise TypeError(
        "mass contributions must be Quantity or QuantityRange"
    )


__all__ = [
    "MolarMassCalculator",
]
