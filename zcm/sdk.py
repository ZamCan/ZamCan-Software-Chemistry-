"""Python SDK around the local scientific engines and notebook."""
from scm.notebook import LabNotebook
from scm.robotics import simulate_transfers
from zcm.calculations import calculate, stoichiometry, titrate

from .chemistry_api import ChemistryAPI


class ZCMClient:
    def __init__(self):
        self.chemistry = ChemistryAPI()

    calculate = staticmethod(calculate)
    stoichiometry = staticmethod(stoichiometry)
    titrate = staticmethod(titrate)
    open_notebook = staticmethod(LabNotebook)
    simulate_transfers = staticmethod(simulate_transfers)
