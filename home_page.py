import tkinter as tk
from tkinter import ttk
from sidebar import Sidebar
from PIL import Image, ImageTk

class Home:
    def __init__(self, username: str):
        self.username = username
        self.window = tk.Tk()
        self.window.tk.call("source", "./oakridge-codefest/forest-dark.tcl")
        ttk.Style().theme_use("forest-dark")

        self.main_frame = ttk.Frame(self.window)
        self.main_frame.grid(row = 0, column = 1, padx = 10, pady = 10)

        self.welcome = ttk.Label(self.main_frame, text = f"Welcome {self.username}!")
        self.welcome.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.logo = ImageTk.PhotoImage(Image.open("./oakridge-codefest/logo.png"))

        self.label = ttk.Label(self.main_frame, image = self.logo)
        self.label.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.window.update()
        self.sidebar = Sidebar(self.window, self.username, True)
        self.window.mainloop()