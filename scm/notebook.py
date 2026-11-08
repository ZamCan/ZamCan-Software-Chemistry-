"""Offline, append-only experiment records with structured evidence."""
from contextlib import closing, contextmanager
from dataclasses import asdict
from datetime import datetime, timezone
import json
from math import isfinite
from pathlib import Path
import sqlite3
from statistics import mean, stdev
from uuid import uuid4

from scm.chemistry.analytical.base import Observation
from scm.chemistry.analytical.qualitative import identify_salt, validate_observation
from scm.lab_records import Measurement
from scm.research import Dataset, Experiment


def _require_text(*values: str) -> None:
    if any(not isinstance(value, str) or not value.strip() for value in values):
        raise ValueError("Required text fields must be nonempty.")


class LabNotebook:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        with self._database() as connection:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS experiments (
                    id TEXT PRIMARY KEY, title TEXT NOT NULL,
                    objective TEXT NOT NULL, created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS events (
                    sequence INTEGER PRIMARY KEY, experiment_id TEXT NOT NULL
                        REFERENCES experiments(id),
                    kind TEXT NOT NULL, payload TEXT NOT NULL, created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS events_experiment
                    ON events(experiment_id, sequence);
            """)

    @contextmanager
    def _database(self):
        with closing(sqlite3.connect(self.path)) as connection, connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.row_factory = sqlite3.Row
            yield connection

    def create(self, title: str, objective: str) -> Experiment:
        _require_text(title, objective)
        experiment = Experiment(uuid4().hex, title.strip(), objective.strip())
        with self._database() as connection:
            connection.execute(
                "INSERT INTO experiments VALUES (?, ?, ?, ?)",
                (experiment.experiment_id, experiment.title, experiment.objective,
                 datetime.now(timezone.utc).isoformat()),
            )
        return experiment

    def list(self) -> list[dict]:
        with self._database() as connection:
            return [dict(row) for row in connection.execute(
                "SELECT * FROM experiments ORDER BY created_at, id"
            )]

    def _append(self, experiment_id: str, kind: str, payload: dict) -> int:
        encoded = json.dumps(payload, allow_nan=False)
        with self._database() as connection:
            self._experiment(connection, experiment_id)
            cursor = connection.execute(
                "INSERT INTO events(experiment_id, kind, payload, created_at) VALUES (?, ?, ?, ?)",
                (experiment_id, kind, encoded, datetime.now(timezone.utc).isoformat()),
            )
            return cursor.lastrowid

    @staticmethod
    def _experiment(connection, experiment_id):
        row = connection.execute(
            "SELECT * FROM experiments WHERE id = ?", (experiment_id,)
        ).fetchone()
        if row is None:
            raise KeyError(f"Unknown experiment: {experiment_id}")
        return dict(row)

    def record_measurement(self, experiment_id: str, measurement: Measurement) -> int:
        _require_text(measurement.quantity, measurement.unit)
        if isinstance(measurement.value, bool) or not isfinite(measurement.value):
            raise ValueError("Measurement must be finite.")
        uncertainty = measurement.uncertainty
        if uncertainty is not None and (
            isinstance(uncertainty, bool) or not isfinite(uncertainty) or uncertainty < 0
        ):
            raise ValueError("Uncertainty must be finite and nonnegative.")
        if measurement.instrument_id is not None:
            _require_text(measurement.instrument_id)
        return self._append(experiment_id, "measurement", asdict(measurement))

    def record_note(self, experiment_id: str, text: str, *, conclusion: bool = False) -> int:
        _require_text(text)
        return self._append(
            experiment_id, "conclusion" if conclusion else "observation", {"text": text}
        )

    def record_dataset(self, experiment_id: str, dataset: Dataset) -> int:
        _require_text(dataset.dataset_id, dataset.version, dataset.title, dataset.source)
        return self._append(experiment_id, "dataset", asdict(dataset))

    def record_ion_observation(
        self, experiment_id: str, sample: str, observation: Observation
    ) -> int:
        _require_text(sample)
        validate_observation(observation)
        return self._append(
            experiment_id, "ion_observation", {"sample": sample.strip(), **asdict(observation)}
        )

    def analyze_salt(self, experiment_id: str, sample: str, *, save: bool = False) -> dict:
        _require_text(sample)
        sample = sample.strip()
        rows = [
            event for event in self.export(experiment_id)["events"]
            if event["kind"] == "ion_observation" and event["payload"]["sample"] == sample
        ]
        observations = [
            Observation(event["payload"]["test"], event["payload"]["observation"])
            for event in rows
        ]
        result = identify_salt(observations)
        for item, event in zip(result["observations"], rows, strict=True):
            item["record_sequence"] = event["sequence"]
        result["sample"] = sample
        if save:
            return {**result, "record_sequence": self._append(experiment_id, "salt_analysis", result)}
        return result

    def record_calculation(self, experiment_id: str, result: dict) -> int:
        return self._append(experiment_id, "calculation", result)

    def record_simulation(self, experiment_id: str, result: dict) -> int:
        return self._append(experiment_id, "simulation", result)

    def export(self, experiment_id: str) -> dict:
        with self._database() as connection:
            experiment = self._experiment(connection, experiment_id)
            events = connection.execute(
                "SELECT sequence, kind, payload, created_at FROM events "
                "WHERE experiment_id = ? ORDER BY sequence",
                (experiment_id,),
            )
            records = [{**dict(event), "payload": json.loads(event["payload"])} for event in events]
        return {"schema_version": 1, "experiment": experiment, "events": records}

    def summarize(self, experiment_id: str, quantity: str, unit: str) -> dict:
        _require_text(quantity, unit)
        rows = [
            event for event in self.export(experiment_id)["events"]
            if event["kind"] == "measurement"
            and event["payload"]["quantity"] == quantity
            and event["payload"]["unit"] == unit
        ]
        if not rows:
            raise ValueError("No measurements match the requested quantity and unit.")
        values = [event["payload"]["value"] for event in rows]
        return {
            "method": "replicate_summary",
            "status": "calculated",
            "quantity": quantity,
            "unit": unit,
            "count": len(values),
            "mean": mean(values),
            "sample_standard_deviation": stdev(values) if len(values) > 1 else None,
            "measurement_sequences": [event["sequence"] for event in rows],
        }
