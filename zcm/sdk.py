"""Thin Python SDK around the local SCM service facade."""
from .chemistry_api import ChemistryAPI

class ZCMClient:
    def __init__(self): self.chemistry=ChemistryAPI()
