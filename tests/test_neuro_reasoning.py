import unittest
from zcm.neuro_reasoning import Evidence, Rule, ScientificReasoner

class ReasoningTests(unittest.TestCase):
    def test_chain(self):
        engine = ScientificReasoner([
            Rule("transcription", ("dna_template", "transcription_observed"), "rna_supported", .9),
            Rule("translation", ("rna_supported", "translation_observed"), "protein_supported", .8),
        ])
        result = engine.infer([
            Evidence("dna_template", "sample A", 1, "observed"),
            Evidence("transcription_observed", "assay B", .9, "observed"),
            Evidence("translation_observed", "assay C", .95, "observed"),
        ])
        p = result["protein_supported"]
        self.assertAlmostEqual(p.score, .648)
        self.assertEqual(p.status, "predicted")
        self.assertEqual(p.trace, ("transcription", "translation"))
        self.assertEqual(len(p.sources), 3)

    def test_missing_premise(self):
        engine = ScientificReasoner([Rule("r", ("a", "b"), "c")])
        self.assertNotIn("c", engine.infer([Evidence("a", "source", 1, "observed")]))

    def test_conflict(self):
        e = Evidence("a", "source", 1, "observed")
        with self.assertRaises(ValueError):
            ScientificReasoner().infer([e, e])

    def test_invalid_score(self):
        with self.assertRaises(ValueError):
            Evidence("a", "source", float("nan"), "observed")

if __name__ == "__main__":
    unittest.main()
