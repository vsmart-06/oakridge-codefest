import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
from sidebar import Sidebar
import os
import dotenv
import requests

dotenv.load_dotenv()

API_KEY = os.getenv("API_KEY")

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
        self.title_entry.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "ew")

        self.description_label = ttk.Label(self.main_frame, text = "Description:")
        self.description_label.grid(row = 1, column = 0, padx = 10, pady = (0, 10), sticky = "n")
        self.description_frame = ttk.Frame(self.main_frame, style = "Card", borderwidth = 1)
        self.description_frame.grid(row = 1, column = 1, padx = 10, pady = (0, 10), sticky = "ew")
        self.description_entry = tk.Text(self.description_frame, width = 50, height = 20, borderwidth = 0)
        self.description_entry.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "ew")


        self.cal_label = ttk.Label(self.main_frame, text = "Choose the date for the event:")
        self.cal_label.grid(row = 2, column = 0, padx = 10, pady = (0, 10))
        self.cal = DateEntry(self.main_frame)
        self.cal.set_date(datetime.date.today())
        self.cal.grid(row = 2, column = 1, padx = 10, pady = (0, 10), sticky = "w")

        self.time_label = ttk.Label(self.main_frame, text = "Time: ")
        self.time_label.grid(row = 3, column = 0, padx = 10, pady = (0, 10))
        self.time_frame = ttk.Frame(self.main_frame)
        self.time_frame.grid(row = 3, column = 1, padx = 10, pady = (0, 10), sticky = "ew")
        self.time_hour = ttk.Spinbox(self.time_frame, from_ = 0, to = 24)
        self.time_hour.grid(row = 0, column = 0)
        self.colon = ttk.Label(self.time_frame, text = " : ")
        self.colon.grid(row = 0, column = 1)
        self.time_minutes = ttk.Spinbox(self.time_frame, from_ = 0, to = 59)
        self.time_minutes.grid(row = 0, column = 2)
        self.time_hour.set(0)
        self.time_minutes.set(0)

        self.location_label = ttk.Label(self.main_frame, text = "Location:")
        self.location_label.grid(row = 4, column = 0, padx = 10, pady = (0, 10), sticky = "n")
        self.location_frame = ttk.Frame(self.main_frame)
        self.location_frame.grid(row = 4, column = 1)
        self.location_entry = ttk.Entry(self.location_frame, width = 50)
        self.location_entry.grid(row = 0, column = 0, padx = 10, pady = (0, 10), sticky = "ew")
        self.location_btn = ttk.Button(self.location_frame, text = "Search", style = "Accent.TButton", command = self.search_place)
        self.location_btn.grid(row = 0, column = 1, padx = 10, pady = (0, 10))

        self.window.update()
        self.sidebar = Sidebar(self.window)

        self.window.mainloop()
    
    def search_place(self):
        place_string = self.location_entry.get()
        places = requests.get(f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={place_string}&key={API_KEY}").json()["predictions"]
        place_names = [x["description"] for x in places]
        if len(place_names) > 5:
            place_names = place_names[:5]
        
        places_frame = ttk.Frame(self.location_frame)
        places_frame.grid(row = 1, column = 0, sticky = "ew")
        
        self.place_btns = []
        for x in range(len(place_names)):
            self.place_btns.append(ttk.Button(places_frame, text = place_names[x]))
            self.place_btns[-1].grid(row = x, column = 0, pady = (0, 5), sticky = "ew")

        self.window.update()
        self.sidebar = Sidebar(self.window)

Events()