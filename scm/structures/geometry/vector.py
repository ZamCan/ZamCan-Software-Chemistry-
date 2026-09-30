from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

from scm.core import Quantity


@dataclass(frozen=True)
class Vector3D:
    """
    Three-dimensional Cartesian vector whose components carry units.

    All components must represent the same physical dimension.
    """

    x: Quantity
    y: Quantity
    z: Quantity

    def __post_init__(self) -> None:
        for component in (self.x, self.y, self.z):
            if not isinstance(component, Quantity):
                raise TypeError("vector components must be Quantity objects")

        if not (
            self.x.dimension
            == self.y.dimension
            == self.z.dimension
        ):
            raise ValueError(
                "vector components must have identical dimensions"
            )

    @property
    def dimension(self):
        return self.x.dimension

    def to(self, unit: str) -> Vector3D:
        """Return this vector expressed in the requested unit."""
        return Vector3D(
            self.x.to(unit),
            self.y.to(unit),
            self.z.to(unit),
        )

    def __add__(self, other: Vector3D) -> Vector3D:
        if not isinstance(other, Vector3D):
            return NotImplemented

        return Vector3D(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __sub__(self, other: Vector3D) -> Vector3D:
        if not isinstance(other, Vector3D):
            return NotImplemented

        return Vector3D(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )

    def __mul__(self, scalar: int | float) -> Vector3D:
        if not isinstance(scalar, (int, float)):
            return NotImplemented

        return Vector3D(
            self.x * scalar,
            self.y * scalar,
            self.z * scalar,
        )

    def __rmul__(self, scalar: int | float) -> Vector3D:
        return self.__mul__(scalar)

    def __neg__(self) -> Vector3D:
        return Vector3D(
            -self.x,
            -self.y,
            -self.z,
        )

    @property
    def components(self) -> tuple[Quantity, Quantity, Quantity]:
        return self.x, self.y, self.z

    def dot(self, other: Vector3D) -> Quantity:
        """
        Return the scalar dot product with another vector.

        The vectors must have the same physical dimension.
        The resulting Quantity therefore has the squared dimension
        of the vector components.
        """
        if not isinstance(other, Vector3D):
            raise TypeError("other must be a Vector3D")

        if self.dimension != other.dimension:
            raise ValueError("Vector dimensions must match")

        other = other.to(self.x.unit)

        return (
            self.x * other.x
            + self.y * other.y
            + self.z * other.z
        )

    def norm(self) -> Quantity:
        """
        Return the Euclidean magnitude of the vector.
        """
        return Quantity(
            sqrt(
                self.x.value ** 2
                + self.y.value ** 2
                + self.z.value ** 2
            ),
            self.x.unit,
            _dimension=self.dimension,
        )

    def normalized(self) -> Vector3D:
        """
        Return a dimensionless unit vector in the same direction.

        Raises ValueError for a zero vector.
        """
        magnitude = self.norm()

        if magnitude.value == 0:
            raise ValueError("zero vector cannot be normalized")

        return Vector3D(
            self.x / magnitude,
            self.y / magnitude,
            self.z / magnitude,
        )

    def cross(self, other: Vector3D) -> Vector3D:
        """
        Return the vector cross product with another vector.

        The vectors must have the same physical dimension.
        Each resulting component therefore has the squared dimension
        of the input vectors.
        """
        if not isinstance(other, Vector3D):
            raise TypeError("other must be a Vector3D")

        if self.dimension != other.dimension:
            raise ValueError("Vector dimensions must match")

        other = other.to(self.x.unit)

        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )
