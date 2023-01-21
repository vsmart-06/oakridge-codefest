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
        self.description_mega_frame = ttk.Frame(self.main_frame)
        self.description_mega_frame.grid(row = 1, column = 1, pady = (0, 10), sticky = "ew")
        self.description_frame = ttk.Frame(self.description_mega_frame, style = "Card", borderwidth = 1)
        self.description_frame.grid(row = 0, column = 0, padx = 10, pady = (0, 10), sticky = "ew")
        self.description_entry = tk.Text(self.description_frame, width = 50, height = 10, borderwidth = 0)
        self.description_entry.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "ew")
        self.description_entry.bind("<FocusOut>", self.check_description)


        self.cal_label = ttk.Label(self.main_frame, text = "Choose the date for the event:")
        self.cal_label.grid(row = 2, column = 0, padx = 10, pady = (0, 10))
        self.cal = DateEntry(self.main_frame)
        self.cal.set_date(datetime.date.today())
        self.cal.grid(row = 2, column = 1, padx = 10, pady = (0, 10), sticky = "w")

        self.time_label = ttk.Label(self.main_frame, text = "Time:")
        self.time_label.grid(row = 3, column = 0, padx = 10, pady = (0, 10))
        self.time_frame = ttk.Frame(self.main_frame)
        self.time_frame.grid(row = 3, column = 1, padx = 10, pady = (0, 10), sticky = "ew")
        self.time_hour = ttk.Spinbox(self.time_frame, from_ = 0, to = 24)
        self.time_hour.grid(row = 0, column = 0)
        self.colon = ttk.Label(self.time_frame, text = " : ")
        self.colon.grid(row = 0, column = 1)
        self.time_minutes = ttk.Spinbox(self.time_frame, from_ = 0, to = 59)
        self.time_minutes.grid(row = 0, column = 2)
        self.time_hour.set("00")
        self.time_minutes.set("00")
        self.time_hour.bind("<FocusOut>", lambda m = True: self.check_time(m))
        self.time_minutes.bind("<FocusOut>", lambda m = False: self.check_time(m))

        self.location_label = ttk.Label(self.main_frame, text = "Location:")
        self.location_label.grid(row = 4, column = 0, padx = 10, pady = (0, 10), sticky = "n")
        self.location_frame = ttk.Frame(self.main_frame)
        self.location_frame.grid(row = 4, column = 1)
        self.location_entry = ttk.Entry(self.location_frame, width = 50)
        self.location_entry.grid(row = 0, column = 0, padx = 10, pady = (0, 10), sticky = "ew")
        self.location_btn = ttk.Button(self.location_frame, text = "Search", style = "Accent.TButton", command = self.search_place)
        self.location_btn.grid(row = 0, column = 1, padx = 10, pady = (0, 10))
        
        self.create_btn = ttk.Button(self.main_frame, text = "Create Event", style = "Accent.TButton", command = self.create_event)
        self.create_btn.grid(row = 5, column = 1, padx = 10, pady = (0, 10), sticky = "e")

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
            self.place_btns.append(ttk.Button(places_frame, text = place_names[x], command = lambda m = x: self.choose_place(m)))
            self.place_btns[-1].grid(row = x, column = 0, pady = (0, 5), sticky = "ew")

        self.window.update()
        self.sidebar = Sidebar(self.window)
    
    def choose_place(self, index):
        place = self.place_btns[index]["text"]
        self.location_entry.delete(0, "end")
        self.location_entry.insert(0, place)

    def check_time(self, hour):
        try:
            int(self.time_hour.get())
        except:
            self.time_hour.set("00")
        
        try:
            int(self.time_minutes.get())
        except:
            self.time_minutes.set("00")

        if hour:
            if not (0 <= int(self.time_hour.get()) <= 24):
                self.time_hour.set("00")
                
        else:
            if not (0 <= int(self.time_minutes.get()) <= 59):
                self.time_hour.set("00")
    
    def check_description(self, m):
        description = self.description_entry.get("1.0", "end-1c").strip()
        if len(description.split()) > 300:
            description = description.split()[:300]
            self.error_lbl = ttk.Label(self.description_mega_frame, text = "Make your description within 300 words", foreground = "red")
            self.error_lbl.grid(row = 1, column = 0)
        else:
            try:
                self.error_lbl.grid_forget()
            except:
                pass


    def create_event(self):
        title = self.title_entry.get()
        description = self.description_entry.get("1.0", "end-1c")
        date = self.cal.get_date()
        time = self.time_hour.get()+":"+self.time_minutes.get()
        location = self.location_entry.get()


Events()