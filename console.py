import shlex
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import sys


def PressEnter(event=None, line=None):
    global inputStart
    if line != None:
        inputLine = line.strip()
    else:
        inputLine = text.get(inputStart, "end-1c").strip()

    if len(inputLine) != 0:
        inputLine = shlex.split(inputLine)
        command = inputLine[0]
        output = ""
    else:
        command = ""

    match command:
        case "cd":
            if len(inputLine) > 1:
                output = "Command: cd; Parameters: " + ", ".join(inputLine[1:])
            else:
                output = "Command: cd"

        case "ls":
            if len(inputLine) > 1:
                output = "Command: ls; Parameters: " + ", ".join(inputLine[1:])
            else:
                output = "Command: ls"

        case "":
            output = "Empty line"

        case "exit":
            exit(0)

        case _:
            output = "Wrong command"

    text.insert(END, "\n" + output + "\n" + VFSPath)
    text.see(END)

    inputStart = text.index("end-1c")
    return "break"

def PressBackspace(event):
    if text.compare("insert", "<=", inputStart):
        return "break"

window = Tk()
window.title("MyVFS")
window.geometry("800x400")

text = ScrolledText(window, wrap=WORD, height=20)
text.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)

launchParameters = sys.argv[1:]


script = None
VFSPath = ">>"

if len(launchParameters) == 2:
    VFSPath = launchParameters[0] + ">>"
    script = launchParameters[1]
elif len(launchParameters) == 1:
    VFSPath = launchParameters[0] + ">>"

text.insert(END, "Launch parameters: " + ", ".join(sys.argv[1:]) + "\n" + VFSPath)
inputStart = text.index("end-1c")

if script != None:
    with open(script, "r") as file:
        for line in file:
            line = line.strip()
            text.insert(END, line)
            PressEnter(line=line)


text.bind("<Return>", PressEnter)
text.bind("<BackSpace>", PressBackspace)

window.mainloop()
