from tkinter import filedialog
import os.path
import shutil
import customtkinter


def m3u_copy(source, destination):
    try:
        file = open(source).readlines()
    except IOError:
        customtkinter.CTkLabel(frame_messages, text="Cannot open m3u file").pack()
        return
    if not os.path.exists(destination) or not os.path.isdir(destination):
        customtkinter.CTkLabel(
            frame_messages,
            text="No such destination directory or destination is not a directory",
        ).pack()
        return
    if "/" in source:
        source_path = source[: source.rindex("/") + 1]
    else:
        source_path = ""
    shutil.copy(source, destination)
    for line in file:
        if line.strip() != "":
            line = line[: len(line) - 1]
            if "/" in line and not os.path.exists(
                destination + line[: line.rindex("/") + 1]
            ):
                os.makedirs(destination + line[: line.rindex("/") + 1])
            if not os.path.isfile(source_path + line):
                customtkinter.CTkLabel(
                    frame_messages, text=f"\n{line} does not exist"
                ).pack()
            else:
                try:
                    shutil.copy(source_path + line, destination + line)
                except IOError:
                    customtkinter.CTkLabel(
                        frame_messages,
                        text=f"\n{line} cannot be copied, function terminated",
                    ).pack()
                    return
    customtkinter.CTkLabel(frame_messages, text="Copied!").pack()


def go_through_lines(path):
    try:
        file = open(path).readlines()
    except IOError:
        customtkinter.CTkLabel(frame_messages, text="Cannot open m3u file").pack()
        return
    for widgets in frame_paths.winfo_children():
        widgets.destroy()
    for line in file:
        if line.strip() != "":
            customtkinter.CTkLabel(frame_paths, text=line).pack()


def m3u_path():
    path = filedialog.askopenfilename(
        initialdir="/", title="Choose a m3u file", filetypes=(("m3u files", "*.m3u"),)
    )
    label_src.configure(text=path)


def destination_path():
    path = filedialog.askdirectory(
        initialdir="/", title="Choose a destination directory"
    )
    label_dest.configure(text=path)


def get_paths_and_copy():
    src = label_src.cget("text")
    try:
        src = src.strip()
    except AttributeError:
        customtkinter.CTkLabel(frame_messages, text="m3u file not specified!").pack()
        return
    if src == "":
        customtkinter.CTkLabel(frame_messages, text="m3u file not specified!").pack()
        return
    dest = label_dest.cget("text")
    dest = dest.strip() + "/"
    if dest == "":
        customtkinter.CTkLabel(frame_messages, text="Destination not specified!").pack()
        return
    for widgets in frame_messages.winfo_children():
        widgets.destroy()
    try:
        m3u_copy(src, dest)
    except shutil.SameFileError as err:
        customtkinter.CTkLabel(frame_messages, text=err).pack()
        return
    except PermissionError:
        customtkinter.CTkLabel(frame_messages, text="Destination not specified!").pack()
        return


def get_m3u_path_and_list_paths():
    for widgets in frame_messages.winfo_children():
        widgets.destroy()
    m3u_path()
    try:
        src = label_src.cget("text").strip()
    except AttributeError:
        customtkinter.CTkLabel(frame_messages, text="m3u file not specified!").pack()
        return
    go_through_lines(src)


window = customtkinter.CTk()
window.geometry("700x800")
window.resizable(False, False)
window.title("m3u copy by SBanczyk")
label_tile = customtkinter.CTkLabel(
    window, text="m3u copier", font=("Helvetica", 70)
).pack()
button_source = customtkinter.CTkButton(
    window, text="Source", font=("Arial", 50), command=get_m3u_path_and_list_paths
)
label_src = customtkinter.CTkLabel(
    window, text="", width=100, height=1, text_color="dodger blue"
)
button_destination = customtkinter.CTkButton(
    window, text="Destination", font=("Arial", 50), command=destination_path
)
label_dest = customtkinter.CTkLabel(window, text="", width=100, height=1)
label_paths = customtkinter.CTkLabel(window, text="Paths:")
frame_paths = customtkinter.CTkScrollableFrame(window, width=300, height=300)
frame_copy = customtkinter.CTkFrame(window)
button_copy = customtkinter.CTkButton(
    frame_copy, text="Copy", font=("Arial", 50), command=get_paths_and_copy
)
frame_messages = customtkinter.CTkScrollableFrame(frame_copy, width=600)

button_source.pack()
label_src.pack()
button_destination.pack()
label_dest.pack()
label_paths.pack()
frame_paths.pack()
button_copy.pack()
frame_copy.pack(pady=40)
frame_messages.pack()
window.mainloop()
