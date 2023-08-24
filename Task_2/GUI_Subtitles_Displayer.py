import tkinter as tk
import pysrt
from tkinter import filedialog
import time

current_index=0
current_subtitle=None
subtitle=None


#Loading file storing the subtitles data
def load_srt_file():
    global current_index, current_subtitle, subtitle

    #Constraint allowing .srt files only "filetypes=[]"
    allowed_path=filedialog.askopenfilename(filetypes=[("SRT files", "*.srt")])

    try:
        subtitle=pysrt.open(allowed_path)
        current_index=0
        current_subtitle=subtitle[current_index]
        display_subtitle()

    #display error message "Error: msg"
    except Exception as ex:
        subtitle_label.config(text=f"Error: {str(ex)}") 


def display_subtitle():
    global current_index, current_subtitle

    #Checking if current_subtitle is not None as None is taken as False in Python 
    if current_subtitle:

        # Calculating starting time, i.e. time of loading the SRT file converted into seconds
        current_start_time = (
        current_subtitle.start.hours * 3600 +
        current_subtitle.start.minutes * 60 +
        current_subtitle.start.seconds +
        current_subtitle.start.milliseconds / 1000.0)

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
        subtitle_text.set('No more subtitles')

#Updates current_index and current_subtitle to display next subtitle
def new_subtitle():
    global current_subtitle, current_index, subtitle
    current_index += 1
    if current_index < len(subtitle):
        current_subtitle = subtitle[current_index]
        display_subtitle()
    else:
        current_subtitle = None
        display_subtitle()


# Create the main application window
window=tk.Tk()
window.title("SRT Subtitle Display")
window.geometry("1920x515")
window.configure(bg="#000000")

# Create and configure widgets
load_button = tk.Button(window, text="Load SRT File", command=load_srt_file)

#subtitle_text is an object of StringVar class of tkinter. StringVar is used to hold string values.
subtitle_text = tk.StringVar() 

#display text with specific formatting and appearance
subtitle_label = tk.Label(window, textvariable=subtitle_text, wraplength=400, justify="center", font=("Calibri", 16), fg="#ffffff",background="#000000")

# Pack widgets
load_button.pack(pady=10)
subtitle_label.pack(pady=20)

# Start the GUI application
window.mainloop()