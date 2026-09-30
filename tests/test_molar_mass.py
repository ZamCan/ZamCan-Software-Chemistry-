import pytest

from scm.core import Quantity, QuantityRange
from scm.matter.composition import Composition
from scm.matter.species import ChemicalSpecies
from scm.chemistry.quantities.molar_mass import MolarMassCalculator


calculator = MolarMassCalculator()


def species_from_formula_mapping(mapping):
    return ChemicalSpecies(
        composition=Composition.from_mapping(mapping)
    )


def test_hydrogen_water_molar_mass_preserves_atomic_weight_ranges():
    water = species_from_formula_mapping(
        {"H": 2, "O": 1}
    )

    result = calculator.calculate(water)

    assert result.species == water
    assert len(result.terms) == 2
    assert isinstance(result.molar_mass, QuantityRange)

    minimum = result.molar_mass.minimum.to("g/mol").value
    maximum = result.molar_mass.maximum.to("g/mol").value

    assert minimum == pytest.approx(
        2 * 1.00784 + 15.999,
        rel=1e-12,
    )

    assert maximum == pytest.approx(
        2 * 1.00811 + 16.000,
        rel=1e-12,
    )


def test_single_element_oxygen_preserves_standard_atomic_weight_range():
    oxygen = species_from_formula_mapping(
        {"O": 1}
    )

    result = calculator.calculate(oxygen)

    assert isinstance(result.molar_mass, QuantityRange)

    minimum = result.molar_mass.minimum.to("g/mol").value
    maximum = result.molar_mass.maximum.to("g/mol").value

    assert minimum == pytest.approx(
        15.999,
        rel=1e-12,
    )

    assert maximum == pytest.approx(
        16.000,
        rel=1e-12,
    )


def test_stoichiometric_count_scales_range_contribution():
    oxygen = species_from_formula_mapping(
        {"O": 2}
    )

    result = calculator.calculate(oxygen)

    assert isinstance(result.molar_mass, QuantityRange)

    minimum = result.molar_mass.minimum.to("g/mol").value
    maximum = result.molar_mass.maximum.to("g/mol").value

    assert minimum == pytest.approx(
        2 * 15.999,
        rel=1e-12,
    )

    assert maximum == pytest.approx(
        2 * 16.000,
        rel=1e-12,
    )


def test_terms_preserve_elemental_calculation_trace():
    water = species_from_formula_mapping(
        {"H": 2, "O": 1}
    )

    result = calculator.calculate(water)

    hydrogen_term = next(
        term
        for term in result.terms
        if term.element == "H"
    )

    oxygen_term = next(
        term
        for term in result.terms
        if term.element == "O"
    )

    assert hydrogen_term.count == 2
    assert oxygen_term.count == 1

    assert isinstance(
        hydrogen_term.atomic_mass,
        QuantityRange,
    )

    assert isinstance(
        hydrogen_term.contribution,
        QuantityRange,
    )

    assert isinstance(
        oxygen_term.atomic_mass,
        QuantityRange,
    )

    assert isinstance(
        oxygen_term.contribution,
        QuantityRange,
    )


def test_empty_composition_is_rejected():
    with pytest.raises(ValueError):
        Composition.from_mapping({})


def test_invalid_species_is_rejected():
    with pytest.raises(TypeError):
        calculator.calculate("H2O")


def test_unknown_element_is_rejected():
    with pytest.raises((KeyError, ValueError)):
        species_from_formula_mapping(
            {"Xx": 2}
        )
