import json
import subprocess
import sys

import pytest

from scm.chemistry.analytical.base import Observation
from zcm.sdk import ZCMClient


def test_qualitative_formula_from_two_independent_ion_signatures():
    result = ZCMClient().identify_salt([
        Observation("sodium_hydroxide", "white_precipitate"),
        Observation("excess_sodium_hydroxide", "white_precipitate_dissolves"),
        Observation("barium_chloride_hydrochloric_acid", "white_precipitate"),
    ])
    assert result["status"] == "supported_hypothesis"
    assert result["formula"] == "Al2(SO4)3"
    assert result["candidates"]["cation"] == [{"formula": "Al", "charge": 3}]
    assert result["reference"].startswith("https://www.aqa.org.uk/")


def test_qualitative_distinguishes_missing_ambiguous_and_conflicting_evidence():
    identify = ZCMClient().identify_salt
    white = Observation("sodium_hydroxide", "white_precipitate")
    chloride = Observation("silver_nitrate_nitric_acid", "white_precipitate")
    for observations, status in (
        ([white, Observation("silver_nitrate_nitric_acid", "no_observable_change")], "needs_evidence"),
        ([white, chloride], "ambiguous"),
        ([white, Observation("sodium_hydroxide", "blue_precipitate"), chloride], "conflicting_evidence"),
        ([Observation("flame", "yellow"), Observation("sodium_hydroxide", "blue_precipitate"), chloride],
         "conflicting_evidence"),
    ):
        result = identify(observations)
        assert result["status"] == status
        assert "formula" not in result
    assert identify([white, chloride])["additional_evidence"]["cation"] == ["excess_sodium_hydroxide"]
    with pytest.raises(ValueError, match="Unsupported outcome"):
        identify([Observation("flame", "white_precipitate")])


def test_cli_salt_analysis_is_sample_scoped_and_links_source_records(tmp_path):
    db = tmp_path / "lab.db"
    notebook = ZCMClient().open_notebook(db)
    experiment = notebook.create("Unknown salts", "Identify both ions").experiment_id

    def lab(*args):
        return json.loads(subprocess.check_output([
            sys.executable, "-m", "zcm.cli", "--db", str(db), "lab", *args,
        ], text=True))

    source = lab("observe-ion", experiment, "a", "flame", "yellow")["record_sequence"]
    lab("observe-ion", experiment, "b", "flame", "lilac")
    lab("observe-ion", experiment, "a", "silver_nitrate_nitric_acid", "white_precipitate")
    result = lab("identify-salt", experiment, "a", "--save")
    assert result["formula"] == "NaCl"
    assert result["observations"][0]["record_sequence"] == source
    assert len(result["observations"]) == 2
    last = notebook.export(experiment)["events"][-1]
    assert last["kind"] == "salt_analysis"
    assert last["sequence"] == result.pop("record_sequence")
    assert last["payload"] == result
