from scm.matter.electrons import (
    ElectronConfiguration,
    SubshellOccupancy,
)


def test_from_subshell_counts():
    configuration = ElectronConfiguration.from_subshell_counts(
        (
            (1, "s", 2),
            (2, "s", 2),
            (2, "p", 4),
        )
    )

    assert configuration.electron_count == 8
    assert configuration.notation() == "1s2 2s2 2p4"


def test_from_subshell_counts_creates_valid_occupancy():
    configuration = ElectronConfiguration.from_subshell_counts(
        (
            (1, "s", 2),
            (2, "s", 2),
            (2, "p", 3),
        )
    )

    assert configuration.validate_pauli
    assert configuration.validate_hund
    assert configuration.unpaired_electron_count == 3


def test_from_occupancies():
    occupancies = (
        SubshellOccupancy.from_electron_count(1, "s", 2),
        SubshellOccupancy.from_electron_count(2, "s", 2),
        SubshellOccupancy.from_electron_count(2, "p", 2),
    )

    configuration = ElectronConfiguration.from_occupancies(
        occupancies
    )

    assert configuration.electron_count == 6
    assert configuration.notation() == "1s2 2s2 2p2"


def test_round_trip_occupancies():
    configuration = ElectronConfiguration.from_subshell_counts(
        (
            (1, "s", 2),
            (2, "s", 2),
            (2, "p", 4),
        )
    )

    rebuilt = ElectronConfiguration.from_occupancies(
        configuration.occupancies
    )

    assert rebuilt.notation() == configuration.notation()
    assert rebuilt.electron_count == configuration.electron_count


def test_empty_configuration():
    configuration = ElectronConfiguration.from_subshell_counts(())

    assert configuration.electron_count == 0
    assert configuration.occupancies == ()
    assert configuration.notation() == ""
    assert configuration.validate_pauli
    assert configuration.validate_hund


def test_occupancy_count_matches_configuration():
    configuration = ElectronConfiguration.from_subshell_counts(
        (
            (1, "s", 2),
            (2, "s", 2),
            (2, "p", 4),
        )
    )

    assert sum(
        occupancy.electron_count
        for occupancy in configuration.occupancies
    ) == configuration.electron_count
