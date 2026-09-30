from __future__ import annotations

from dataclasses import dataclass

from .configuration import ElectronConfiguration
from .occupancy import SubshellOccupancy


# Canonical aufbau-style ordering used by the model.
# This is an energy-ordering model, not a claim that every
# many-electron atom follows a simple hydrogenic ordering.
FILLING_ORDER: tuple[tuple[int, str, int], ...] = (
    (1, "s", 2),
    (2, "s", 2),
    (2, "p", 6),
    (3, "s", 2),
    (3, "p", 6),
    (4, "s", 2),
    (3, "d", 10),
    (4, "p", 6),
    (5, "s", 2),
    (4, "d", 10),
    (5, "p", 6),
    (6, "s", 2),
    (4, "f", 14),
    (5, "d", 10),
    (6, "p", 6),
    (7, "s", 2),
    (5, "f", 14),
    (6, "d", 10),
    (7, "p", 6),
)


# Known ground-state configuration adjustments represented
# explicitly by this model.
GROUND_STATE_EXCEPTIONS: dict[int, tuple[tuple[int, str, int], ...]] = {
    24: ((4, "s", 1), (3, "d", 5)),    # Cr
    29: ((4, "s", 1), (3, "d", 10)),   # Cu
    41: ((5, "s", 1), (4, "d", 4)),    # Nb
    42: ((5, "s", 1), (4, "d", 5)),    # Mo
    44: ((5, "s", 1), (4, "d", 7)),    # Ru
    45: ((5, "s", 1), (4, "d", 8)),    # Rh
    46: ((5, "s", 0), (4, "d", 10)),   # Pd
    47: ((5, "s", 1), (4, "d", 10)),   # Ag
    57: ((6, "s", 2), (5, "d", 1)),    # La
    58: ((6, "s", 2), (4, "f", 1), (5, "d", 1)),  # Ce
    64: ((6, "s", 2), (4, "f", 7), (5, "d", 1)),  # Gd
    78: ((6, "s", 1), (4, "f", 14), (5, "d", 9)), # Pt
    79: ((6, "s", 1), (4, "f", 14), (5, "d", 10)),# Au
    89: ((7, "s", 2), (5, "f", 0), (6, "d", 1)),  # Ac
    90: ((7, "s", 2), (5, "f", 1), (6, "d", 1)),  # Th
    91: ((7, "s", 2), (5, "f", 2), (6, "d", 1)),  # Pa
    92: ((7, "s", 2), (5, "f", 3), (6, "d", 1)),  # U
    93: ((7, "s", 2), (5, "f", 4), (6, "d", 1)),  # Np
    96: ((7, "s", 2), (5, "f", 7), (6, "d", 0)),  # Cm
    103: ((7, "s", 2), (5, "f", 14), (6, "d", 1)),# Lr
}



# Backward-compatible public name. The canonical configuration container is now ElectronConfiguration.
GeneratedConfiguration = ElectronConfiguration


def _aufbau_counts(electron_count: int) -> list[tuple[int, str, int]]:
    remaining = electron_count
    result: list[tuple[int, str, int]] = []

    for n, subshell, capacity in FILLING_ORDER:
        if remaining <= 0:
            break

        count = min(remaining, capacity)
        result.append((n, subshell, count))
        remaining -= count

    if remaining:
        raise ValueError(
            f"electron_count {electron_count} exceeds supported configuration capacity"
        )

    return result


def _apply_ground_state_exception(
    atomic_number: int,
    counts: list[tuple[int, str, int]],
) -> list[tuple[int, str, int]]:
    exception = GROUND_STATE_EXCEPTIONS.get(atomic_number)

    if exception is None:
        return counts

    mapping = {(n, subshell): count for n, subshell, count in counts}

    for n, subshell, count in exception:
        mapping[(n, subshell)] = count

    # Preserve canonical filling-order order.
    return [
        (n, subshell, mapping[(n, subshell)])
        for n, subshell, _ in FILLING_ORDER
        if (n, subshell) in mapping and mapping[(n, subshell)] > 0
    ]


def generate_configuration(
    electron_count: int,
    *,
    atomic_number: int | None = None,
    enforce_hund: bool = True,
) -> ElectronConfiguration:
    """
    Generate a structured electron configuration.

    The generator now constructs SubshellOccupancy directly. Counts are
    intermediate generation data only and are not the authoritative state.
    """
    if isinstance(electron_count, bool) or not isinstance(electron_count, int):
        raise TypeError("electron_count must be an integer")

    if electron_count < 0:
        raise ValueError("electron_count cannot be negative")

    if atomic_number is not None:
        if isinstance(atomic_number, bool) or not isinstance(atomic_number, int):
            raise TypeError("atomic_number must be an integer")
        if not 1 <= atomic_number <= 118:
            raise ValueError("atomic_number must be between 1 and 118")

    counts = _aufbau_counts(electron_count)

    if atomic_number is not None and electron_count == atomic_number:
        counts = _apply_ground_state_exception(atomic_number, counts)

    occupancies = tuple(
        SubshellOccupancy.from_electron_count(
            n,
            subshell,
            count,
            enforce_hund=enforce_hund,
        )
        for n, subshell, count in counts
    )

    generated = ElectronConfiguration.from_occupancies(occupancies)

    if generated.electron_count != electron_count:
        raise RuntimeError(
            "generated configuration electron count does not match requested count"
        )

    generated.validate()
    return generated


def ground_state_configuration(
    atomic_number: int,
    electron_count: int | None = None,
) -> ElectronConfiguration:
    """
    Generate the ground-state-style electron configuration represented
    by this model.

    When electron_count is omitted, a neutral atom is assumed.

    When electron_count is supplied, the configuration is generated for
    that electron count. Neutral atoms receive the modeled atomic
    ground-state exceptions; ions use the electron-count configuration
    without incorrectly applying neutral-atom exceptions.
    """
    if electron_count is None:
        electron_count = atomic_number

    if isinstance(electron_count, bool) or not isinstance(electron_count, int):
        raise TypeError("electron_count must be an integer")

    if electron_count < 0:
        raise ValueError("electron_count cannot be negative")

    return generate_configuration(
        electron_count,
        atomic_number=(
            atomic_number
            if electron_count == atomic_number
            else None
        ),
        enforce_hund=True,
    )
