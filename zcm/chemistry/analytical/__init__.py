from scm.chemistry.analytical import (
    AnalysisRecord,
    AnalysisType,
    Observation,
)


class AnalyticalWorkspace:
    def create_record(
        self,
        analysis_type: AnalysisType,
        observations: tuple[Observation, ...] = (),
    ) -> AnalysisRecord:
        return AnalysisRecord(
            analysis_type=analysis_type,
            observations=observations,
        )


analytical_workspace = AnalyticalWorkspace()

__all__ = [
    "AnalyticalWorkspace",
    "analytical_workspace",
]
