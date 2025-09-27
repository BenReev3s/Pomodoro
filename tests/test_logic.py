import os
import csv
import datetime
import pytest
from main import PomodoroTimer

def test_get_duration(tmp_path):
    log_file = tmp_path / "test_file.csv"
    app = PomodoroTimer(test_mode=True, log_file=log_file)
    app.session_type = "Work"
    app.work_input.insert(0, "25")
    assert app.get_duration() == 25

    app.session_type = "Short Break"
    app.work_input.insert(0, "5")
    assert app.get_duration() == 5

    app.session_type = "Long Break"
    app.work_input.insert(0, "20")
    assert app.get_duration() == 20

def test_start_timer(tmp_path):
    log_file = tmp_path
    app = PomodoroTimer(test_mode=True, log_file=log_file)
    app.reps = 0
    app.start_timer()
    assert app.session_type == "Work"

    app.reps = 1
    app.start_timer()
    assert app.session_type == "Short Break"

    app.reps = 7
    app.start_timer()
    assert app.session_type == "Long Break"