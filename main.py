from math import floor
from tkinter import *
import math
import csv
import datetime
from pathlib import Path
import pandas
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

class PomodoroTimer:
    def __init__(self, test_mode=False, log_file="session_log.csv"):
        self.reps = 0
        self.timer = None
        self.session_type = None
        self.last_session_type = None
        self.test_mode = test_mode

        self.log_file = Path("session_log.csv")
        if not self.log_file.exists():
            with open(self.log_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["date", "time", "session_type", "duration"])

        if self.test_mode:
            class DummySpinbox:
                def __init__(self, value):
                    self.value = value

                def get(self):
                    return str(self.value)

                def insert(self, index, value):
                    self.value = value

            self.work_input = DummySpinbox(25)
            self.short_input = DummySpinbox(5)
            self.long_input = DummySpinbox(20)

        else:
            self.window = Tk()
            self.window.title("Pomodoro")
            self.window.config(padx=100, pady=50, bg=YELLOW)

            self.canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
            self.img = PhotoImage(file="tomato.png")
            self.canvas.create_image(103, 112, image=self.img)
            self.timer_text = self.canvas.create_text(103, 130, text="00.00", fill="white", font=(FONT_NAME, 35, "bold"))

            self.title_label = Label(text="Timer")
            self.title_label.config(fg=GREEN, font=(FONT_NAME, 28, "bold"), bg=YELLOW)
            self.title_label.grid(column=1, row=1)

            self.check_mark = Label()
            self.check_mark.config(fg=GREEN, bg=YELLOW)
            self.check_mark.grid(column=1, row=3)

            self.settings = LabelFrame(self.window, text="settings", bg=YELLOW, font=(FONT_NAME, 12, "bold"))
            self.settings.grid(column=0, row=0, columnspan=3, pady=10)

            # ---------------------------- TIMER CONFIG ------------------------------- #
            Label(self.settings, text="Work (mins)", bg=YELLOW).grid(column=0, row=0)
            self.work_input =Spinbox(self.settings, from_=1, to=120, width=5)
            self.work_input.grid(column=1, row=0)
            self.work_input.insert(0, 24)

            Label(self.settings, text="Short Break", bg=YELLOW).grid(column=0, row=1)
            self.short_input = Spinbox(self.settings, from_=1, to=120, width=5)
            self.short_input.grid(column=1, row=1)
            self.short_input.insert(0, 5)

            Label(self.settings, text="Long Break", bg=YELLOW).grid(column=0, row=2)
            self.long_input = Spinbox(self.settings, from_=1, to=120, width=5)
            self.long_input.grid(column=1, row=2)
            self.long_input.insert(0, 20)

            # ---------------------------- BUTTONS ------------------------------- #

            self.start_btn = Button(text="Start", highlightthickness=0, command=self.start_timer)
            self.start_btn.grid(column=0, row=3)

            self.reset_btn = Button(text="Reset", highlightthickness=0, command=self.timer_reset)
            self.reset_btn.grid(column=2, row=3)

            self.stats_btn = Button(text="Show Stats", highlightthickness=0, command=self.show_stats)
            self.stats_btn.grid(column=1, row =4)

            self.canvas.grid(column=1, row=2)

            self.window.mainloop()
    # ---------------------------- TIMER RESET ------------------------------- #
    def timer_reset(self):
        self.window.after_cancel(timer)
        self.canvas.itemconfig(self.timer_text, text="00:00")
        self.title_label.config(text="Timer", fg=GREEN)
        self.check_mark.config(text="")
        self.work_input.config(state="normal")
        self.short_input.config(state="normal")
        self.long_input.config(state="normal")
        self.reps = 0

    # ---------------------------- TIMER MECHANISM ------------------------------- #
    def start_timer(self):
        self. reps += 1
        self.last_session_type = self.session_type
        work_sec = int(self.work_input.get()) * 60
        short_break_sec = int(self.short_input.get()) * 60
        long_break_seconds = int(self.long_input.get()) * 60
        self.work_input.config(state="disabled")
        self.short_input.config(state="disabled")
        self.long_input.config(state="disabled")

        if self.reps % 8 == 0:
            self.count_down(long_break_seconds)
            self.title_label.config(text="Long Break", fg= RED )
            self.session_type = "Long Break"
        elif self.reps % 2 == 0:
            self.count_down(short_break_sec)
            self.title_label.config(text="Short Break", fg=PINK)
            self.session_type = "Short Break"
        else:
            self.count_down(work_sec)
            self.title_label.config(text="Work Time", fg=GREEN)
            self.session_type = "Work"

    # ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
    def count_down(self, count):
        count_min = floor(count / 60)
        count_sec = count % 60

        self.canvas.itemconfig(self.timer_text, text=f"{count_min}:{count_sec:02}")
        if count > 0:
            global timer
            timer = self.window.after(1000, self.count_down, count - 1)
        else:
            date_time = datetime.datetime.now()
            date = date_time.strftime("%Y-%m-%d")
            time = date_time.strftime("%H:%M:%S")
            duration = self.get_duration()
            with open("session_log.csv", "a") as file:
                writer = csv.writer(file)
                writer.writerow([date, time, self.session_type, f"{duration} mins"])

            self.start_timer()
            mark = ""
            completed_work_sessions =  floor(self.reps / 2)
            for i in range (completed_work_sessions):
                mark += "✓"
            self.check_mark.config(text = mark)

    def get_duration(self):
        if self.session_type == "Work":
            return int(self.work_input.get())
        elif self.session_type == "Short Break":
            return int(self.short_input.get())
        elif self.session_type == "Long Break":
            return int(self.short_input.get())

    # ---------------------------- STATISTICS ------------------------------- #
    def show_stats(self):
        df = pandas.read_csv("session_log.csv")
        df["duration_minutes"] = df["duration"].str.replace(" mins", "").astype(int)
        work_sessions = df[df["session_type"] == "Work"]

        total_sessions = work_sessions.groupby("date").size().reset_index(name="work_sessions")
        total_minutes = work_sessions.groupby("date")["duration_minutes"].sum().reset_index(name="total_minutes")
        stats = pandas.merge(total_sessions, total_minutes)

        win = Toplevel(self.window)
        win.title("Work Stats")
        win.geometry("720x420")

        fig = Figure(figsize=(7, 4), dpi=100)
        ax = fig.add_subplot(111)

        ax.bar(stats["date"], stats["total_minutes"], color="green", label="Total Minutes")
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Minutes Worked")
        ax.tick_params(axis="x", labelrotation=45)
        ax.legend()
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack()

        NavigationToolbar2Tk(canvas, win)

    # ---------------------------- UI SETUP ------------------------------- #

if __name__ == "__main__":
    PomodoroTimer()
