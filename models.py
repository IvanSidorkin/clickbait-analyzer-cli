from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class VideoMetric:
    title: str
    ctr: float
    retention_rate: float