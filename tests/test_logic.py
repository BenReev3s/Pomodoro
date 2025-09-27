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

def test_count_down():
    app = PomodoroTimer(test_mode=True)
    app.reps = 2
    app.count_down(0)
    assert app.check_mark.cget("text") == "✓"

    app.reps = 4
    app.count_down(0)
    assert app.check_mark.cget("text") == "✓✓"



