import os
import shutil
import tkinter as tk
from tkinter import filedialog
import json

# ============ Default Categories ============

# Dictionary mapping file extensions to their category folders
# This serves as the default if no config.json exists
DEFAULT_CATEGORIES = {
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

# ============ Save / Load Config ============

def save_categories():
    """Saves the current FILE_CATEGORIES dictionary to config.json."""
    with open("config.json", "w") as f:
        json.dump(FILE_CATEGORIES, f, indent=4)

def load_categories():
    """
    Loads categories from config.json if it exists.
    Otherwise falls back to DEFAULT_CATEGORIES.
    """
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            return json.load(f)
    else:
        return DEFAULT_CATEGORIES

# Load categories on startup
FILE_CATEGORIES = load_categories()

# ============ Window Setup ============

window = tk.Tk()
window.title("File Organizer")
window.geometry("500x400")

# Center the window on screen
window.update()
x = (window.winfo_screenwidth() - 500) // 2
y = (window.winfo_screenheight() - 400) // 2
window.geometry(f"500x400+{x}+{y}")

# ============ Move History ============

# Stores tuples of (original_path, new_path) for each file moved
# Used by the undo function to reverse moves
move_history = []

# ============ Core Functions ============

def organise(preview=False):
    """
    Asks user to select a folder, then sorts files into category folders.
    
    Args:
        preview (bool): If True, only shows what would happen without moving files.
                        Defaults to False (actually moves files).
    """
    # Clear previous log entries
    log.delete("1.0", tk.END)

    # Only clear move history for real operations, not previews
    # This preserves undo ability if user runs a preview after organizing
    if not preview:
        move_history.clear()

    # Open folder picker dialog
    folder = filedialog.askdirectory(title="Choose a folder to organize")

    if folder:
        items = os.listdir(folder)
        file_count = 0        # Tracks how many files were moved/would be moved
        folder_set = set()    # Tracks unique category folders created

        for item in items:
            full_path = os.path.join(folder, item)

            # Skip category folders we already created (e.g. "Images", "Music")
            if item in FILE_CATEGORIES.values():
                continue

            # Only process files, not folders
            if os.path.isfile(full_path):
                name, extension = os.path.splitext(item)

                if extension in FILE_CATEGORIES:
                    # Get the category name and build the destination path
                    category = FILE_CATEGORIES[extension]
                    destination = os.path.join(folder, category)

                    if preview:
                        # Preview mode: just log what would happen
                        log.insert(tk.END, f"[PREVIEW] Would move {item} to {category}\n")
                        file_count += 1
                        folder_set.add(category)
                    else:
                        # Real mode: create folder and move the file
                        os.makedirs(destination, exist_ok=True)
                        try:
                            shutil.move(full_path, os.path.join(destination, item))
                            # Record the move so we can undo it later
                            move_history.append((full_path, os.path.join(destination, item)))
                            log.insert(tk.END, f"Moved {item} to {category}\n")
                            file_count += 1
                            folder_set.add(category)
                        except Exception as e:
                            log.insert(tk.END, f"Error moving {item}: {e}\n")
                else:
                    # File extension not in our categories
                    log.insert(tk.END, f"Skipped unknown file type: {item}\n")

        # Show summary of results
        if preview:
            label.config(text="Preview complete! No files were moved.")
            log.insert(tk.END, f"\nPreview: {file_count} files would be moved into {len(folder_set)} folders.\n")
        else:
            label.config(text="Done! Files organized successfully.")
            log.insert(tk.END, f"\nDone! Moved {file_count} files into {len(folder_set)} folders.\n")
    else:
        label.config(text="No folder selected!")


def undo():
    """
    Reverses the last organize operation.
    Moves all files back to their original locations and removes empty category folders.
    """
    log.delete("1.0", tk.END)

    # Nothing to undo if history is empty
    if not move_history:
        log.insert(tk.END, "Nothing to undo!\n")
        return

    # Step 1: Move each file back to its original location
    for original_path, new_path in move_history:
        try:
            shutil.move(new_path, original_path)
            filename = os.path.basename(original_path)
            log.insert(tk.END, f"Moved {filename} back!\n")
        except Exception as e:
            log.insert(tk.END, f"Error undoing move: {e}\n")

    # Step 2: Clean up empty category folders
    # Use a set to avoid trying to remove the same folder multiple times
    folders_to_remove = set()
    for original_path, new_path in move_history:
        folders_to_remove.add(os.path.dirname(new_path))

    for folder in folders_to_remove:
        try:
            # os.rmdir only removes empty folders (safe — won't delete files)
            os.rmdir(folder)
            log.insert(tk.END, f"Removed empty folder: {folder}\n")
        except:
            # Folder not empty or can't be removed — just skip it
            pass

    # Step 3: Clear history since everything has been undone
    move_history.clear()
    label.config(text="Undo complete!")


def add_category():
    """
    Opens a popup window where users can add a custom file extension
    and assign it to a category. The new mapping is saved to config.json.
    """
    # Create popup window
    popup = tk.Toplevel(window)
    popup.title("Add Custom Category")
    popup.geometry("300x200")

    # Center the popup on screen
    popup.update()
    x = (popup.winfo_screenwidth() - 300) // 2
    y = (popup.winfo_screenheight() - 200) // 2
    popup.geometry(f"300x200+{x}+{y}")

    # Extension input field
    ext_label = tk.Label(popup, text="Extension (e.g. .py):")
    ext_label.pack()
    ext_entry = tk.Entry(popup)
    ext_entry.pack()

    # Category input field
    cat_label = tk.Label(popup, text="Category Name (e.g. Code):")
    cat_label.pack()
    cat_entry = tk.Entry(popup)
    cat_entry.pack()

    def save():
        """Reads both input fields, adds the new mapping, saves to config, and closes popup."""
        ext = ext_entry.get()
        cat = cat_entry.get()
        FILE_CATEGORIES[ext] = cat
        save_categories()
        popup.destroy()

    # Save button inside the popup
    save_button = tk.Button(popup, text="Save", command=save)
    save_button.pack()

# ============ UI Elements ============

label = tk.Label(window, text="Select a Folder to organize")
label.pack()

preview_button = tk.Button(window, text="Preview files moved?", command=lambda: organise(preview=True))
preview_button.pack()

organise_button = tk.Button(window, text="Organize Files!", command=organise)
organise_button.pack()

undo_button = tk.Button(window, text="Undo!", command=undo)
undo_button.pack()

add_category_button = tk.Button(window, text="Add Custom Category", command=add_category)
add_category_button.pack()

log = tk.Text(window)
log.pack()

# ============ Start the App ============

window.mainloop()