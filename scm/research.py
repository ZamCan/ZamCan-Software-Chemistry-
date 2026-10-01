from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass(frozen=True)
class Dataset:
    dataset_id: str
    version: str
    title: str
    source: str
    license: str = ''
    checksum: str = ''
    retrieved_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class Experiment:
    experiment_id: str
    title: str
    objective: str
    observations: list[dict] = field(default_factory=list)
    calculations: list[dict] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    conclusions: list[str] = field(default_factory=list)
    def observe(self, **data): self.observations.append(data)
    def calculate(self, **data): self.calculations.append(data)
    def conclude(self, text): self.conclusions.append(text)

@dataclass
class ResearchWorkspace:
    workspace_id: str
    title: str
    experiments: list[Experiment] = field(default_factory=list)
    datasets: list[Dataset] = field(default_factory=list)
    def add_experiment(self, experiment): self.experiments.append(experiment)
    def add_dataset(self, dataset): self.datasets.append(dataset)
