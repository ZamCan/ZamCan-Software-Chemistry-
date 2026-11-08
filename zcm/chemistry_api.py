from scm.chemistry import assign_oxidation_states, solve_stoichiometry, gibbs_free_energy
from scm.chemistry.concentration import diluted_molarity, molarity, molarity_from_mass
from scm.engines import reaction_quotient, titration, material_balance

class ChemistryAPI:
    oxidation_states = staticmethod(assign_oxidation_states)
    stoichiometry = staticmethod(solve_stoichiometry)
    gibbs = staticmethod(gibbs_free_energy)
    quotient = staticmethod(reaction_quotient)
    molarity = staticmethod(molarity)
    molarity_from_mass = staticmethod(molarity_from_mass)
    diluted_molarity = staticmethod(diluted_molarity)
    titration = staticmethod(titration)
    material_balance = staticmethod(material_balance)
