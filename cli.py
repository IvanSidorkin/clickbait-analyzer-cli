import argparse
import csv
import sys
from collections.abc import Iterable, Sequence
from pathlib import Path

from tabulate import tabulate

from models import VideoMetric
from reports import get_report

REQUIRED_COLUMNS = {"title", "ctr", "retention_rate"}
SUCCESS = 0
ERROR = 1


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build reports from YouTube video metrics CSV files.",
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Paths to CSV files with YouTube video metrics.",
    )
    parser.add_argument(
        "--report",
        required=True,
        help="Report name to build. Example: clickbait",
    )
    return parser.parse_args(argv)


def parse_video_row(row: dict[str, str]) -> VideoMetric:
    return VideoMetric(
        title=row["title"],
        ctr=float(row["ctr"]),
        retention_rate=float(row["retention_rate"]),
    )


def read_videos(file_paths: Iterable[str]) -> list[VideoMetric]:
    videos: list[VideoMetric] = []

    for file_path in file_paths:
        path = Path(file_path)
        with path.open("r", encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            if reader.fieldnames is None:
                raise ValueError(f"CSV file is empty: {path}")

            missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames)
            if missing_columns:
                missing = ", ".join(sorted(missing_columns))
                raise ValueError(f"Missing required CSV columns in {path}: {missing}")

            for row in reader:
                videos.append(parse_video_row(row))

    return videos


def render_report_table(videos: Iterable[VideoMetric]) -> str:
    table = [
        [video.title, video.ctr, video.retention_rate]
        for video in videos
    ]
    return tabulate(
        table,
        headers=["title", "ctr", "retention_rate"],
        tablefmt="github",
        floatfmt=".1f",
    )


def run(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        videos = read_videos(args.files)
        report = get_report(args.report)
        result = report.build(videos)
    except FileNotFoundError as exc:
        print(f"File not found: {exc}", file=sys.stderr)
        return ERROR
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return ERROR

    print(render_report_table(result))
    return SUCCESS


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()