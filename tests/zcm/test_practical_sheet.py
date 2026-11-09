import subprocess
import sys

from scm.chemistry.analytical.base import Observation
from scm.lab_records import Measurement
from zcm.sdk import ZCMClient


def test_printable_sheet_preserves_observations_sources_and_escaped_notes(tmp_path):
    client = ZCMClient()
    db = tmp_path / "practical.db"
    notebook = client.open_notebook(db)
    experiment = notebook.create("Salt <A>", "Identify the ions").experiment_id
    measure = notebook.record_measurement(experiment, Measurement("mass", 0, "g", uncertainty=0))
    notebook.record_calculation(experiment, notebook.summarize(experiment, "mass", "g"))
    flame = notebook.record_ion_observation(experiment, "A", Observation("flame", "yellow"))
    notebook.record_ion_observation(
        experiment, "A", Observation("silver_nitrate_nitric_acid", "white_precipitate")
    )
    notebook.analyze_salt(experiment, "A", save=True)
    notebook.record_note(experiment, "<script>alert(1)</script>", conclusion=True)

    snapshot = notebook.export(experiment)
    html = client.render_practical_sheet(snapshot)
    assert html.startswith("<!doctype html>")
    assert "@media print" in html
    assert "Salt &lt;A&gt;" in html
    assert "NaCl" in html
    assert "supported hypothesis" in html
    assert f'href="#record-{measure}"' in html
    assert f'href="#record-{flame}"' in html
    assert f'id="record-{flame}"' in html
    assert "<td>0</td>" in html
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert "<script>" not in html
    assert subprocess.check_output([
        sys.executable, "-m", "zcm.cli", "--db", str(db), "lab", "sheet", experiment,
    ], text=True) == html
    assert notebook.export(experiment) == snapshot
