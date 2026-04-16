import pytest

from models import VideoMetric
from reports import ClickbaitReport, get_report


def test_clickbait_report_filters_and_sorts_by_ctr_desc() -> None:
    videos = [
        VideoMetric(title="A", ctr=18.2, retention_rate=35.0),
        VideoMetric(title="B", ctr=22.5, retention_rate=28.0),
        VideoMetric(title="C", ctr=9.5, retention_rate=82.0),
        VideoMetric(title="D", ctr=25.0, retention_rate=22.0),
        VideoMetric(title="E", ctr=16.5, retention_rate=42.0),
        VideoMetric(title="F", ctr=19.0, retention_rate=38.0),
    ]

    report = ClickbaitReport()

    result = report.build(videos)

    assert [video.title for video in result] == ["D", "B", "F", "A"]


def test_get_report_raises_for_unknown_report() -> None:
    with pytest.raises(ValueError, match="Unknown report"):
        get_report("unknown")   