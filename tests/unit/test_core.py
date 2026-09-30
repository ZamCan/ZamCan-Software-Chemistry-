from scm.core import (
    Conditions,
    Evidence,
    EvidenceType,
    Quantity,
    ScientificProperty,
    ScientificStatus,
    Uncertainty,
)


def test_quantity():
    q = Quantity(660.32, "K")
    assert q.value == 660.32
    assert q.unit == "K"


def test_scientific_property():
    prop = ScientificProperty(
        name="melting point",
        quantity=Quantity(933.47, "K"),
        status=ScientificStatus.KNOWN,
        conditions=Conditions(
            pressure=Quantity(101325, "Pa"),
        ),
        uncertainty=Uncertainty(absolute=0.01),
        evidence=Evidence(
            evidence_type=EvidenceType.REFERENCE,
            source="scientific reference",
        ),
    )

    assert prop.name == "melting point"
    assert prop.quantity.unit == "K"
    assert prop.status == ScientificStatus.KNOWN
    assert prop.conditions.pressure.unit == "Pa"
    assert prop.primary_evidence.evidence_type == EvidenceType.REFERENCE


def test_uncertainty_confidence_validation():
    Uncertainty(confidence=0.95)

    try:
        Uncertainty(confidence=1.5)
        assert False
    except ValueError:
        pass


def test_action_dimension_maps_to_joule_second():
    from scm.core import Quantity

    action = Quantity(1, "J") * Quantity(1, "s")

    assert action.unit == "J·s"
    assert action.value == 1
