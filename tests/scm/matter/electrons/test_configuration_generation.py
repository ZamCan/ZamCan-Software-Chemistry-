import pytest

from scm.matter.electrons import (
    GeneratedConfiguration,
    generate_configuration,
    ground_state_configuration,
)


def test_generate_configuration_returns_structured_occupancies():
    config = generate_configuration(8)

    assert isinstance(config, GeneratedConfiguration)
    assert config.electron_count == 8
    assert all(item.electron_count >= 0 for item in config.occupancies)


def test_generated_configuration_is_pauli_valid():
    config = generate_configuration(17)

    assert config.validate()


def test_generated_configuration_uses_hund_occupancy():
    config = generate_configuration(7)

    nitrogen = next(
        item
        for item in config.occupancies
        if item.principal_level == 2 and item.subshell == "p"
    )

    assert nitrogen.electron_count == 3
    assert nitrogen.unpaired_electron_count == 3
    assert nitrogen.validate_hund()


def test_neutral_ground_state_uses_atomic_number():
    config = ground_state_configuration(11)

    assert config.electron_count == 11


def test_chromium_exception_is_structured():
    config = ground_state_configuration(24)

    d3 = next(
        item
        for item in config.occupancies
        if item.principal_level == 3 and item.subshell == "d"
    )

    s4 = next(
        item
        for item in config.occupancies
        if item.principal_level == 4 and item.subshell == "s"
    )

    assert d3.electron_count == 5
    assert s4.electron_count == 1


def test_invalid_electron_count_rejected():
    with pytest.raises(ValueError):
        generate_configuration(-1)


def test_invalid_atomic_number_rejected():
    with pytest.raises(ValueError):
        generate_configuration(1, atomic_number=119)
