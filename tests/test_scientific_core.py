import unittest
from scm.scientific_core import (
    composition, balance, Measurement, titration_concentration, ChemistryInputError
)

class ScientificCoreTests(unittest.TestCase):
    def test_nested_formula(self):
        self.assertEqual(composition("Ca3(PO4)2"), {"Ca": 3, "P": 2, "O": 8})
    def test_invalid_formula(self):
        for value in ("", "H2O)", "(OH", "H0", "2H2O", "Mg()2"):
            with self.subTest(value=value):
                with self.assertRaises(ChemistryInputError):
                    composition(value)
    def test_water_balancing(self):
        result = balance(["H2", "O2"], ["H2O"])
        self.assertEqual(result["reactants"], {"H2": 2, "O2": 1})
        self.assertEqual(result["products"], {"H2O": 2})
    def test_combustion(self):
        result = balance(["C2H6", "O2"], ["CO2", "H2O"])
        self.assertEqual(result["reactants"], {"C2H6": 2, "O2": 7})
        self.assertEqual(result["products"], {"CO2": 4, "H2O": 6})
    def test_impossible_balance(self):
        with self.assertRaises(ChemistryInputError):
            balance(["H2"], ["H2O"])
    def test_titration(self):
        result = titration_concentration(
            Measurement(25.0, 0.03, "mL"),
            Measurement(20.0, 0.04, "mL"),
            Measurement(0.1000, 0.0002, "mol/L"))
        self.assertAlmostEqual(result["value"], 0.08)
        self.assertGreater(result["standard_uncertainty"], 0)
    def test_reject_inconsistent_units(self):
        with self.assertRaises(ChemistryInputError):
            titration_concentration(Measurement(25, 0, "mL"),
                Measurement(0.02, 0, "L"), Measurement(0.1, 0, "mol/L"))

if __name__ == "__main__":
    unittest.main()
