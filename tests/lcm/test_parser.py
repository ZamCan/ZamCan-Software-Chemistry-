import pytest

from lcm import IntentKind, parse


def test_parses_english_element_lookup():
    intent = parse("What is oxygen?")
    assert intent.kind is IntentKind.ELEMENT_LOOKUP
    assert intent.target == "oxygen"


def test_parses_swahili_element_lookup():
    intent = parse("Ni nini oxygen?")
    assert intent.kind is IntentKind.ELEMENT_LOOKUP
    assert intent.target == "oxygen"


def test_parses_balance_request():
    intent = parse("balance H2 + O2 -> H2O")
    assert intent.kind is IntentKind.BALANCE_EQUATION
    assert intent.reactants == ("H2", "O2")
    assert intent.products == ("H2O",)


def test_unknown_text_is_not_guessed():
    intent = parse("Tell me something interesting about chemistry.")
    assert intent.kind is IntentKind.UNKNOWN
    assert intent.confidence == 0.0


def test_empty_input_rejected():
    with pytest.raises(ValueError):
        parse("")


def test_non_text_rejected():
    with pytest.raises(TypeError):
        parse(None)
