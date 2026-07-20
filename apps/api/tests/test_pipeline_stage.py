from app.ingestion.pipeline_stage import PipelineStage


def test_pipeline_stage_is_abstract() -> None:
    assert PipelineStage.__abstractmethods__ == {"process"}
