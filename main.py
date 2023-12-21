import tkinter as tk
from tkinter import filedialog
import os.path
import shutil


def m3u_copy(source, destination):
    try:
        file = open(source).readlines()
    except IOError:
        current_text = label_errors.cget("text")
        label_errors.config(text=current_text + "Cannot open m3u file")
        return
    if not os.path.exists(destination) or not os.path.isdir(destination):
        current_text = label_errors.cget("text")
        label_errors.config(text=current_text + "No such destination directory or destination is not a directory")
        return
    if "/" in source:
        source_path = source[:source.rindex("/")+1]
    else:
        source_path = ""
    shutil.copy(source, destination)
    for line in file:
        if line.strip() != '':
            line = line[:len(line) - 1]
            if "/" in line and not os.path.exists(destination + line[:line.rindex("/") + 1]):
                os.makedirs(destination + line[:line.rindex("/") + 1])
            if not os.path.isfile(source_path + line):
                current_text = label_errors.cget("text")
                label_errors.config(text=current_text+f"\n{line} does not exist")
            else:
                try:
                    shutil.copy(source_path + line, destination + line)
                except IOError:
                    current_text = label_errors.cget("text")
                    label_errors.config(text=current_text + f"\n{line} cannot be copied, function terminated")
                    return
    label_finish.config(text="Copied!")


def go_through_lines(path):
    try:
        file = open(path).readlines()
    except IOError:
        current_text = label_errors.cget("text")
        label_errors.config(text=current_text + "Cannot open m3u file")
        return
    for line in file:
        if line.strip() != "":
            current_text = label_paths.cget("text")
            label_paths.config(text=current_text+line)


def m3u_path():
    path = filedialog.askopenfilename(initialdir="/home/szymon/PycharmProjects/GitHub/m3u_copy",
                                      title="Choose a m3u file", filetypes=(("m3u files", "*.m3u"),))
    label_src.config(text="Source: "+path)


def destination_path():
    path = filedialog.askdirectory(initialdir="/home/szymon/PycharmProjects", title="Choose a destination directory")
    label_dest.config(text="Destination: "+path)


def polaczone():
    src = label_src.cget("text")
    src = src[src.rindex(" ")+1:]
    dest = label_dest.cget("text") + "/"
    dest = dest[dest.rindex(" ")+1:]
    m3u_copy(src, dest)


def polaczone2():
    m3u_path()
    src = label_src.cget("text")
    src = src[src.rindex(" ")+1:]
    go_through_lines(src)


window = tk.Tk()
window.geometry("700x350")
label_src = tk.Label(window,
                     text="Source:",
                     width=100, height=1,
                     fg="blue")
label_dest = tk.Label(window,
                      text="Destination:",
                      width=100, height=1,
                      fg="blue")
button_source = tk.Button(window,
                          text="Source",
                          command=polaczone2)
button_destination = tk.Button(window,
                               text="Destination",
                               command=destination_path)
label_paths = tk.Label(window,
                       text="Paths:\n")
button_copy = tk.Button(window,
                        text="Copy",
                        command=polaczone)
label_errors = tk.Label(window,
                        text="")
label_finish = tk.Label(window,
                        text="")
label_src.pack()
label_dest.pack()
button_source.pack()
button_destination.pack()
label_paths.pack()
button_copy.pack()
label_errors.pack()
label_finish.pack()
window.mainloop()
