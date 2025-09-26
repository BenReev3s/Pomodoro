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
    result = app.get_duration()
    print("DEBUG → get_duration() returned:", result)

