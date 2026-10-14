from scm.properties.registry import PropertyRecord, PropertyRegistry, PropertyLookupStatus
from scm.chemistry.reaction_plausibility import assess_reaction, PlausibilityStatus
from scm.validation import finite_number, validate_unique

def test_property_registry_preserves_provenance_and_resolves():
    registry=PropertyRegistry()
    registry.add(PropertyRecord('H2O','boiling_point',373.15,'K',(('pressure','101325 Pa'),),'source-A'))
    result=registry.lookup('h2o','BOILING_POINT',{'pressure':'101325 pa'})
    assert result.status is PropertyLookupStatus.RESOLVED
    assert result.records[0].source=='source-A'

def test_property_registry_reports_conflicting_values():
    registry=PropertyRegistry()
    registry.add(PropertyRecord('H2O','density',1.0,'g/mL',source='A'))
    registry.add(PropertyRecord('H2O','density',0.9,'g/mL',source='B'))
    assert registry.lookup('H2O','density').status is PropertyLookupStatus.AMBIGUOUS

def test_property_registry_not_found():
    assert PropertyRegistry().lookup('X','unknown').status is PropertyLookupStatus.NOT_FOUND

def test_input_validation_rejects_boolean_as_number():
    assert finite_number(True,'value')

def test_reaction_requires_evidence_beyond_balance():
    assert assess_reaction(atom_balance=True,charge_balance=True).status is PlausibilityStatus.INSUFFICIENT_DATA
