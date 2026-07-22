from pathlib import Path

import yaml

from app.config.source_config import SourceConfig


class SourceRegistry:
    """Loads configured content sources."""

    def __init__(self, sources: list[SourceConfig]) -> None:
        self._sources = sources

    @classmethod
    def load(cls, path: Path) -> "SourceRegistry":
        with path.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        sources = [SourceConfig(**source) for source in config.get("sources", [])]

        return cls(sources)

    def all(self) -> list[SourceConfig]:
        return self._sources

    def enabled_sources(self) -> list[SourceConfig]:
        return [source for source in self._sources if source.enabled]
