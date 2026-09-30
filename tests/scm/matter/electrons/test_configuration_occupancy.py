from scm.matter.electrons import (
    ElectronConfiguration,
    ElectronSubshell,
)


def make_configuration(*items):
    return ElectronConfiguration(
        subshells=tuple(
            ElectronSubshell(
                principal_level=n,
                subshell=subshell,
                electron_count=count,
            )
            for n, subshell, count in items
        )
    )


def test_configuration_exposes_subshell_occupancies():
    configuration = make_configuration(
        (1, "s", 2),
        (2, "s", 2),
        (2, "p", 2),
    )

    occupancies = configuration.occupancies

    assert len(occupancies) == 3
    assert occupancies[0].notation == "1s2"
    assert occupancies[1].notation == "2s2"
    assert occupancies[2].notation == "2p2"


def test_configuration_flattens_orbital_occupancies():
    configuration = make_configuration(
        (1, "s", 2),
        (2, "p", 2),
    )

    orbital_occupancies = configuration.orbital_occupancies

    # 1s has 1 orbital, 2p has 3 orbitals.
    assert len(orbital_occupancies) == 4


def test_configuration_unpaired_electron_count():
    configuration = make_configuration(
        (1, "s", 2),
        (2, "p", 2),
    )

    assert configuration.unpaired_electron_count == 2


def test_configuration_spin_multiplicity():
    configuration = make_configuration(
        (1, "s", 2),
        (2, "p", 2),
    )

    assert configuration.spin_multiplicity == 3


def test_configuration_pauli_validation():
    configuration = make_configuration(
        (1, "s", 2),
        (2, "p", 4),
    )

    assert configuration.validate_pauli is True


def test_configuration_hund_validation():
    configuration = make_configuration(
        (1, "s", 2),
        (2, "p", 4),
    )

    assert configuration.validate_hund is True
    assert configuration.is_hund_ground_state is True


def test_configuration_total_electron_count_is_preserved():
    configuration = make_configuration(
        (1, "s", 2),
        (2, "s", 2),
        (2, "p", 4),
    )

    assert configuration.electron_count == 8


def test_existing_notation_is_preserved():
    configuration = make_configuration(
        (1, "s", 2),
        (2, "s", 2),
        (2, "p", 4),
    )

    assert configuration.notation() == "1s2 2s2 2p4"
