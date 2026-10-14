from scm.chemistry import assign_oxidation_states, solve_stoichiometry, gibbs_free_energy
from scm.engines import reaction_quotient, titration, Stream, material_balance
from scm.validation import finite_number, validate_unique
from scm.chemistry.reaction_plausibility import assess_reaction, PlausibilityStatus

def test_oxidation_water():
    r=assign_oxidation_states('H2O')
    assert r.status.value=='resolved'
    assert [x.state for x in r.assignments]==[1,-2]

def test_limiting_reagent():
    r=solve_stoichiometry({'H2':4,'O2':1},{'H2O':0},{'H2':2,'O2':1,'H2O':2})
    assert r.limiting_reactants==('O2',)

def test_gibbs():
    assert gibbs_free_energy(1000,2,300)==400

def test_equilibrium_quotient():
    assert reaction_quotient({'C':2},{'A':1}).quotient==2

def test_titration():
    assert titration(0.1,0.01,0.02).concentration==0.05

def test_material_balance():
    r=material_balance((Stream('in',{'A':2}),),(Stream('out',{'A':2}),))
    assert r.balanced

def test_scientific_input_validation():
    assert finite_number(float('nan'), 'temperature')
    assert not finite_number(298.15, 'temperature')
    assert validate_unique(['H2','O2']).valid is True
    assert not validate_unique(['H2','H2']).valid

def test_balanced_equation_is_not_proof_of_reaction():
    result=assess_reaction(atom_balance=True,charge_balance=True)
    assert result.status is PlausibilityStatus.INSUFFICIENT_DATA

def test_elemental_oxygen_oxidation_state_is_zero():
    result=assign_oxidation_states('O2')
    assert result.status.value=='resolved'
    assert result.assignments[0].state==0
