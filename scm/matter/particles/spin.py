from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import sqrt

from scm.core import Quantity


@dataclass(frozen=True)
class Spin:
    """
    Intrinsic quantum spin of a particle.

    quantum_number:
        Intrinsic spin quantum number s.

        Physical spin quantum numbers are non-negative integers
        or half-integers:

            0, 1/2, 1, 3/2, 2, ...

    projection:
        Optional spin projection quantum number m_s.
        If supplied, it must satisfy:

            -s <= m_s <= s

        and differ from -s in integer steps.
    """

    quantum_number: Fraction
    projection: Fraction | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.quantum_number, Fraction):
            raise TypeError(
                "spin quantum number must be a Fraction"
            )

        if self.quantum_number < 0:
            raise ValueError(
                "spin quantum number must be non-negative"
            )

        # Physical spin quantum numbers must be integer
        # or half-integer values. Therefore 2s must be integer.
        if (2 * self.quantum_number).denominator != 1:
            raise ValueError(
                "spin quantum number must be an integer "
                "or half-integer"
            )

        if self.projection is not None:
            if not isinstance(self.projection, Fraction):
                raise TypeError(
                    "spin projection must be a Fraction"
                )

            if self.projection < -self.quantum_number:
                raise ValueError(
                    "spin projection cannot be below -s"
                )

            if self.projection > self.quantum_number:
                raise ValueError(
                    "spin projection cannot exceed +s"
                )

            difference = self.projection + self.quantum_number

            if difference.denominator != 1:
                raise ValueError(
                    "spin projection must differ from -s "
                    "in integer steps"
                )

    @property
    def angular_momentum_magnitude(self) -> Quantity:
        """
        Magnitude of intrinsic spin angular momentum:

            |S| = sqrt(s(s+1)) * ħ

        The numerical value is represented in J·s.
        """
        from knowledge.constants.physical import hbar

        factor = sqrt(
            float(
                self.quantum_number
                * (self.quantum_number + 1)
            )
        )

        return factor * hbar

    @property
    def allowed_projections(self) -> tuple[Fraction, ...]:
        """
        Return all allowed m_s values for this spin.
        """
        start = -self.quantum_number
        count = int(2 * self.quantum_number)

        return tuple(
            start + Fraction(i, 1)
            for i in range(count + 1)
        )
