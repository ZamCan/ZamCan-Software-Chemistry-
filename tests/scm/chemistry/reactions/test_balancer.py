from scm.chemistry.reactions import ChemicalEquation, balance_equation


def test_balance_water_formation():
    equation = ChemicalEquation.from_formulas(
        ("H2", "O2"),
        ("H2O",),
    )

    result = balance_equation(equation)

    assert result.reactant_coefficients == (2, 1)
    assert result.product_coefficients == (2,)
    assert result.formatted() == "2H2 + O2 → 2H2O"


def test_balance_iron_oxide():
    equation = ChemicalEquation.from_formulas(
        ("Fe", "O2"),
        ("Fe2O3",),
    )

    result = balance_equation(equation)

    assert result.formatted() == "4Fe + 3O2 → 2Fe2O3"
