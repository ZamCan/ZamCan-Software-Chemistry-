import pytest

from scm.core import Quantity
from scm.structures.geometry import Vector3D, distance


def q(value, unit):
    return Quantity(value, unit)


def test_distance_along_x():
    a = Vector3D(q(0, "nm"), q(0, "nm"), q(0, "nm"))
    b = Vector3D(q(0.1, "nm"), q(0, "nm"), q(0, "nm"))

    result = distance(a, b)

    assert result == q(0.1, "nm")


def test_distance_in_three_dimensions():
    a = Vector3D(q(0, "m"), q(0, "m"), q(0, "m"))
    b = Vector3D(q(3, "m"), q(4, "m"), q(12, "m"))

    result = distance(a, b)

    assert result == q(13, "m")


def test_distance_is_symmetric():
    a = Vector3D(q(0, "nm"), q(0, "nm"), q(0, "nm"))
    b = Vector3D(q(1, "nm"), q(2, "nm"), q(2, "nm"))

    assert distance(a, b) == distance(b, a)


def test_distance_supports_unit_conversion():
    a = Vector3D(q(0, "nm"), q(0, "nm"), q(0, "nm"))
    b = Vector3D(q(1, "m"), q(0, "m"), q(0, "m"))

    assert distance(a, b).to("m") == q(1, "m")


def test_distance_rejects_non_vectors():
    with pytest.raises(TypeError):
        distance(q(0, "m"), q(1, "m"))


def test_distance_rejects_incompatible_dimensions():
    a = Vector3D(q(0, "m"), q(0, "m"), q(0, "m"))
    b = Vector3D(q(1, "s"), q(0, "s"), q(0, "s"))

    with pytest.raises(ValueError):
        distance(a, b)
