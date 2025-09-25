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

# ---------------------------- TIMER RESET ------------------------------- # 
def timer_reset():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg=GREEN)
    check_mark.config(text="")
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1

    work_sec = 1 * 60
    short_break_sec = 1 * 60
    long_break_seconds = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_seconds)
        title_label.config(text="Long Break", fg= RED )
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Short Break", fg=PINK)
    else:
        count_down(work_sec)
        title_label.config(text="Work Time", fg=GREEN)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = floor(count / 60)
    count_sec = count % 60

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec:02}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        mark = ""
        completed_work_sessions =  floor(reps / 2)
        for i in range (completed_work_sessions):
            mark += "✓"
        check_mark.config(text = mark)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width= 200, height= 224, bg= YELLOW, highlightthickness= 0)
img = PhotoImage(file="tomato.png")
canvas.create_image(103, 112, image=img)
timer_text = canvas.create_text(103, 130, text= "00.00", fill="white", font=(FONT_NAME, 35, "bold"))

title_label = Label(text="Timer")
title_label.config(fg=GREEN, font=(FONT_NAME, 28, "bold"), bg=YELLOW)
title_label.grid(column=1, row = 0)

check_mark = Label()
check_mark.config(fg=GREEN, bg=YELLOW)
check_mark.grid(column=1, row=3)

start_btn = Button(text="Start", highlightthickness=0, command=start_timer)
start_btn.grid(column=0, row=2)

reset_btn = Button(text="Reset", highlightthickness=0, command=timer_reset)
reset_btn.grid(column=2, row=2)

canvas.grid(column=1, row=1)



window.mainloop()