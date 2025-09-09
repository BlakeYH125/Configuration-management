import shlex
from tkinter import *
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText

window = Tk()
window.title("VFS")
window.geometry("800x400")
tab_control = ttk.Notebook(window)

frame = Frame(window)
frame.pack(side=BOTTOM, fill=X, padx=5, pady=5)

entry = Entry(frame, width=80)
entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))

text = ScrolledText(window, wrap=WORD, height=20, state=DISABLED)
text.pack(side=TOP, fill=X, padx=5, pady=5)

allText = []

def PressEnter(event):
    inputLine = entry.get()
    if len(inputLine) != 0:
        inputLine = shlex.split(inputLine)
        command = inputLine[0]
        output = ""
    else:
        command = ""
    match command:
        case "cd":
            if len(inputLine) > 1:
                output = "C:\\cd Parameters: " + ", ".join(inputLine[1:])
            else:
                output = "C:\\cd"

        case "ls":
            if len(inputLine) > 1:
                output = "C:\\ls Parameters: " + ", ".join(inputLine[1:])
            else:
                output = "C:\\ls"

        case "":
            output = "C:\\"

        case "exit":
            exit(0)

        case _:
            output = "C:\\Неверная команда"

    allText.append(output + "\n")
    text.config(state=NORMAL)
    text.insert(END, output + "\n")
    text.see(END)
    text.config(state=DISABLED)
    entry.delete(0, END)
entry.bind("<Return>", PressEnter)

window.mainloop()
