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

        self.main_frame = ttk.Frame(self.window)
        self.main_frame.grid(row = 0, column = 1)

        self.title_label = ttk.Label(self.main_frame, text = "Title:")
        self.title_label.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.title_entry = ttk.Entry(self.main_frame, width = 50)
        self.title_entry.grid(row = 0, column = 1, padx = 10, pady = 10)

        self.description_label = ttk.Label(self.main_frame, text = "Description:")
        self.description_label.grid(row = 1, column = 0, padx = 10, pady = (0, 10), sticky = "n")
        self.description_frame = ttk.Frame(self.main_frame, style = "Card", borderwidth = 1)
        self.description_frame.grid(row = 1, column = 1, padx = 10, pady = (0, 10))
        self.description_entry = tk.Text(self.description_frame, width = 50, height = 20, borderwidth = 0)
        self.description_entry.grid(row = 0, column = 0, padx = 5, pady = 5)


        self.cal_label = ttk.Label(self.main_frame, text = "Choose the date for the event:")
        self.cal_label.grid(row = 2, column = 0, padx = 10, pady = (0, 10))
        self.cal = DateEntry(self.main_frame)
        self.cal.set_date(datetime.date.today())
        self.cal.grid(row = 2, column = 1, padx = 10, pady = (0, 10), sticky = "w")

        self.sidebar = Sidebar(self.window)

        self.window.mainloop()