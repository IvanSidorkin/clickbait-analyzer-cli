import csv
from pathlib import Path


from cli import read_videos, run


def create_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "title",
                "ctr",
                "retention_rate",
                "views",
                "likes",
                "avg_watch_time",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def test_read_videos_reads_multiple_files(tmp_path: Path) -> None:
    file1 = tmp_path / "metrics1.csv"
    file2 = tmp_path / "metrics2.csv"

    create_csv(
        file1,
        [
            {
                "title": "Video 1",
                "ctr": "18.2",
                "retention_rate": "35",
                "views": "1000",
                "likes": "100",
                "avg_watch_time": "4.2",
            }
        ],
    )
    create_csv(
        file2,
        [
            {
                "title": "Video 2",
                "ctr": "22.5",
                "retention_rate": "28",
                "views": "2000",
                "likes": "200",
                "avg_watch_time": "3.1",
            }
        ],
    )

    videos = read_videos([str(file1), str(file2)])

    assert len(videos) == 2
    assert videos[0].title == "Video 1"
    assert videos[1].title == "Video 2"


def test_run_success(tmp_path):
    file = tmp_path / "data.csv"

    file.write_text(
        "title,ctr,retention_rate\n"
        "A,20,30\n"
    )

    code = run(["--files", str(file), "--report", "clickbait"])

    assert code == 0


def test_run_unknown_report(tmp_path):
    file = tmp_path / "data.csv"

    file.write_text(
        "title,ctr,retention_rate\n"
        "A,20,30\n"
    )

    code = run(["--files", str(file), "--report", "unknown"])

    assert code == 1


def test_run_missing_file():
    code = run(["--files", "nope.csv", "--report", "clickbait"])

    assert code == 1
