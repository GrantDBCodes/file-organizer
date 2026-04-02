import os
import shutil
import tkinter as tk
from tkinter import filedialog

#Dictionary mapping file extensions to their category folders
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

# ============ Window Setup ============


window = tk.Tk()
window.title("File Organizer")
window.geometry("500x400")

#Center the window on screen
window.update()
x = (window.winfo_screenwidth() - 500) // 2
y = (window.winfo_screenheight() - 400) // 2
window.geometry(f"500x400+{x}+{y}")

# ============ Main Function ============


def organise():
    """Asks user to select a folder, then sorts files into category folders."""
    
    #Clears previous log entries
    log.delete("1.0", tk.END)

    #Open folder pickup dialog
    folder = filedialog.askdirectory(title="Choose a folder to organize")

    
    if folder:
        items = os.listdir(folder)
        file_count = 0
        folder_set = set()
       
        for item in items:
            full_path = os.path.join(folder, item)
            
            #Skip category folders we already created.
            if item in FILE_CATEGORIES.values():
                continue

            #Check if it's a file and move it to the appropriate category folder
            if os.path.isfile(full_path):
                name, extension = os.path.splitext(item)

                if extension in FILE_CATEGORIES:
                    #Get the category and build destination path
                    category = FILE_CATEGORIES[extension]
                    destination = os.path.join(folder, category)
                    os.makedirs(destination, exist_ok=True)
                    # Try to move the file, log error if it fails
                    try:
                        shutil.move(full_path, os.path.join(destination, item ))
                        log.insert(tk.END, f"Moved {item} to {category}\n") 
                        file_count += 1
                        folder_set.add(category)
                    except Exception as e:
                        log.insert(tk.END, f"Error moving {item}: {e}\n")
                else:
                    log.insert(tk.END, f"Skipped unknown file type: {item}\n")
        #Show summary of results            
        label.config(text="Done! Files organized successfully.")  
        log.insert(tk.END, f"\nDone! Moved {file_count} files into {len(folder_set)} folders .\n")   
    else:
        label.config(text="No folder selected!")

# ============ UI Elements ============


label = tk.Label(window, text="Select a Folder to organize")
label.pack()

button = tk.Button(window, text="Organize Files!", command=organise)
button.pack()

log = tk.Text(window)
log.pack()

# ============ Start the app ============


window.mainloop()