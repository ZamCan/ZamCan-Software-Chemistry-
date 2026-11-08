"""Interpret recorded single-salt observations with a traceable rule set."""
from collections.abc import Iterable
from dataclasses import asdict
from math import gcd

from knowledge.compounds.qualitative import CATALOGUE_VERSION, REFERENCE, SIGNATURES
from scm.chemistry.analytical.base import Observation
from scm.chemistry.reactions import parse_formula


_UNINFORMATIVE = {"inconclusive", "no_observable_change"}


def observation_catalogue() -> dict:
    return {
        "version": CATALOGUE_VERSION,
        "reference": REFERENCE,
        "tests": {
            test: [*outcomes, *sorted(_UNINFORMATIVE)]
            for test, outcomes in SIGNATURES.items()
        },
    }


def validate_observation(observation: Observation) -> None:
    if not isinstance(observation, Observation):
        raise TypeError("Expected an Observation.")
    if observation.test not in SIGNATURES:
        raise ValueError(f"Unknown qualitative test: {observation.test}")
    if observation.observation not in SIGNATURES[observation.test] and observation.observation not in _UNINFORMATIVE:
        raise ValueError(f"Unsupported outcome for {observation.test}: {observation.observation}")


def _ion(formula: str, charge: int) -> dict:
    return {"formula": formula, "charge": charge}


def _formula(cation: tuple[str, int], anion: tuple[str, int]) -> str:
    divisor = gcd(cation[1], -anion[1])

    def term(formula, count):
        if count == 1:
            return formula
        if sum(parse_formula(formula).values()) > 1:
            return f"({formula}){count}"
        return f"{formula}{count}"

    return term(cation[0], -anion[1] // divisor) + term(anion[0], cation[1] // divisor)


def _evidence_options(group: str, candidates: list, observed_tests: set[str]) -> list[str]:
    options = []
    for test, outcomes in SIGNATURES.items():
        if test in observed_tests:
            continue
        profiles = [set(ions) for ions in outcomes.values()]
        test_group = "cation" if next(iter(profiles[0]))[1] > 0 else "anion"
        if test_group != group:
            continue
        if not candidates:
            if test != "excess_sodium_hydroxide":
                options.append(test)
        elif len(candidates) > 1:
            remaining = set(candidates)
            matches = [profile & remaining for profile in profiles]
            if set.union(*matches) == remaining and all(match != remaining for match in matches):
                options.append(test)
    return options


def identify_salt(observations: Iterable[Observation]) -> dict:
    """Find jointly supported ions without treating missing or negative tests as proof."""
    outcomes_by_test = {}
    supported = {"cation": [], "anion": []}
    trace = []
    for index, observation in enumerate(observations, start=1):
        validate_observation(observation)
        outcome = observation.observation
        if outcome != "inconclusive":
            outcomes_by_test.setdefault(observation.test, set()).add(outcome)
        signatures = SIGNATURES[observation.test].get(outcome, ())
        row = {
            "observation_number": index,
            **asdict(observation),
            "supported_ions": [_ion(*ion) for ion in signatures],
        }
        if signatures:
            group = "cation" if signatures[0][1] > 0 else "anion"
            supported[group].append(set(signatures))
        trace.append(row)

    conflicting_tests = [test for test, outcomes in outcomes_by_test.items() if len(outcomes) > 1]
    candidates = {
        group: sorted(set.intersection(*sets)) if sets else []
        for group, sets in supported.items()
    }
    conflicting_groups = [group for group, sets in supported.items() if sets and not candidates[group]]
    missing = [group for group, sets in supported.items() if not sets]
    result = {
        "method": "single_salt_qualitative_analysis",
        "scope": "Single salts and positive signatures in the referenced catalogue.",
        "catalogue_version": CATALOGUE_VERSION,
        "reference": REFERENCE,
        "observations": trace,
        "candidates": {group: [_ion(*ion) for ion in ions] for group, ions in candidates.items()},
        "missing_ion_evidence": missing,
        "conflicting_tests": conflicting_tests,
        "conflicting_ion_evidence": conflicting_groups,
    }
    if conflicting_tests or conflicting_groups:
        return {**result, "status": "conflicting_evidence"}
    result["additional_evidence"] = {
        group: _evidence_options(group, ions, set(outcomes_by_test))
        for group, ions in candidates.items()
        if len(ions) != 1
    }
    if missing:
        return {**result, "status": "needs_evidence"}
    if any(len(ions) > 1 for ions in candidates.values()):
        return {**result, "status": "ambiguous"}
    return {
        **result,
        "status": "supported_hypothesis",
        "formula": _formula(candidates["cation"][0], candidates["anion"][0]),
    }
