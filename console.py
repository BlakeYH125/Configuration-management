import shlex
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import sys
import zipfile
import os
import hashlib
import getpass


def PressEnter(event=None, line=None):
    global inputStart, currentDirectory, zip_ref
    if line != None:
        inputLine = line.strip()
    else:
        inputLine = text.get(inputStart, "end-1c").strip()

    if len(inputLine) != 0:
        inputLine = shlex.split(inputLine, posix=False)
        command = inputLine[0]
        output = ""
    else:
        command = ""

    match command:
        case "cd":
            if len(inputLine) == 1:
                output = currentDirectory
            elif len(inputLine) == 2:
                target = inputLine[1]
                if target == "..":
                    if currentDirectory == VFSPath:
                        output = ""
                    else:
                        parts = currentDirectory[len(VFSPath):].strip("/").split("/")
                        currentDirectory = f"{VFSPath}/{'/'.join(parts[:-1])}"
                        currentDirectory = currentDirectory[:-1]
                        output = ""
                elif target == "/":
                    currentDirectory = VFSPath
                    output = ""
                else:
                    target = target.rstrip('/')
                    parts = currentDirectory[len(VFSPath):].strip("/")
                    if parts:
                        search_path = f"{parts}/{target}"
                    else:
                        search_path = target

                    found = False
                    for file_path in allFiles:
                        if file_path.startswith(search_path + '/'):
                            found = True
                            break

                    if found:
                        if search_path:
                            currentDirectory = f"{VFSPath}/{search_path}"
                        else:
                            currentDirectory = VFSPath
                        output = ""
                    else:
                        output = f"Папка '{target}' не найдена"

        case "ls":
            prefix = currentDirectory[len(VFSPath):].lstrip("/")
            contents = set()
            for file_path in allFiles:
                if not file_path.startswith(prefix):
                    continue

                remaining_path = file_path[len(prefix):].lstrip("/")

                if remaining_path == "":
                    continue

                first_part = remaining_path.split("/")[0]

                if "/" in remaining_path:
                    contents.add(first_part + "/")
                else:
                    contents.add(first_part)
            if contents:
                sorted_contents = sorted(contents)
                output = "\n".join(sorted_contents)
            else:
                output = "(пусто)"

        case "cat":
            if len(inputLine) != 2:
                output = "Использование: cat <имя_файла>"
            else:
                filename = inputLine[1]
                prefix = currentDirectory[len(VFSPath):].strip("/")
                if prefix:
                    file_path = prefix + "/" + filename
                else:
                    file_path = filename
                if file_path in allFiles:
                    with zipfile.ZipFile(path, "r") as zip_ref:
                        data = zip_ref.read(file_path)
                        output = data.decode("utf-8")
                else:
                    output = f"Файл '{filename}' не найден"

        case "whoami":
            username = getpass.getuser()
            hostname = os.environ.get("COMPUTERNAME")
            output = f"{hostname}\\{username}"

        case "du":
            prefix = currentDirectory[len(VFSPath):].strip("/")
            sizes = {}
            for f in allFiles:
                if f.startswith(prefix):
                    remainder = f[len(prefix):].lstrip("/")
                    if remainder:
                        top_level = remainder.split("/")[0]
                        sizes[top_level] = sizes.get(top_level, 0) + zip_ref.getinfo(f).file_size
            output = "\n".join(f"{name}\t{size} bytes" for name, size in sizes.items())

        case "vfs-info":
            hasher = hashlib.sha256()

            output = f"MyVFS {VFSHash}"

        case "":
            output = "Empty line"

        case "exit":
            exit(0)

        case _:
            output = "Wrong command"
    if output != "":
        text.insert(END, "\n" + output + "\n" + currentDirectory + ">")
        text.see(END)
    else:
        text.insert(END, "\n" + currentDirectory + ">")
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

text.insert(END, VFSPath + ">")
inputStart = text.index("end-1c")

with zipfile.ZipFile(path, "r") as zip_ref:
    allFiles = zip_ref.namelist()
allDirectories = sorted({name for name in allFiles if name.endswith('/')})
allDirectories = [i[:-1] for i in allDirectories]

currentDirectory = VFSPath

if script != None:
    with open(script, "r") as file:
        for line in file:
            line = line.strip()
            text.insert(END, line)
            PressEnter(line=line)



text.bind("<Return>", PressEnter)
text.bind("<BackSpace>", PressBackspace)

window.mainloop()
