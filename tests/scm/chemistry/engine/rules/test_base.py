import pytest

from scm.chemistry.engine.rules import Rule, RuleResult, RuleStatus


def test_rule_status_values():
    assert RuleStatus.PASSED.value == "passed"
    assert RuleStatus.FAILED.value == "failed"
    assert RuleStatus.INCONCLUSIVE.value == "inconclusive"
    assert RuleStatus.NOT_APPLICABLE.value == "not_applicable"


def test_rule_result_passed():
    result = RuleResult(
        status=RuleStatus.PASSED,
        reason="constraint satisfied",
    )

    assert result.passed is True
    assert result.failed is False
    assert result.conclusive is True


def test_rule_result_failed():
    result = RuleResult(
        status=RuleStatus.FAILED,
        reason="constraint violated",
    )

    assert result.passed is False
    assert result.failed is True
    assert result.conclusive is True


def test_rule_result_inconclusive():
    result = RuleResult(
        status=RuleStatus.INCONCLUSIVE,
        reason="insufficient information",
    )

    assert result.passed is False
    assert result.failed is False
    assert result.conclusive is False


def test_rule_result_not_applicable():
    result = RuleResult(
        status=RuleStatus.NOT_APPLICABLE,
        reason="rule does not apply",
    )

    assert result.passed is False
    assert result.failed is False
    assert result.conclusive is False


def test_rule_result_can_store_details():
    result = RuleResult(
        status=RuleStatus.PASSED,
        reason="constraint satisfied",
        details={"element": "H", "difference": 0},
    )

    assert result.details == {
        "element": "H",
        "difference": 0,
    }


def test_rule_has_default_description():
    rule = Rule()

    assert rule.describe() == "unnamed_rule"


def test_rule_default_can_apply():
    rule = Rule()

    assert rule.can_apply("anything") is True


def test_base_rule_requires_evaluate_implementation():
    rule = Rule()

    with pytest.raises(NotImplementedError):
        rule.evaluate()
