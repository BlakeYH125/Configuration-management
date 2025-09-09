import shlex
from tkinter import *
import tkinter.ttk as ttk

window = Tk()
window.title("VFS")
window.geometry("800x400")
tab_control = ttk.Notebook(window)

frame = Frame(window)
frame.pack(side=BOTTOM, fill=X, padx=5, pady=5)

entry = Entry(frame, width=80)
entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))

output_label = Label(window, text="", anchor="w", justify=LEFT)
output_label.pack(side=TOP, fill=X, padx=5, pady=5)

allText = []

def PressEnter(event):
    inputLine = shlex.split(entry.get())
    command = inputLine[0]
    output = ""

    match command:
        case "cd":
            if len(inputLine) > 1:
                output = "C:\\cd Parameters: " + ", ".join(inputLine[1:])
            else:
                output = "C:\\cd"

        case "ls":
            if len(inputLine) > 1:
                output = "C:\\ls Parameters: " + " ".join(inputLine[1:])
            else:
                output = "C:\\ls"

        case "exit":
            exit(0)

        case _:
            output = "C:\\Неверная команда"

    allText.append(output + "\n")
    output_label.config(text="".join(allText))
    entry.delete(0, END)
entry.bind("<Return>", PressEnter)

window.mainloop()

