import pytest

from scm.matter.atoms import Atom
from scm.structures import Bond, BondOrder, Connectivity, Molecule


def make_water():
    oxygen = Atom.create(8)
    hydrogen_1 = Atom.create(1)
    hydrogen_2 = Atom.create(1)

    bond_1 = Bond(
        oxygen,
        hydrogen_1,
        order=BondOrder.SINGLE,
    )
    bond_2 = Bond(
        oxygen,
        hydrogen_2,
        order=BondOrder.SINGLE,
    )

    connectivity = Connectivity(
        nodes=(oxygen, hydrogen_1, hydrogen_2),
        bonds=(bond_1, bond_2),
    )

    molecule = Molecule(
        species=(oxygen, hydrogen_1, hydrogen_2),
        connectivity=connectivity,
    )

    return molecule, oxygen, hydrogen_1, hydrogen_2


def test_water_molecule():
    molecule, oxygen, hydrogen_1, hydrogen_2 = make_water()

    assert molecule.atom_count == 3
    assert molecule.formula == "H2O"
    assert molecule.formula_counts == {"H": 2, "O": 1}
    assert molecule.net_charge == 0
    assert molecule.connected
    assert molecule.component_count == 1


def test_identity_distinguishes_two_hydrogen_instances():
    molecule, _, hydrogen_1, hydrogen_2 = make_water()

    assert hydrogen_1 == hydrogen_2
    assert hydrogen_1 is not hydrogen_2

    assert molecule.contains(hydrogen_1)
    assert molecule.contains(hydrogen_2)
    assert molecule.count(hydrogen_1) == 1
    assert molecule.count(hydrogen_2) == 1


def test_neighbors_are_delegated_to_connectivity():
    molecule, oxygen, hydrogen_1, hydrogen_2 = make_water()

    assert molecule.neighbors(oxygen) == (hydrogen_1, hydrogen_2)


def test_molecule_requires_matching_connectivity():
    oxygen = Atom.create(8)
    hydrogen = Atom.create(1)

    other_hydrogen = Atom.create(1)

    connectivity = Connectivity(
        nodes=(oxygen, hydrogen),
        bonds=(
            Bond(
                oxygen,
                hydrogen,
            ),
        ),
    )

    with pytest.raises(ValueError):
        Molecule(
            species=(oxygen, other_hydrogen),
            connectivity=connectivity,
        )


def test_molecule_rejects_wrong_charge():
    molecule, oxygen, hydrogen_1, hydrogen_2 = make_water()

    with pytest.raises(ValueError):
        Molecule(
            species=(oxygen, hydrogen_1, hydrogen_2),
            connectivity=molecule.connectivity,
            charge=1,
        )


def test_molecule_requires_at_least_one_species():
    connectivity = Connectivity()

    with pytest.raises(ValueError):
        Molecule(
            species=(),
            connectivity=connectivity,
        )
