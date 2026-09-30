from __future__ import annotations

from scm.core import Quantity
from .vector import Vector3D


def distance(first: Vector3D, second: Vector3D) -> Quantity:
    """Return the Euclidean distance between two 3D positions.

    Both vectors must represent positions in the same physical
    length dimension. The result uses the unit of the first vector's
    x-component.
    """
    if not isinstance(first, Vector3D):
        raise TypeError("first must be a Vector3D")

    if not isinstance(second, Vector3D):
        raise TypeError("second must be a Vector3D")

    if first.dimension != second.dimension:
        raise ValueError("Vector dimensions must match")

    dx = first.x - second.x
    dy = first.y - second.y
    dz = first.z - second.z

    squared = (
        dx.value ** 2
        + dy.value ** 2
        + dz.value ** 2
    )

    return Quantity(squared ** 0.5, first.x.unit)

def bond_length(
    molecule,
    bond,
    geometry,
) -> Quantity:
    """Return the geometric length of a bond in a molecule.

    The bond endpoints must be the exact ChemicalSpecies instances
    belonging to the molecule and represented by the supplied geometry.
    """
    from scm.structures.bonds import Bond
    from scm.structures.molecules import Molecule
    from .structure import MolecularGeometry

    if not isinstance(molecule, Molecule):
        raise TypeError("molecule must be a Molecule")

    if not isinstance(bond, Bond):
        raise TypeError("bond must be a Bond")

    if not isinstance(geometry, MolecularGeometry):
        raise TypeError("geometry must be a MolecularGeometry")

    if geometry.molecule is not molecule:
        raise ValueError("geometry must belong to the supplied molecule")

    first, second = bond.endpoints

    if not molecule.contains(first) or not molecule.contains(second):
        raise ValueError("bond endpoints must belong to the molecule")

    return distance(
        geometry.position_of(first),
        geometry.position_of(second),
    )

def angle(
    molecule,
    first,
    vertex,
    second,
    geometry,
) -> Quantity:
    """Return the geometric angle first-vertex-second.

    The vertex species is the central point of the angle. The angle is
    calculated from the vectors vertex->first and vertex->second.

    The result is returned in radians.

    Species identity is checked using object identity, consistent with
    the rest of the molecular structure and geometry system.
    """
    from math import acos

    from scm.structures.molecules import Molecule
    from .structure import MolecularGeometry

    if not isinstance(molecule, Molecule):
        raise TypeError("molecule must be a Molecule")

    if not isinstance(geometry, MolecularGeometry):
        raise TypeError("geometry must be a MolecularGeometry")

    if geometry.molecule is not molecule:
        raise ValueError("geometry must belong to the supplied molecule")

    if not molecule.contains(first):
        raise ValueError("first species must belong to the molecule")

    if not molecule.contains(vertex):
        raise ValueError("vertex species must belong to the molecule")

    if not molecule.contains(second):
        raise ValueError("second species must belong to the molecule")

    if first is vertex or second is vertex:
        raise ValueError("angle endpoints must differ from the vertex")

    if first is second:
        raise ValueError("angle endpoints must be different species instances")

    first_position = geometry.position_of(first)
    vertex_position = geometry.position_of(vertex)
    second_position = geometry.position_of(second)

    first_vector = first_position - vertex_position
    second_vector = second_position - vertex_position

    if first_vector.dimension != second_vector.dimension:
        raise ValueError("angle vectors must have matching dimensions")

    if first_vector.dimension != first_position.dimension:
        raise ValueError("angle geometry must use position vectors consistently")

    # Convert to the first vector's unit so the dot-product calculation
    # operates in one consistent length unit.
    second_vector = second_vector.to(first_vector.x.unit)

    dot = (
        first_vector.x.value * second_vector.x.value
        + first_vector.y.value * second_vector.y.value
        + first_vector.z.value * second_vector.z.value
    )

    first_norm = (
        first_vector.x.value ** 2
        + first_vector.y.value ** 2
        + first_vector.z.value ** 2
    ) ** 0.5

    second_norm = (
        second_vector.x.value ** 2
        + second_vector.y.value ** 2
        + second_vector.z.value ** 2
    ) ** 0.5

    if first_norm == 0 or second_norm == 0:
        raise ValueError(
            "angle cannot be calculated when an endpoint coincides with the vertex"
        )

    cosine = dot / (first_norm * second_norm)

    # Floating-point arithmetic can produce values such as
    # 1.0000000000000002 for an exact 0-degree angle.
    cosine = max(-1.0, min(1.0, cosine))

    return Quantity(acos(cosine), "rad")

