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


def test_balances_explicit_ionic_charge():
    from scm.chemistry.reactions.equation import ChemicalEquation, ReactionSide, Species
    from scm.chemistry.reactions.balancer import balance_equation

    equation = ChemicalEquation(
        reactants=ReactionSide((
            Species("Fe", charge_number=2),
            Species("Ce", charge_number=4),
        )),
        products=ReactionSide((
            Species("Fe", charge_number=3),
            Species("Ce", charge_number=3),
        )),
    )
    result = balance_equation(equation)

    assert result.balanced


def test_grouped_formula_parser_counts_nested_groups():
    from scm.chemistry.formulas import parse_grouped_formula

    parsed = parse_grouped_formula("Al2(SO4)3")
    assert parsed.element_counts == {"Al": 2, "S": 3, "O": 12}
