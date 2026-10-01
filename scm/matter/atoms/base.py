from __future__ import annotations

from dataclasses import dataclass

from scm.matter.composition import Composition
from scm.matter.electrons import (
    ElectronConfiguration,
    ground_state_configuration,
)
from scm.matter.species import ChemicalSpecies
from scm.matter.nuclei import Nucleus
from scm.matter.isotopes import Isotope


@dataclass(frozen=True)
class Atom(ChemicalSpecies):
    """
    Atomic chemical species.

    Atomic number defines elemental identity.
    Electron count defines the electronic charge state.

    Element names and symbols are resolved through the knowledge layer;
    the structural matter layer retains atomic number as the identity.
    """

    atomic_number: int = 1
    electron_count: int | None = None
    symbol: str | None = None
    mass_number: int | None = None

    def __post_init__(self) -> None:
        if self.mass_number is not None:
            if isinstance(self.mass_number, bool) or not isinstance(self.mass_number, int):
                raise TypeError("mass_number must be an integer")
            if self.mass_number < self.atomic_number:
                raise ValueError("mass_number cannot be less than atomic_number")

        if not isinstance(self.atomic_number, int):
            raise TypeError("atomic_number must be an integer")

        if not 1 <= self.atomic_number <= 118:
            raise ValueError(
                "atomic_number must be between 1 and 118"
            )

        electron_count = self.electron_count

        if electron_count is None:
            electron_count = self.atomic_number
            object.__setattr__(
                self,
                "electron_count",
                electron_count,
            )

        if not isinstance(electron_count, int):
            raise TypeError(
                "electron_count must be an integer"
            )

        if electron_count < 0:
            raise ValueError(
                "electron_count cannot be negative"
            )

        expected_charge = (
            self.atomic_number - electron_count
        )

        if expected_charge != self.charge_number:
            raise ValueError(
                "charge_number does not match "
                "atomic_number and electron_count"
            )

        if self.symbol is not None:
            if not isinstance(self.symbol, str):
                raise TypeError("symbol must be a string")

            if not self.symbol.strip():
                raise ValueError("symbol must not be empty")

        super().__post_init__()

    @classmethod
    def create(
        cls,
        atomic_number: int,
        *,
        electron_count: int | None = None,
        symbol: str | None = None,
        mass_number: int | None = None,
    ) -> "Atom":
        """
        Construct an atom from atomic identity.

        Atomic number is the authoritative structural identity.
        If no symbol is supplied, the canonical chemical symbol is
        resolved from knowledge.elements.
        """

        if not isinstance(atomic_number, int):
            raise TypeError("atomic_number must be an integer")

        if not 1 <= atomic_number <= 118:
            raise ValueError(
                "atomic_number must be between 1 and 118"
            )

        # Resolve the canonical element record from scientific knowledge.
        #
        # Lazy import avoids coupling the matter package to the knowledge
        # registry during module initialization.
        from knowledge.elements import get_element

        element_record = get_element(atomic_number)
        canonical_symbol = element_record.symbol

        if symbol is None:
            symbol = canonical_symbol
        else:
            if not isinstance(symbol, str):
                raise TypeError("symbol must be a string")

            symbol = symbol.strip()

            if not symbol:
                raise ValueError("symbol must not be empty")

            # A supplied symbol must agree with the atomic identity.
            if symbol.casefold() != canonical_symbol.casefold():
                raise ValueError(
                    f"symbol {symbol!r} does not match "
                    f"atomic number {atomic_number} "
                    f"({canonical_symbol})"
                )

            symbol = canonical_symbol

        if electron_count is None:
            electron_count = atomic_number

        charge_number = atomic_number - electron_count

        composition = Composition.from_mapping(
            {canonical_symbol: 1}
        )

        return cls(
            composition=composition,
            charge_number=charge_number,
            atomic_number=atomic_number,
            electron_count=electron_count,
            symbol=canonical_symbol,
            mass_number=mass_number,
        )

    @classmethod
    def from_isotope(
        cls,
        isotope: Isotope,
        *,
        electron_count: int | None = None,
    ) -> "Atom":
        """Construct an atomic electronic state from a nuclear isotope identity."""
        if not isinstance(isotope, Isotope):
            raise TypeError("isotope must be an Isotope")
        return cls.create(
            isotope.atomic_number,
            electron_count=electron_count,
            mass_number=isotope.mass_number,
        )

    @property
    def nucleus(self) -> Nucleus:
        """Return the nuclear identity represented by this atom."""
        if self.mass_number is None:
            raise ValueError("nucleus is unavailable for an atom without isotope identity")
        return Nucleus.from_mass_number(self.atomic_number, self.mass_number)

    @property
    def isotope(self) -> Isotope | None:
        """Return isotope identity when mass number is explicitly modeled."""
        if self.mass_number is None:
            return None
        return Isotope.from_za(self.atomic_number, self.mass_number)

    @property
    def neutron_count(self) -> int | None:
        """Return neutron count when isotope identity is explicit."""
        if self.mass_number is None:
            return None
        return self.mass_number - self.atomic_number

    @property
    def proton_count(self) -> int:
        return self.atomic_number

    @property
    def configuration(self) -> ElectronConfiguration:
        return ground_state_configuration(
            self.atomic_number,
            self.electron_count,
        )

    @property
    def valence_electron_count(self) -> int:
        return self.configuration.valence_electron_count

    @property
    def notation(self) -> str:
        return self.configuration.notation()

    @property
    def is_neutral_atom(self) -> bool:
        return self.charge_number == 0

    def __str__(self) -> str:
        if self.charge_number == 0:
            return self.symbol or f"Z={self.atomic_number}"

        return f"{self.symbol or f'Z={self.atomic_number}'}{self.charge_symbol}"
