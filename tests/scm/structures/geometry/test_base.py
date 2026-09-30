import pytest

from scm.core import Quantity
from scm.matter.atoms import Atom
from scm.structures import (
    Bond,
    Connectivity,
    Molecule,
    MolecularGeometry,
    Vector3D,
)


def make_water():
    oxygen = Atom.create(8)
    hydrogen_1 = Atom.create(1)
    hydrogen_2 = Atom.create(1)

    connectivity = Connectivity(
        nodes=(oxygen, hydrogen_1, hydrogen_2),
        bonds=(
            Bond(oxygen, hydrogen_1),
            Bond(oxygen, hydrogen_2),
        ),
    )

    molecule = Molecule(
        species=(oxygen, hydrogen_1, hydrogen_2),
        connectivity=connectivity,
    )

    geometry = MolecularGeometry(
        molecule=molecule,
        positions=(
            (
                oxygen,
                Vector3D(
                    Quantity(0, "m"),
                    Quantity(0, "m"),
                    Quantity(0, "m"),
                ),
            ),
            (
                hydrogen_1,
                Vector3D(
                    Quantity(0.096, "nm"),
                    Quantity(0, "nm"),
                    Quantity(0, "nm"),
                ),
            ),
            (
                hydrogen_2,
                Vector3D(
                    Quantity(-0.024, "nm"),
                    Quantity(0.093, "nm"),
                    Quantity(0, "nm"),
                ),
            ),
        ),
    )

    return molecule, geometry, oxygen, hydrogen_1, hydrogen_2


def test_vector_requires_quantities():
    with pytest.raises(TypeError):
        Vector3D(1, Quantity(0, "m"), Quantity(0, "m"))


def test_vector_requires_same_dimension():
    with pytest.raises(ValueError):
        Vector3D(
            Quantity(1, "m"),
            Quantity(2, "s"),
            Quantity(3, "m"),
        )


def test_vector_addition_and_conversion():
    first = Vector3D(
        Quantity(1, "m"),
        Quantity(2, "m"),
        Quantity(3, "m"),
    )

    second = Vector3D(
        Quantity(50, "cm"),
        Quantity(1, "m"),
        Quantity(2, "m"),
    )

    result = first + second

    assert result.x.to("m").value == pytest.approx(1.5)
    assert result.y.value == pytest.approx(3)
    assert result.z.value == pytest.approx(5)


def test_vector_subtraction():
    first = Vector3D(
        Quantity(3, "m"),
        Quantity(4, "m"),
        Quantity(5, "m"),
    )

    second = Vector3D(
        Quantity(1, "m"),
        Quantity(2, "m"),
        Quantity(3, "m"),
    )

    result = first - second

    assert result.components == (
        Quantity(2, "m"),
        Quantity(2, "m"),
        Quantity(2, "m"),
    )


def test_vector_scalar_multiplication():
    vector = Vector3D(
        Quantity(1, "m"),
        Quantity(2, "m"),
        Quantity(3, "m"),
    )

    result = 2 * vector

    assert result.components == (
        Quantity(2, "m"),
        Quantity(4, "m"),
        Quantity(6, "m"),
    )


def test_water_geometry():
    molecule, geometry, oxygen, hydrogen_1, hydrogen_2 = make_water()

    assert geometry.dimensionality == 3
    assert geometry.contains(oxygen)
    assert geometry.contains(hydrogen_1)
    assert geometry.contains(hydrogen_2)

    assert geometry.position_of(oxygen).x.value == 0
    assert geometry.position_of(hydrogen_1).x.to("nm").value == pytest.approx(0.096)


def test_geometry_rejects_species_outside_molecule():
    molecule, _, _, _, _ = make_water()

    external_hydrogen = Atom.create(1)

    with pytest.raises(ValueError):
        MolecularGeometry(
            molecule=molecule,
            positions=(
                (
                    external_hydrogen,
                    Vector3D(
                        Quantity(0, "m"),
                        Quantity(0, "m"),
                        Quantity(0, "m"),
                    ),
                ),
            ),
        )


def test_geometry_requires_every_species_positioned():
    molecule, _, oxygen, hydrogen_1, _ = make_water()

    with pytest.raises(ValueError):
        MolecularGeometry(
            molecule=molecule,
            positions=(
                (
                    oxygen,
                    Vector3D(
                        Quantity(0, "m"),
                        Quantity(0, "m"),
                        Quantity(0, "m"),
                    ),
                ),
                (
                    hydrogen_1,
                    Vector3D(
                        Quantity(1, "m"),
                        Quantity(0, "m"),
                        Quantity(0, "m"),
                    ),
                ),
            ),
        )


def test_geometry_rejects_duplicate_species_position():
    molecule, _, oxygen, _, _ = make_water()

    position = Vector3D(
        Quantity(0, "m"),
        Quantity(0, "m"),
        Quantity(0, "m"),
    )

    with pytest.raises(ValueError):
        MolecularGeometry(
            molecule=molecule,
            positions=(
                (oxygen, position),
                (oxygen, position),
            ),
        )
