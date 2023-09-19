import time
from tkinter import *
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
window.geometry('500x250')
window.configure(bg="#B8C1CB")
window.resizable(False, False)

# #remove title bar
# window.overrideredirect(True)

# title=Frame(window, bg="#7AA428", relief=SUNKEN,bd=0)
# title.pack( fill=X)

# #binding for moving
# title.bind("<B1-Motion>", move_app)


# title_label=Label(title, text="STOP WATCH", bg="#7AA428", fg='#000000')
# title_label.pack(anchor=CENTER)

# win_close=Button(title,text="X", fg='black', bg='red', command=window.destroy)
# win_close.pack(side=RIGHT)


# my_button=Button(window, text="Close", command=window.quit)
# my_button.pack()


# UI
label = Label(window, text="00:00:00", background="#000000", foreground="#ffffff",font=('Serif',20))
label.pack(padx=50, pady=50)

# Create a frame to hold the buttons and center them horizontally
button_frame = Frame(window)
button_frame.pack(pady=25)

# Create a colored label as the background for the frame (black in this case)
bg_label = Label(button_frame, background="#B8C1CB")
bg_label.pack(fill="both", expand=True)

# Place the "Reset" button in the middle
reset_button = Button(bg_label, text='Reset', command=reset, bg="#000000", fg="#ffffff")
reset_button.pack(side="left", padx=15)

# Place the "Start" button on the left
start_button = Button(bg_label, text='Start', command=start_watch, bg="#2A69BF", fg="#ffffff")
start_button.pack(side="left", padx=15)

# Place the "Stop" button on the right
stop_button = Button(bg_label, text='Stop', command=stop_watch, bg="#D12B2B", fg="#ffffff")
stop_button.pack(side="right", padx=15)


# main_loop
window.mainloop()
