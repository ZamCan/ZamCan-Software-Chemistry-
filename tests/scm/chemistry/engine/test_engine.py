import pytest

from scm.chemistry.engine import (
    CalculationResult,
    ChemistryContext,
    ChemistryModule,
    ChemistryModuleRegistry,
    ResultStatus,
)


class DummyModule(ChemistryModule):
    name = "dummy"

    def capabilities(self):
        return frozenset({
            "calculation",
            "chemistry",
        })


def test_success_result():
    result = CalculationResult(
        status=ResultStatus.SUCCESS,
        value=42,
    )

    assert result.successful
    assert result.usable
    assert result.value == 42


def test_warning_result_is_usable():
    result = CalculationResult(
        status=ResultStatus.WARNING,
        value=42,
        message="uncertainty present",
    )

    assert not result.successful
    assert result.usable


def test_context_composition():
    context = ChemistryContext()
    context = context.with_condition("25 °C")
    context = context.with_assumption("ideal solution")

    assert context.conditions == ("25 °C",)
    assert context.assumptions == ("ideal solution",)


def test_module_capability():
    module = DummyModule()

    assert module.can_handle("calculation")
    assert not module.can_handle("robotics")


def test_registry():
    registry = ChemistryModuleRegistry()
    module = DummyModule()

    registry.register(module)

    assert registry.get("dummy") is module
    assert registry.find_capability("chemistry") == (module,)


def test_duplicate_module_rejected():
    registry = ChemistryModuleRegistry()

    registry.register(DummyModule())

    with pytest.raises(ValueError):
        registry.register(DummyModule())
