import tkinter as tk
import pysrt
from tkinter import filedialog
import time

current_index=0
current_subtitle=None
subtitle=None
current_text_size=16
current_start_time=0
current_end_time=0


#Loading file storing the subtitles data
def load_srt_file():
    global current_index, current_subtitle, subtitle

    #Constraint allowing .srt files only "filetypes=[]"
    allowed_path=filedialog.askopenfilename(filetypes=[("SRT files", "*.srt")])

    try:
        subtitle=pysrt.open(allowed_path)
        current_index=0
        current_subtitle=subtitle[current_index]
        load_button.pack_forget()
        display_subtitle()

    #display error message "Error: msg"
    except Exception as ex:
        subtitle_label.config(text=f"Error: {str(ex)}") 


def display_subtitle():
    global current_subtitle,current_end_time,current_start_time

    #Checking if current_subtitle is not None as None is taken as False in Python 
    if current_subtitle:

        # Calculating starting time, i.e. time of loading the SRT file converted into seconds
        current_start_time = (
        current_subtitle.start.hours * 3600 +
        current_subtitle.start.minutes * 60 +
        current_subtitle.start.seconds +
        current_subtitle.start.milliseconds / 1000.0)

        previous_end_time=current_end_time
        time_stamp=int(current_start_time-previous_end_time)
        # if current_index>=1 and time_stamp > 0:
        #     if  current_start_time > previous_end_time:
        #         time_stamp_empty=time_stamp*1000
        #         subtitle_text.set("")
        #         window.after(time_stamp_empty,new_subtitle)

        #likely used to represent the end time of that subtitle in the SRT (SubRip) file.
        current_end_time = (                
            current_subtitle.end.hours * 3600 +
            current_subtitle.end.minutes * 60 +
            current_subtitle.end.seconds +
            current_subtitle.end.milliseconds / 1000.0)

        #selecting time stamp for displaying the subtitle
        time_stamp = int((current_end_time - current_start_time) * 1000)


        #.set is the attribute of "StringVar" class and .text is attribute of pysrt library used to access text content of current_subtitle
        subtitle_text.set(current_subtitle.text)  
        window.after(time_stamp, new_subtitle)
    else:
        increase_text_button.pack_forget()
        decrease_text_button.pack_forget()
        subtitle_label.pack_forget()
        subtitle_text.set('No more subtitles')
        load_button.pack(pady=10)
        subtitle_label.pack(pady=20)
        increase_text_button.pack(pady=10)
        decrease_text_button.pack(pady=10)



#Function to update current_index and current_subtitle to display next subtitle
def new_subtitle():
    global current_subtitle, current_index, subtitle
    current_index += 1
    if current_index < len(subtitle):
        current_subtitle = subtitle[current_index]
        display_subtitle()
    else:
        current_subtitle = None
        display_subtitle()


# Function to increase text size
def increase_text_size(event=None):
    global current_text_size
    if current_text_size!=72:
        current_text_size += 2
        subtitle_label.config(font=("Calibri", current_text_size))

# Function to decrease text size
def decrease_text_size(event=None):
    global current_text_size
    if current_text_size!=4:
        current_text_size -= 2
        subtitle_label.config(font=("Calibri", current_text_size))


# Create the main application window
window=tk.Tk()
window.title("SRT Subtitle Display")
window.geometry("1920x515")
window.configure(bg="#000000")

# Create and configure widgets
load_button = tk.Button(window, text="Load SRT File", command=load_srt_file)
increase_text_button = tk.Label(window, text="+", font=("Arial", 40), padx=10, cursor="hand2",justify="center", fg="#ffffff",background="#000000")
decrease_text_button = tk.Label(window, text="-", font=("Arial", 40), padx=10, cursor="hand2",justify="left", fg="#ffffff",background="#000000")

#subtitle_text is an object of StringVar class of tkinter. StringVar is used to hold string values.
subtitle_text = tk.StringVar() 

increase_text_button.bind("<Button-1>", increase_text_size)
decrease_text_button.bind("<Button-1>", decrease_text_size)

#display text with specific formatting and appearance
subtitle_label = tk.Label(window, textvariable=subtitle_text, wraplength=1920, justify="center", font=("Calibri", 16), fg="#ffffff",background="#000000")

# Pack widgets
load_button.pack(pady=10)
subtitle_label.pack(pady=20,anchor='center',fill='both',expand=True)
increase_text_button.pack(pady=10,side="left") 
decrease_text_button.pack(pady=10,side="right")

# Start the GUI application
window.mainloop()