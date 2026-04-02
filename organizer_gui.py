import os
import shutil
import tkinter as tk
from tkinter import filedialog

FILE_CATEGORIES = {
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".mp3": "Music",
    ".wav": "Music",
    ".mkv": "Videos",
    ".mp4": "Videos",
    ".avi": "Videos",
    ".pdf": "Documents",
    ".docx": "Documents",
    ".xlsx": "Documents",
    ".txt": "Documents",
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".torrent": "Torrents",
    ".exe": "Applications",
}



#Step 1: Create a window
window = tk.Tk()
window.title("File Organizer")

#Step 2: Set the size of the window
window.geometry("500x400")

#Step 3 Center Window
window.update()
x = (window.winfo_screenwidth() - 500) // 2
y = (window.winfo_screenheight() - 400) // 2
window.geometry(f"500x400+{x}+{y}")

#Step 4 Create a function for the button
def organise():
    folder = filedialog.askdirectory(title="Choose a folder to organize")
    if folder:
        items = os.listdir(folder)
        for item in items:
            full_path = os.path.join(folder, item)
            if os.path.isfile(full_path):
                name, extension = os.path.splitext(item)
                if extension in FILE_CATEGORIES:
                    category = FILE_CATEGORIES[extension]
                    destination = os.path.join(folder, category)
                    os.makedirs(destination, exist_ok=True)
                    shutil.move(full_path, os.path.join(destination, item ))  
        label.config(text="Done! Files organized successfully.")     
    else:
        label.config(text="No folder selected!")

#Step 3: Create your label and button
label = tk.Label(window, text="Hello!")
label.pack()

button = tk.Button(window, text="Organize Files!", command=organise)
button.pack()

#Step 4: Always Lasts(Keep the window open)
window.mainloop()