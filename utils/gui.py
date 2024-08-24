import tkinter as tk
import sys
import os
from tkinter import filedialog
from tkinter import PhotoImage

def initWindow():
    root = tk.Tk()
    root.title('Infoeduka Scraper')
    #root.configure(bg="lightgray")
    root.geometry('700x400')

    if hasattr(sys, '_MEIPASS'):
        # Running as a PyInstaller bundle
        icon_path = os.path.join(sys._MEIPASS, 'icon.png')
    else:
        # Running as a script
        icon_path = 'icon.png'

    try:
        # Load and set the icon
        icon = PhotoImage(file=icon_path)
        root.iconphoto(False, icon)
    except Exception as e:
        print(f"Failed to load icon: {e}")


    return root

def chooseDir():
    # shows dialog box and return the path
    path = filedialog.askdirectory()
    if not path:
        raise Exception("No directory selected. The operation was canceled by the user.")
    print("Selected path: " + path)
    return path