
import pytest

from scm.matter.nuclear_states import (
    NuclearState,
    NuclearStateType,
)


def test_ground_state():
    state = NuclearState(
        state_type=NuclearStateType.GROUND,
    )

    assert state.state_type is NuclearStateType.GROUND
    assert state.excitation_energy is None


def test_excited_state():
    state = NuclearState(
        state_type=NuclearStateType.EXCITED,
        excitation_energy=100.0,
        excitation_energy_unit="keV",
    )

    assert state.state_type is NuclearStateType.EXCITED
    assert state.excitation_energy == 100.0


def test_isomeric_state():
    state = NuclearState(
        state_type=NuclearStateType.ISOMERIC,
        excitation_energy=142.68,
        excitation_energy_unit="keV",
        label="m",
    )

    assert state.state_type is NuclearStateType.ISOMERIC
    assert state.label == "m"


def test_excitation_energy_requires_unit():
    with pytest.raises(ValueError):
        NuclearState(
            state_type=NuclearStateType.EXCITED,
            excitation_energy=100.0,
        )


def test_excitation_energy_cannot_be_negative():
    with pytest.raises(ValueError):
        NuclearState(
            state_type=NuclearStateType.EXCITED,
            excitation_energy=-1.0,
            excitation_energy_unit="keV",
        )


def test_ground_state_cannot_have_nonzero_excitation_energy():
    with pytest.raises(ValueError):
        NuclearState(
            state_type=NuclearStateType.GROUND,
            excitation_energy=1.0,
            excitation_energy_unit="keV",
        )
