from math import floor
from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None


class PomodoroTimer:
    def __init__(self):
        self.reps = 0
        self.timer = None

        self.window = Tk()
        self.window.title("Pomodoro")
        self.window.config(padx=100, pady=50, bg=YELLOW)

        self.canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
        self.img = PhotoImage(file="tomato.png")
        self.canvas.create_image(103, 112, image=self.img)
        self.timer_text = self.canvas.create_text(103, 130, text="00.00", fill="white", font=(FONT_NAME, 35, "bold"))

        self.title_label = Label(text="Timer")
        self.title_label.config(fg=GREEN, font=(FONT_NAME, 28, "bold"), bg=YELLOW)
        self.title_label.grid(column=1, row=0)

        self.check_mark = Label()
        self.check_mark.config(fg=GREEN, bg=YELLOW)
        self.check_mark.grid(column=1, row=3)

        self.start_btn = Button(text="Start", highlightthickness=0, command=self.start_timer)
        self.start_btn.grid(column=0, row=2)

        self.reset_btn = Button(text="Reset", highlightthickness=0, command=self.timer_reset)
        self.reset_btn.grid(column=2, row=2)

        self.canvas.grid(column=1, row=1)

        self.window.mainloop()
    # ---------------------------- TIMER RESET ------------------------------- #
    def timer_reset(self):
        self.window.after_cancel(timer)
        self.canvas.itemconfig(self.timer_text, text="00:00")
        self.title_label.config(text="Timer", fg=GREEN)
        self.check_mark.config(text="")
        self.reps = 0

    # ---------------------------- TIMER MECHANISM ------------------------------- #
    def start_timer(self):

        self. reps += 1

        work_sec = 1 * 60
        short_break_sec = 1 * 60
        long_break_seconds = LONG_BREAK_MIN * 60

        if self.reps % 8 == 0:
            self.count_down(long_break_seconds)
            self.title_label.config(text="Long Break", fg= RED )
        elif self.reps % 2 == 0:
            self.count_down(short_break_sec)
            self.title_label.config(text="Short Break", fg=PINK)
        else:
            self.count_down(work_sec)
            self.title_label.config(text="Work Time", fg=GREEN)

    # ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
    def count_down(self, count):
        count_min = floor(count / 60)
        count_sec = count % 60

        self.canvas.itemconfig(self.timer_text, text=f"{count_min}:{count_sec:02}")
        if count > 0:
            global timer
            timer = self.window.after(1000, self.count_down, count - 1)
        else:
            self.start_timer()
            mark = ""
            completed_work_sessions =  floor(self.reps / 2)
            for i in range (completed_work_sessions):
                mark += "✓"
            self.check_mark.config(text = mark)

    # ---------------------------- UI SETUP ------------------------------- #

if __name__ == "__main__":
    PomodoroTimer()
