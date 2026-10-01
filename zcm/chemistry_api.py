from scm.chemistry import assign_oxidation_states, solve_stoichiometry, gibbs_free_energy
from scm.engines import reaction_quotient, titration, material_balance

class ChemistryAPI:
    oxidation_states = staticmethod(assign_oxidation_states)
    stoichiometry = staticmethod(solve_stoichiometry)
    gibbs = staticmethod(gibbs_free_energy)
    quotient = staticmethod(reaction_quotient)
    titration = staticmethod(titration)
    material_balance = staticmethod(material_balance)
