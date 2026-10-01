from lcm import interpret, parse


def test_interprets_element_lookup_through_zcm_catalog():
    result = interpret(parse("What is oxygen?"))
    assert result.successful
    assert result.result.symbol == "O"
    assert result.result.atomic_number == 8


def test_interprets_equation_balance_through_scm():
    result = interpret(parse("balance H2 + O2 -> H2O"))
    assert result.successful
    assert result.result.is_balanced
