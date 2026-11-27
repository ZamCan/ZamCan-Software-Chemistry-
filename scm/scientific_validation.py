"""Validation of numerical benchmarks, not experimental confirmation."""
from dataclasses import dataclass
from math import isfinite, fsum
from typing import Sequence

@dataclass(frozen=True)
class BenchmarkResult:
    count: int
    mae: float
    maximum_error: float
    unit: str
    reference_origin: str
    dataset_version: str
    passed: bool

def benchmark(predictions: Sequence[float], references: Sequence[float], *,
              unit: str, reference_origin: str, dataset_version: str,
              mae_limit: float, max_error_limit: float) -> BenchmarkResult:
    """Compare paired values in the same explicitly declared unit.
    Caller must establish pairing, independence and unit compatibility.
    Passing is numerical agreement only, not proof of chemical validity.
    """
    if not predictions or len(predictions) != len(references):
        raise ValueError("Nonempty paired values required")
    if not unit.strip() or not dataset_version.strip():
        raise ValueError("Unit and dataset version required")
    if reference_origin not in ("experimental", "computational", "analytical"):
        raise ValueError("Unsupported reference origin")
    if any(not isfinite(x) or x < 0 for x in (mae_limit, max_error_limit)):
        raise ValueError("Finite nonnegative limits required")
    errors = []
    for p, r in zip(predictions, references):
        if not isfinite(p) or not isfinite(r):
            raise ValueError("Nonfinite benchmark value")
        e = abs(p-r)
        if not isfinite(e):
            raise ValueError("Nonfinite error")
        errors.append(e)
    mae = fsum(e / len(errors) for e in errors)
    maximum = max(errors)
    return BenchmarkResult(len(errors), mae, maximum, unit, reference_origin,
                           dataset_version, mae <= mae_limit and maximum <= max_error_limit)

def conservation_residual(reactants, products):
    """Each side contains (positive integer coefficient, atom-count mapping,
    integer charge). Returns products minus reactants; zero is necessary,
    not sufficient, for a chemically possible reaction.
    Atom keys may encode isotope identity. No formula parsing is implied.
    """
    residual = {}
    charge = 0
    for sign, side in ((-1, reactants), (1, products)):
        if not side:
            raise ValueError("Both reaction sides required")
        for coefficient, atoms, species_charge in side:
            if type(coefficient) is not int or coefficient <= 0 or type(species_charge) is not int:
                raise ValueError("Invalid coefficient or charge")
            if not atoms and species_charge == 0:
                raise ValueError("Empty neutral species")
            for atom, count in atoms.items():
                if not isinstance(atom, str) or not atom or type(count) is not int or count <= 0:
                    raise ValueError("Invalid atom count")
                residual[atom] = residual.get(atom, 0) + sign * coefficient * count
            charge += sign * coefficient * species_charge
    return {"atoms": {k:v for k,v in residual.items() if v}, "charge": charge}
