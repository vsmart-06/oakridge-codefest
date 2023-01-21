import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
from sidebar import Sidebar
import os
import dotenv
import requests
from records import new_event, get_event, join_event

dotenv.load_dotenv()

API_KEY = os.getenv("API_KEY")

class Event:
    def __init__(self, username: str):
        self.username = username
        self.window = tk.Tk()
        self.window.title("Events")
        self.window.tk.call("source", "./oakridge-codefest/forest-dark.tcl")
        ttk.Style().theme_use("forest-dark")

        all_events = get_event()
        all_posts = []
        self.main_frame = ttk.Frame(self.window)
        self.main_frame.grid(row = 0, column = 1, padx = 10)
        for x in range(len(all_events)):
            mega_frame = ttk.Frame(self.main_frame)
            mega_frame.grid(row = x, column = 1, pady = 10)
            title_lbl = ttk.Label(mega_frame, text = all_events[x][2])
            title_lbl.grid(row = 0, column = 0, pady = 10)
            mini_frame = ttk.Frame(mega_frame)
            mini_frame.grid(row = 1, column = 0)
            join_btn = ttk.Button(mini_frame, text = "Join Event", style = "Accent.TButton", command = lambda m = all_events[x][0]: join_event(m, self.username))
            join_btn.grid(row = 0, column = 0, padx = 10)
            details_btn = ttk.Button(mini_frame, text = "More Details", command = lambda m = all_events[x][0]: EventView(self.username, m))
            details_btn.grid(row = 0, column = 1, padx = 10)
            all_posts.append(mega_frame)
        
        self.window.update()
        if self.window.winfo_height() < 300:
            self.window.geometry("500x300")
        self.window.update()
        self.sidebar = Sidebar(self.window)

        self.window.mainloop()

class EventView:
    def __init__(self, username: str, id: int):
        self.window = tk.Tk()
        self.window.title("Events")
        self.window.tk.call("source", "./oakridge-codefest/forest-dark.tcl")
        ttk.Style().theme_use("forest-dark")

        event_data = get_event(id)

        self.main_frame = ttk.Frame(self.window)
        self.main_frame.grid(row = 0, column = 1)

        title_name_lbl = ttk.Label(self.main_frame, text = "Title:")
        title_name_lbl.grid(row = 0, column = 0, pady = 10, padx = 10)
        title_lbl = ttk.Label(self.main_frame, text = event_data[2])
        title_lbl.grid(row = 0, column = 1, pady = 10, padx = 10)

        description_name_lbl = ttk.Label(self.main_frame, text = "Description:")
        description_name_lbl.grid(row = 1, column = 0, pady = (0, 10), padx = 10)
        description_lbl = ttk.Label(self.main_frame, text = event_data[3])
        description_lbl.grid(row = 1, column = 1, pady = (0, 10))

        date_name_lbl = ttk.Label(self.main_frame, text = "Date:")
        date_name_lbl.grid(row = 2, column = 0, pady = (0, 10), padx = 10)
        date_lbl = ttk.Label(self.main_frame, text = event_data[4])
        date_lbl.grid(row = 2, column = 1, pady = (0, 10))

        time_name_lbl = ttk.Label(self.main_frame, text = "Time:")
        time_name_lbl.grid(row = 3, column = 0, pady = (0, 10), padx = 10)
        time_lbl = ttk.Label(self.main_frame, text = event_data[5])
        time_lbl.grid(row = 3, column = 1, pady = (0, 10))

        location_name_lbl = ttk.Label(self.main_frame, text = "Location:")
        location_name_lbl.grid(row = 4, column = 0, pady = (0, 10), padx = 10)
        location_lbl = ttk.Label(self.main_frame, text = event_data[6])
        location_lbl.grid(row = 4, column = 1, pady = (0, 10))

        author_name_lbl = ttk.Label(self.main_frame, text = "Description:")
        author_name_lbl.grid(row = 5, column = 0, pady = (0, 10), padx = 10)
        author_lbl = ttk.Label(self.main_frame, text = username)
        author_lbl.grid(row = 5, column = 1)

        attendees_name_lbl = ttk.Label(self.main_frame, text = "Attendees:")
        attendees_name_lbl.grid(row = 6, column = 0, pady = (0, 10), padx = 10)
        attendees_lbl = ttk.Label(self.main_frame, text = len(event_data[7].split(",")))
        attendees_lbl.grid(row = 6, column = 1)


class EventCreate:
    def __init__(self, username: str):
        self.username = username
        self.window = tk.Tk()
        self.window.title("Events")
        self.window.tk.call("source", "./oakridge-codefest/forest-dark.tcl")
        ttk.Style().theme_use("forest-dark")

        self.main_frame = ttk.Frame(self.window)
        self.main_frame.grid(row = 0, column = 1)

        self.title_label = ttk.Label(self.main_frame, text = "Title:")
        self.title_label.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.title_mega_frame = ttk.Frame(self.main_frame)
        self.title_mega_frame.grid(row = 0, column = 1, sticky = "ew")
        self.title_entry = ttk.Entry(self.title_mega_frame, width = 50)
        self.title_entry.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "ew")
        self.title_entry.bind("<FocusOut>", self.check_title)

        self.description_label = ttk.Label(self.main_frame, text = "Description:")
        self.description_label.grid(row = 1, column = 0, padx = 10, pady = (0, 10), sticky = "n")
        self.description_mega_frame = ttk.Frame(self.main_frame)
        self.description_mega_frame.grid(row = 1, column = 1, sticky = "ew")
        self.description_frame = ttk.Frame(self.description_mega_frame, style = "Card", borderwidth = 1)
        self.description_frame.grid(row = 0, column = 0, padx = 10, pady = (0, 10), sticky = "ew")
        self.description_entry = tk.Text(self.description_frame, width = 50, height = 10, borderwidth = 0)
        self.description_entry.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "ew")
        self.description_entry.bind("<FocusOut>", self.check_description)


        self.cal_label = ttk.Label(self.main_frame, text = "Choose the date for the event:")
        self.cal_label.grid(row = 2, column = 0, padx = 10, pady = (0, 10))
        self.cal_mega_frame = ttk.Frame(self.main_frame)
        self.cal_mega_frame.grid(row = 2, column = 1, sticky = "ew")
        self.cal = DateEntry(self.cal_mega_frame)
        self.cal.set_date(datetime.date.today())
        self.cal.grid(row = 0, column = 0, padx = 10, pady = (0, 10), sticky = "w")

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
    
    def check_title(self, m):
        title = self.title_entry.get().strip()
        if len(title.split()) > 10:
            self.error_lbl_title = ttk.Label(self.title_mega_frame, text = "Make your title within 10 words", foreground = "red")
            self.error_lbl_title.grid(row = 1, column = 0, pady = (0, 10))
        else:
            if title == "":
                self.error_lbl_title = ttk.Label(self.title_mega_frame, text = "Title is a required field", foreground = "red")
                self.error_lbl_title.grid(row = 1, column = 0, pady = (0, 10))
                return
            try:
                self.error_lbl_title.grid_forget()
            except:
                pass


    def check_description(self, m):
        description = self.description_entry.get("1.0", "end-1c").strip()
        if len(description.split()) > 300:
            self.error_lbl_description = ttk.Label(self.description_mega_frame, text = "Make your description within 300 words", foreground = "red")
            self.error_lbl_description.grid(row = 1, column = 0, pady = (0, 10))
        else:
            try:
                self.error_lbl_description.grid_forget()
            except:
                pass
    
    def check_date(self):
        chosen_date = self.cal.get_date()
        today = datetime.date.today()
        if str(chosen_date - today)[0] == "-":
            self.error_lbl_date = ttk.Label(self.cal_mega_frame, text = "You cannot organize an event before today!", foreground = "red")
            self.error_lbl_date.grid(row = 1, column = 0, pady = (0, 10), padx = 10)
            return False
        else:
            try:
                self.error_lbl_date.grid_forget()
            except:
                pass
            return True


    def create_event(self):
        title = self.title_entry.get().strip()
        description = self.description_entry.get("1.0", "end-1c").strip()
        date = self.cal.get_date()
        time = self.time_hour.get()+":"+self.time_minutes.get()
        location = self.location_entry.get().strip()
        title = f"'{title}'"
        if description == "":
            description = "NULL"
        else:
            description = f"'{description}'"
        if not self.check_date():
            return
        date = f"'{date}'"
        time = f"'{time}'"
        if location == "":
            location = "NULL"
        else:
            location = f"'{location}'"

        new_event(self.username, title, description, date, time, location)

Event("vishnu")