from abc import ABC, abstractmethod
from collections.abc import Iterable

from models import VideoMetric

class Report(ABC):
    @abstractmethod
    def build(self, videos: Iterable[VideoMetric]) -> list[VideoMetric]:
        """Build report"""


class ClickbaitReport(Report):
    MIN_CTR = 15.0
    MAX_RETENTION_RATE = 40.0

    def build(self, videos: Iterable[VideoMetric]) -> list[VideoMetric]:
        filtered_videos = [
            video
            for video in videos
            if video.ctr > self.MIN_CTR and video.retention_rate < self.MAX_RETENTION_RATE
        ]
        return sorted(filtered_videos, key=lambda video: video.ctr, reverse=True)


REPORTS: dict[str, type[Report]] = {
    "clickbait": ClickbaitReport,
}

def get_report(report_name: str) -> Report:
    try:
        return REPORTS[report_name]()
    except KeyError as exc:
        available_reports = ", ".join(sorted(REPORTS))
        raise ValueError(
            f"Unknown report: {report_name}. Available reports: {available_reports}"
        ) from exc
    

