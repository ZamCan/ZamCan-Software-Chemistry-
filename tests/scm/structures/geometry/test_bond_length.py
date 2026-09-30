import pytest

from scm.core import Quantity
from scm.matter.atoms import Atom
from scm.structures.bonds import Bond
from scm.structures.connectivity import Connectivity
from scm.structures.molecules import Molecule
from scm.structures.geometry import (
    MolecularGeometry,
    Vector3D,
    bond_length,
)


def q(value, unit):
    return Quantity(value, unit)


def make_h2():
    h1 = Atom.create(1)
    h2 = Atom.create(1)

    bond = Bond(h1, h2)

    connectivity = Connectivity(
        nodes=(h1, h2),
        bonds=(bond,),
    )

    molecule = Molecule(
        species=(h1, h2),
        connectivity=connectivity,
    )

    geometry = MolecularGeometry(
        molecule=molecule,
        positions=(
            (
                h1,
                Vector3D(
                    q(0, "nm"),
                    q(0, "nm"),
                    q(0, "nm"),
                ),
            ),
            (
                h2,
                Vector3D(
                    q(0.074, "nm"),
                    q(0, "nm"),
                    q(0, "nm"),
                ),
            ),
        ),
    )

    return molecule, bond, geometry


def test_bond_length():
    molecule, bond, geometry = make_h2()

    result = bond_length(molecule, bond, geometry)

    assert result == q(0.074, "nm")


def test_bond_length_is_symmetric():
    molecule, bond, geometry = make_h2()

    reversed_bond = bond.reversed()

    assert bond_length(molecule, bond, geometry) == bond_length(
        molecule,
        reversed_bond,
        geometry,
    )


def test_bond_length_can_convert_units():
    molecule, bond, geometry = make_h2()

    result = bond_length(molecule, bond, geometry)

    assert result.to("m") == q(0.074e-9, "m")


def test_bond_length_rejects_bond_outside_molecule():
    molecule, _, geometry = make_h2()

    x = Atom.create(1)
    y = Atom.create(1)
    outside_bond = Bond(x, y)

    with pytest.raises(ValueError):
        bond_length(molecule, outside_bond, geometry)


def test_bond_length_rejects_wrong_geometry():
    molecule, bond, geometry = make_h2()

    other_h1 = Atom.create(1)
    other_h2 = Atom.create(1)
    other_bond = Bond(other_h1, other_h2)

    other_connectivity = Connectivity(
        nodes=(other_h1, other_h2),
        bonds=(other_bond,),
    )

    other_molecule = Molecule(
        species=(other_h1, other_h2),
        connectivity=other_connectivity,
    )

    other_geometry = MolecularGeometry(
        molecule=other_molecule,
        positions=(
            (
                other_h1,
                Vector3D(
                    q(0, "nm"),
                    q(0, "nm"),
                    q(0, "nm"),
                ),
            ),
            (
                other_h2,
                Vector3D(
                    q(0.074, "nm"),
                    q(0, "nm"),
                    q(0, "nm"),
                ),
            ),
        ),
    )

    with pytest.raises(ValueError):
        bond_length(molecule, bond, other_geometry)


def test_bond_length_rejects_invalid_types():
    molecule, bond, geometry = make_h2()

    with pytest.raises(TypeError):
        bond_length("not molecule", bond, geometry)

    with pytest.raises(TypeError):
        bond_length(molecule, "not bond", geometry)

    with pytest.raises(TypeError):
        bond_length(molecule, bond, "not geometry")
