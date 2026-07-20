from collections.abc import Sequence

from app.ingestion.normalized_document import NormalizedDocument
from app.ingestion.pipeline_stage import PipelineStage


class IngestionPipeline:
    """Runs normalized documents through an ordered sequence of stages."""

    def __init__(self, stages: Sequence[PipelineStage] | None = None) -> None:
        self._stages = list(stages or [])

    def process(self, document: NormalizedDocument) -> NormalizedDocument:
        result = document

        for stage in self._stages:
            result = stage.process(result)

        return result

    def process_all(
        self,
        documents: list[NormalizedDocument],
    ) -> list[NormalizedDocument]:
        return [self.process(document) for document in documents]
