import os
import csv
import datetime
import pytest
from main import PomodoroTimer
from pathlib import Path
import Pandas

def test_get_duration():
    app = PomodoroTimer(test_mode=True,)
    app.session_type = "Work"
    app.work_input.insert(0, "25")
    assert app.get_duration() == 25

    app.session_type = "Short Break"
    app.work_input.insert(0, "5")
    assert app.get_duration() == 5

    app.session_type = "Long Break"
    app.work_input.insert(0, "20")
    assert app.get_duration() == 20

def test_start_timer():
    app = PomodoroTimer(test_mode=True)
    app.reps = 0
    app.start_timer()
    assert app.session_type == "Work"

    app.reps = 1
    app.start_timer()
    assert app.session_type == "Short Break"

    app.reps = 7
    app.start_timer()
    assert app.session_type == "Long Break"

def test_timer_reset():
    app = PomodoroTimer(test_mode=True)

    app.reps = 5
    app.session_type = "Work"
    app.check_mark.config(text="✓✓")
    app.work_input.config(state="disabled")
    app.short_input.config(state="disabled")
    app.long_input.config(state="disabled")

    app.timer_reset()
    assert app.reps == 0
    assert app.session_type == None
    assert app.check_mark.cget("text") == ""
    assert app.work_input.state == "normal"
    assert app.work_input.state == "normal"
    assert app.short_input.state == "normal"

def test_count_down_checkmarks():
    app = PomodoroTimer(test_mode=True)
    app.reps = 2
    app.count_down(0)
    assert app.check_mark.cget("text") == "✓"

    app.reps = 4
    app.count_down(0)
    assert app.check_mark.cget("text") == "✓✓"

def test_count_down_logging(tmp_path):
    log_file = tmp_path / "test_log.csv"
    app = PomodoroTimer(test_mode=True, log_file=log_file)
    app.session_type = "Work"

    app.count_down(0)
    assert log_file.exists()
    with open(log_file, newline="") as f:
        rows = list(csv.reader(f))

    duration = rows[1][3]

    assert rows[0] == ["date", "time", "session_type", "duration"]
    assert rows[1][2] == "Work"
    assert rows[1][3].endswith("mins")
    assert duration == "25 mins"

def test_show_stats(tmp_path):
    log_file = tmp_path / "test.log_csv"
    with open(log_file, "r") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "time", "session_type", "duration"])
        writer.writerow(["2025-09-25", "10:00:00", "Work", "25 mins"])
        writer.writerow(["2025-09-25", "11:00:00", "Work", "25 mins"])
        writer.writerow(["2025-09-26", "09:00:00", "Work", "20 mins"])
        writer.writerow(["2025-09-26", "09:30:00", "Short Break", "5 mins"])

    app = PomodoroTimer(test_mode=True, log_file=log_file)
    stats = app.get_stats_dataframe()
    row_25 = stats[stats["date"] == "2025-09-25"].iloc[0]
    assert row_25["work_sessions"] == 1
    assert row_25["total_minutes"] == 50

    row_26 = stats[stats["date"] == "2025-09-26"].iloc[0]
    assert row_26["work_sessions"] == 1
    assert row_26["total_minutes"] == 20


