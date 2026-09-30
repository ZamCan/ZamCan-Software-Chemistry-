import math

import pytest

from scm.core import Quantity
from scm.matter.atoms import Atom
from scm.structures.bonds import Bond
from scm.structures.connectivity import Connectivity
from scm.structures.molecules import Molecule
from scm.structures.geometry import (
    MolecularGeometry,
    Vector3D,
    angle,
)


def make_three_atom_molecule():
    first = Atom.create(1)
    vertex = Atom.create(8)
    second = Atom.create(1)

    bond1 = Bond(first, vertex)
    bond2 = Bond(vertex, second)

    connectivity = Connectivity(
        nodes=(first, vertex, second),
        bonds=(bond1, bond2),
    )

    molecule = Molecule(
        species=(first, vertex, second),
        connectivity=connectivity,
    )

    return first, vertex, second, molecule


def geometry_for(
    first,
    vertex,
    second,
    first_position,
    vertex_position,
    second_position,
    molecule,
):
    return MolecularGeometry(
        molecule=molecule,
        positions=(
            (first, first_position),
            (vertex, vertex_position),
            (second, second_position),
        ),
    )


def test_angle_returns_90_degrees():
    first, vertex, second, molecule = make_three_atom_molecule()

    geometry = geometry_for(
        first,
        vertex,
        second,
        Vector3D(
            Quantity(1.0, "nm"),
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        Vector3D(
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        Vector3D(
            Quantity(0.0, "nm"),
            Quantity(1.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        molecule,
    )

    result = angle(molecule, first, vertex, second, geometry)

    assert result.unit == "rad"
    assert result.value == pytest.approx(math.pi / 2.0)


def test_angle_returns_180_degrees_for_linear_geometry():
    first, vertex, second, molecule = make_three_atom_molecule()

    geometry = geometry_for(
        first,
        vertex,
        second,
        Vector3D(
            Quantity(-1.0, "nm"),
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        Vector3D(
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        Vector3D(
            Quantity(1.0, "nm"),
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        molecule,
    )

    result = angle(molecule, first, vertex, second, geometry)

    assert result.to("deg").value == pytest.approx(180.0)


def test_angle_returns_60_degrees():
    first, vertex, second, molecule = make_three_atom_molecule()

    geometry = geometry_for(
        first,
        vertex,
        second,
        Vector3D(
            Quantity(1.0, "nm"),
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        Vector3D(
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        Vector3D(
            Quantity(0.5, "nm"),
            Quantity(math.sqrt(3.0) / 2.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        molecule,
    )

    result = angle(molecule, first, vertex, second, geometry)

    assert result.to("deg").value == pytest.approx(60.0)


def test_h_o_h_style_geometry_is_measured_from_coordinates():
    first, vertex, second, molecule = make_three_atom_molecule()

    # A deliberately non-ideal water-like geometry.
    target_angle = 104.5
    half_angle = math.radians(target_angle / 2.0)

    geometry = geometry_for(
        first,
        vertex,
        second,
        Vector3D(
            Quantity(math.cos(half_angle), "nm"),
            Quantity(math.sin(half_angle), "nm"),
            Quantity(0.0, "nm"),
        ),
        Vector3D(
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        Vector3D(
            Quantity(math.cos(half_angle), "nm"),
            Quantity(-math.sin(half_angle), "nm"),
            Quantity(0.0, "nm"),
        ),
        molecule,
    )

    result = angle(molecule, first, vertex, second, geometry)

    assert result.to("deg").value == pytest.approx(target_angle)


def test_angle_is_symmetric_when_endpoints_are_reversed():
    first, vertex, second, molecule = make_three_atom_molecule()

    geometry = geometry_for(
        first,
        vertex,
        second,
        Vector3D(
            Quantity(1.0, "nm"),
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        Vector3D(
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        Vector3D(
            Quantity(0.0, "nm"),
            Quantity(1.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        molecule,
    )

    forward = angle(molecule, first, vertex, second, geometry)
    reverse = angle(molecule, second, vertex, first, geometry)

    assert forward.value == pytest.approx(reverse.value)


def test_angle_handles_mixed_coordinate_units():
    first, vertex, second, molecule = make_three_atom_molecule()

    geometry = geometry_for(
        first,
        vertex,
        second,
        Vector3D(
            Quantity(1.0, "nm"),
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        Vector3D(
            Quantity(0.0, "m"),
            Quantity(0.0, "m"),
            Quantity(0.0, "m"),
        ),
        Vector3D(
            Quantity(0.0, "m"),
            Quantity(1e-9, "m"),
            Quantity(0.0, "m"),
        ),
        molecule,
    )

    result = angle(molecule, first, vertex, second, geometry)

    assert result.to("deg").value == pytest.approx(90.0)


def test_angle_rejects_endpoint_coincident_with_vertex():
    first, vertex, second, molecule = make_three_atom_molecule()

    geometry = geometry_for(
        first,
        vertex,
        second,
        Vector3D(
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        Vector3D(
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        Vector3D(
            Quantity(1.0, "nm"),
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        molecule,
    )

    with pytest.raises(ValueError, match="coincides with the vertex"):
        angle(molecule, first, vertex, second, geometry)


def test_angle_rejects_same_endpoint_species():
    first, vertex, _, molecule = make_three_atom_molecule()

    geometry = MolecularGeometry(
        molecule=molecule,
        positions=(
            (
                first,
                Vector3D(
                    Quantity(1.0, "nm"),
                    Quantity(0.0, "nm"),
                    Quantity(0.0, "nm"),
                ),
            ),
            (
                vertex,
                Vector3D(
                    Quantity(0.0, "nm"),
                    Quantity(0.0, "nm"),
                    Quantity(0.0, "nm"),
                ),
            ),
            (
                molecule.species[2],
                Vector3D(
                    Quantity(0.0, "nm"),
                    Quantity(1.0, "nm"),
                    Quantity(0.0, "nm"),
                ),
            ),
        ),
    )

    with pytest.raises(ValueError, match="different species instances"):
        angle(molecule, first, vertex, first, geometry)


def test_angle_rejects_species_outside_molecule():
    first, vertex, second, molecule = make_three_atom_molecule()

    outside = Atom.create(6)

    geometry = geometry_for(
        first,
        vertex,
        second,
        Vector3D(
            Quantity(1.0, "nm"),
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        Vector3D(
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        Vector3D(
            Quantity(0.0, "nm"),
            Quantity(1.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        molecule,
    )

    with pytest.raises(ValueError, match="first species must belong"):
        angle(molecule, outside, vertex, second, geometry)


def test_angle_rejects_wrong_geometry():
    first, vertex, second, molecule = make_three_atom_molecule()

    other_first, other_vertex, other_second, other_molecule = (
        make_three_atom_molecule()
    )

    other_geometry = geometry_for(
        other_first,
        other_vertex,
        other_second,
        Vector3D(
            Quantity(1.0, "nm"),
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        Vector3D(
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        Vector3D(
            Quantity(0.0, "nm"),
            Quantity(1.0, "nm"),
            Quantity(0.0, "nm"),
        ),
        other_molecule,
    )

    with pytest.raises(ValueError, match="geometry must belong"):
        angle(
            molecule,
            first,
            vertex,
            second,
            other_geometry,
        )
