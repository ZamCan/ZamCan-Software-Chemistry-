"""Python SDK around the local scientific engines and notebook."""
from scm.chemistry.analytical.qualitative import identify_salt, observation_catalogue
from scm.notebook import LabNotebook
from scm.robotics import simulate_transfers
from zcm.calculations import (
    calculate, calculate_dilution, calculate_mass_molarity, calculate_molarity, stoichiometry, titrate,
)

from .chemistry_api import ChemistryAPI
from .practical_sheet import render_practical_sheet
from .reasoning import infer_concentration


class ZCMClient:
    def __init__(self):
        self.chemistry = ChemistryAPI()

    calculate = staticmethod(calculate)
    stoichiometry = staticmethod(stoichiometry)
    molarity = staticmethod(calculate_molarity)
    mass_molarity = staticmethod(calculate_mass_molarity)
    dilute = staticmethod(calculate_dilution)
    titrate = staticmethod(titrate)
    infer_concentration = staticmethod(infer_concentration)
    identify_salt = staticmethod(identify_salt)
    ion_tests = staticmethod(observation_catalogue)
    render_practical_sheet = staticmethod(render_practical_sheet)
    open_notebook = staticmethod(LabNotebook)
    simulate_transfers = staticmethod(simulate_transfers)
