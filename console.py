import shlex
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import sys
import zipfile, io
import os
import hashlib


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

        case "vfs-info":
            hasher = hashlib.sha256()

            output = f"MyVFS {VFSHash}"

        case "":
            output = "Empty line"

        case "exit":
            exit(0)

        case _:
            output = "Wrong command"

    text.insert(END, "\n" + output + "\n" + path + ">")
    text.see(END)

    inputStart = text.index("end-1c")
    return "break"


def PressBackspace(event):
    if text.compare("insert", "<=", inputStart):
        return "break"


window = Tk()
window.title("MyVFS")
window.geometry("1400x700")

text = ScrolledText(window, wrap=WORD, height=20)
text.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)

launchParameters = sys.argv[1:]

text.insert(END, "Launch parameters: " + ", ".join(sys.argv[1:]) + "\n")
inputStart = text.index("end-1c")

script = None

if len(launchParameters) == 2:
    VFSPath = launchParameters[0]
    script = launchParameters[1]

elif len(launchParameters) == 1:
    VFSPath = launchParameters[0]

base_dir = os.path.join(os.path.dirname(__file__))
path = os.path.join(base_dir, VFSPath)
with open(path, "rb") as f:
    hasher = hashlib.sha256()
    chunk = f.read(8192)
    while chunk:
        hasher.update(chunk)
        chunk = f.read(8192)
    VFSHash = hasher.hexdigest()

text.insert(END, path + ">")
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
