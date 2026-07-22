from dataclasses import dataclass


@dataclass(slots=True)
class SourceConfig:
    id: str
    name: str
    type: str
    url: str
    enabled: bool = True
