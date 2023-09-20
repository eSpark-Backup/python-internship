import time
from tkinter import *
from ctypes import windll, byref, sizeof, c_int
# from tkinter.ttk import *

seconds = 0
minutes = 0
hours = 0
stop = 0
update_scheduled = False  # Flag to track if an update is already scheduled

def start_watch():
    global stop, update_scheduled

    if stop == 0 and not update_scheduled:
        update_scheduled = True
        label.after(0, update_timer)

    if stop == 1:
        stop = 0
        label.after(0, update_timer)

def update_timer():
    global hours, minutes, seconds, stop

    if stop == 0:
        seconds += 1
        if seconds == 60:
            minutes += 1
            seconds = 0

        if minutes == 60:
            hours += 1
            minutes = 0

        label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        label.after(1000, update_timer)

def stop_watch():
    global stop
    stop = 1

def reset():
    global hours, minutes, seconds, stop
    seconds = 0
    minutes = 0
    hours = 0
    stop = 1
    label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

def move_app(e):
    window.geometry(f'+{e.x_root}+{e.y_root}')

# main_window
window = Tk()
window.title('STOP WATCH')
window.geometry('400x450')
window.iconbitmap(r'timer_JHz_icon.ico')
window.resizable(False, False)

#background
back=PhotoImage(file='b_g.png')
label_back =Label(window , background="#212121", image=back )
label_back.place(x=0 , y=0, relwidth=1 , relheight=1)

#create label 
label=Label(window, background="#000000", text='00:00:00'
, foreground='#7DAE59',font=('Times',35))
label.place(relx=0.5, rely=0.43,anchor='center')

# Place the "Reset" button in the middle
reset_button = Button(window, text='Reset', command=reset, bg="#000000", fg="#ffffff", padx=57, font=('Serif',13))
reset_button.place(x=116.5, y=305)
# reset_button.pack(side="left", padx=15)

# Place the "Start" button on the left
start_button = Button(window, text='Start  ', command=start_watch, bg="#000000", fg="#0282D6", padx=57, font=('Serif',13))
# start_button.pack(side="left", padx=15)
start_button.place(x=116.5, y=235)

# Place the "Stop" button on the right
stop_button = Button(window, text='Stop  ', command=stop_watch, bg="#000000", fg="red", padx=57, font=('Serif',13))
# stop_button.pack(side="right", padx=15)
stop_button.place(x=116.5, y=270)

# main_loop
window.mainloop()

