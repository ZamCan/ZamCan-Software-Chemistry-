import pytest

from scm.core import Quantity
from scm.structures.geometry import Vector3D


def q(value, unit="m"):
    return Quantity(value, unit)


def test_dot_product():
    first = Vector3D(q(1), q(2), q(3))
    second = Vector3D(q(4), q(5), q(6))
    result = first.dot(second)
    assert result.value == pytest.approx(32.0)
    assert result.dimension == first.x.dimension * second.x.dimension


def test_dot_product_is_symmetric():
    first = Vector3D(q(1), q(2), q(3))
    second = Vector3D(q(4), q(5), q(6))
    assert first.dot(second) == second.dot(first)


def test_dot_product_supports_mixed_units():
    first = Vector3D(q(1, "m"), q(2, "m"), q(3, "m"))
    second = Vector3D(q(100, "cm"), q(200, "cm"), q(300, "cm"))
    result = first.dot(second)
    assert result.value == pytest.approx(14.0)


def test_dot_product_rejects_incompatible_dimensions():
    first = Vector3D(q(1), q(2), q(3))
    second = Vector3D(
        Quantity(1, "s"),
        Quantity(2, "s"),
        Quantity(3, "s"),
    )
    with pytest.raises(ValueError):
        first.dot(second)


def test_norm():
    vector = Vector3D(q(3), q(4), q(0))
    result = vector.norm()
    assert result.value == pytest.approx(5.0)
    assert result.dimension == vector.dimension


def test_normalized_vector_has_unit_magnitude():
    vector = Vector3D(q(3), q(4), q(0))
    normalized = vector.normalized()
    assert normalized.norm().value == pytest.approx(1.0)
    assert normalized.dimension == vector.dimension / vector.dimension


def test_normalized_vector_preserves_direction():
    vector = Vector3D(q(3), q(4), q(0))
    normalized = vector.normalized()
    assert normalized.x.value == pytest.approx(0.6)
    assert normalized.y.value == pytest.approx(0.8)
    assert normalized.z.value == pytest.approx(0.0)


def test_normalized_rejects_zero_vector():
    vector = Vector3D(q(0), q(0), q(0))
    with pytest.raises(ValueError):
        vector.normalized()


def test_cross_product():
    first = Vector3D(q(1), q(0), q(0))
    second = Vector3D(q(0), q(1), q(0))
    result = first.cross(second)
    assert result.x.value == pytest.approx(0.0)
    assert result.y.value == pytest.approx(0.0)
    assert result.z.value == pytest.approx(1.0)
    assert result.dimension == first.dimension * second.dimension


def test_cross_product_reverses_direction():
    first = Vector3D(q(1), q(0), q(0))
    second = Vector3D(q(0), q(1), q(0))
    forward = first.cross(second)
    reverse = second.cross(first)
    assert forward.z.value == pytest.approx(1.0)
    assert reverse.z.value == pytest.approx(-1.0)


def test_cross_product_of_parallel_vectors_is_zero():
    first = Vector3D(q(1), q(2), q(3))
    second = Vector3D(q(2), q(4), q(6))
    result = first.cross(second)
    assert result.x.value == pytest.approx(0.0)
    assert result.y.value == pytest.approx(0.0)
    assert result.z.value == pytest.approx(0.0)


def test_cross_product_supports_mixed_units():
    first = Vector3D(q(1, "m"), q(0, "m"), q(0, "m"))
    second = Vector3D(q(0, "cm"), q(100, "cm"), q(0, "cm"))
    result = first.cross(second)
    assert result.z.value == pytest.approx(1.0)


def test_cross_product_rejects_incompatible_dimensions():
    first = Vector3D(q(1, "m"), q(0, "m"), q(0, "m"))
    second = Vector3D(
        Quantity(0, "s"),
        Quantity(1, "s"),
        Quantity(0, "s"),
    )
    with pytest.raises(ValueError):
        first.cross(second)
