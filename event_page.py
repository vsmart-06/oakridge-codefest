import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
from sidebar import Sidebar

class Events:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Events")
        self.window.tk.call("source", "./oakridge-codefest/forest-dark.tcl")
        ttk.Style().theme_use("forest-dark")

        sidebar = Sidebar(self.window)

        self.title_label = ttk.Label(self.window, text = "Title:")
        self.title_label.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.title_entry = ttk.Entry(self.window, width = 50)
        self.title_entry.grid(row = 0, column = 2, padx = 10, pady = 10)

        self.description_label = ttk.Label(self.window, text = "Description:")
        self.description_label.grid(row = 1, column = 1, padx = 10, pady = (0, 10), sticky = "n")
        self.description_frame = ttk.Frame(self.window, style = "Card", borderwidth = 1)
        self.description_frame.grid(row = 1, column = 2, padx = 10, pady = (0, 10))
        self.description_entry = tk.Text(self.description_frame, width = 50, height = 20, borderwidth = 0)
        self.description_entry.grid(row = 0, column = 0, padx = 5, pady = 5)


        cal_label = ttk.Label(self.window, text = "Choose the date for the event:")
        cal_label.grid(row = 2, column = 1, padx = 10, pady = (0, 10))
        cal = DateEntry(self.window)
        cal.set_date(datetime.date.today())
        cal.grid(row = 2, column = 2, padx = 10, pady = (0, 10), sticky = "w")

        self.window.mainloop()