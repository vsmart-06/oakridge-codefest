import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
import ics
from sidebar import Sidebar
import os
import dotenv
import requests
from records import new_event, get_event, join_event

dotenv.load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

def generate_ics(cal: ics.Calendar, title: str, description: str, time: str, date: str, location: str):
    event = ics.Event()
    event.name = title
    year, month, day = list(map(int, date.split("-")))
    hours, minutes = list(map(int, time.split(":")))
    time = datetime.datetime(year, month, day, hours, minutes)
    event.begin = time-datetime.timedelta(hours = 5, minutes = 30)
    event.location = location
    event.description = description

    cal.events.add(event)

    return cal

class Event:
    def __init__(self, username: str, old_window: tk.Tk = None, cal: ics.Calendar = ics.Calendar()):
        self.cal_ics = cal
        if old_window:
            old_window.destroy()
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
            join_btn = ttk.Button(mini_frame, text = "Join Event", style = "Accent.TButton", command = lambda m = all_events[x][0]: self.join_btn(m))
            join_btn.grid(row = 0, column = 0, padx = 10)
            details_btn = ttk.Button(mini_frame, text = "More Details", command = lambda m = all_events[x][0]: EventView(self.username, m, self.window, cal = self.cal_ics))
            details_btn.grid(row = 0, column = 1, padx = 10)
            all_posts.append(mega_frame)
        
        self.length = len(all_events)
        create_event_btn = ttk.Button(self.main_frame, text = "Create Event", style = "Accent.TButton", command = self.create_event)
        create_event_btn.grid(row = self.length, column = 1, pady = (0, 10))

        download_ics_btn = ttk.Button(self.main_frame, text = "Download .ics File", command = self.download)
        download_ics_btn.grid(row = self.length+1, column = 1, pady = (0, 10))

        self.window.update()
        if self.window.winfo_height() < 300:
            self.window.geometry("500x300")
        self.window.update()
        self.sidebar = Sidebar(self.window, self.username)

        self.window.mainloop()
    
    def create_event(self):
        self.window.destroy()
        EventCreate(self.username, self.cal_ics)
    
    def download(self):
        if len(self.cal_ics.events) == 0:
            error_lbl = ttk.Label(self.main_frame, text = "You do not have an .ics file to download!", foreground = "red")
            error_lbl.grid(row = self.length+2, column = 1)
        else:
            with open('./oakridge-codefest/my_events.ics', 'w') as f: f.writelines(self.cal_ics.serialize_iter())
            

    def join_btn(self, id):
        join_event(id, self.username)
        sub_window = tk.Toplevel()
        ttk.Label(sub_window, text = "You have successfully joined the event!", borderwidth = 1).pack(padx = 10, pady = 10)
        event_data = get_event(id)
        self.cal_ics = generate_ics(self.cal_ics, event_data[2], event_data[3], event_data[5], event_data[4], event_data[6])

class EventView:
    def __init__(self, username: str, id: int, old_window: tk.Tk, cal: ics.Calendar = ics.Calendar()):
        self.cal_ics = cal
        old_window.destroy()
        self.username = username
        self.window = tk.Tk()
        self.window.title("Events")
        self.window.tk.call("source", "./oakridge-codefest/forest-dark.tcl")
        ttk.Style().theme_use("forest-dark")

        self.event_data = get_event(id)

        self.main_frame = ttk.Frame(self.window)
        self.main_frame.grid(row = 0, column = 1)

        title_name_lbl = ttk.Label(self.main_frame, text = "Title:")
        title_name_lbl.grid(row = 0, column = 0, pady = 10, padx = 10)
        title_lbl = ttk.Label(self.main_frame, text = self.event_data[2])
        title_lbl.grid(row = 0, column = 1, pady = 10, padx = 10)

        description_name_lbl = ttk.Label(self.main_frame, text = "Description:")
        description_name_lbl.grid(row = 1, column = 0, pady = (0, 10), padx = 10)
        description_lbl = ttk.Label(self.main_frame, text = self.event_data[3])
        description_lbl.grid(row = 1, column = 1, pady = (0, 10))

        date_name_lbl = ttk.Label(self.main_frame, text = "Date:")
        date_name_lbl.grid(row = 2, column = 0, pady = (0, 10), padx = 10)
        date_lbl = ttk.Label(self.main_frame, text = self.event_data[4])
        date_lbl.grid(row = 2, column = 1, pady = (0, 10))

        time_name_lbl = ttk.Label(self.main_frame, text = "Time:")
        time_name_lbl.grid(row = 3, column = 0, pady = (0, 10), padx = 10)
        time_lbl = ttk.Label(self.main_frame, text = self.event_data[5])
        time_lbl.grid(row = 3, column = 1, pady = (0, 10))

        location_name_lbl = ttk.Label(self.main_frame, text = "Location:")
        location_name_lbl.grid(row = 4, column = 0, pady = (0, 10), padx = 10)
        location_lbl = ttk.Label(self.main_frame, text = self.event_data[6])
        location_lbl.grid(row = 4, column = 1, pady = (0, 10))

        author_name_lbl = ttk.Label(self.main_frame, text = "Author:")
        author_name_lbl.grid(row = 5, column = 0, pady = (0, 10), padx = 10)
        author_lbl = ttk.Label(self.main_frame, text = self.event_data[1])
        author_lbl.grid(row = 5, column = 1)

        attendees_name_lbl = ttk.Label(self.main_frame, text = "Attendees:")
        attendees_name_lbl.grid(row = 6, column = 0, pady = (0, 10), padx = 10)
        try:
            text = len(self.event_data[7].split(","))
        except:
            text = 0
        attendees_lbl = ttk.Label(self.main_frame, text = text)
        attendees_lbl.grid(row = 6, column = 1)

        back_btn = ttk.Button(self.main_frame, text = "Back", command = lambda m = self.username: Event(m, self.window, self.cal_ics))
        back_btn.grid(row = 7, column = 0, pady = (0, 10))
        join_btn = ttk.Button(self.main_frame, text = "Join Event", style = "Accent.TButton", command = lambda m = id: self.join_btn(m))
        join_btn.grid(row = 7, column = 1, pady = (0, 10))

        self.window.update()
        self.sidebar = Sidebar(self.window, self.username)
        self.window.mainloop()
    
    def join_btn(self, id):
        join_event(id, self.username)
        sub_window = tk.Toplevel()
        ttk.Label(sub_window, text = "You have successfully joined the event!", borderwidth = 1).pack(padx = 10, pady = 10)
        self.cal_ics = generate_ics(self.cal_ics, self.event_data[2], self.event_data[3], self.event_data[5], self.event_data[4], self.event_data[6])


class EventCreate:
    def __init__(self, username: str, cal: ics.Calendar = ics.Calendar()):
        self.cal_ics = cal
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
        
        btns_frame = ttk.Frame(self.main_frame)
        btns_frame.grid(row = 5, column = 1)
        self.create_btn = ttk.Button(btns_frame, text = "Create Event", style = "Accent.TButton", command = self.create_event)
        self.create_btn.grid(row = 0, column = 1, padx = 10, pady = (0, 10))
        self.back_btn = ttk.Button(btns_frame, text = "Back", command = lambda m = self.username: Event(m, self.window, self.cal_ics))
        self.back_btn.grid(row = 0, column = 0, padx = 10, pady = (0, 10))

        self.window.update()
        self.sidebar = Sidebar(self.window, self.username)

        self.window.mainloop()
    
    def search_place(self):
        place_string = self.location_entry.get()
        places = requests.get(f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={place_string}&key={API_KEY}").json()["predictions"]
        place_names = [x["description"] for x in places]
        if len(place_names) > 5:
            place_names = place_names[:5]
        
        try:
            self.places_frame.destroy()
        except:
            pass
        self.places_frame = ttk.Frame(self.location_frame)
        self.places_frame.grid(row = 1, column = 0, sticky = "ew")
        
        self.place_btns = []
        for x in range(len(place_names)):
            self.place_btns.append(ttk.Button(self.places_frame, text = place_names[x], command = lambda m = x: self.choose_place(m)))
            self.place_btns[-1].grid(row = x, column = 0, pady = (0, 5), sticky = "ew")

        self.window.update()
        self.sidebar = Sidebar(self.window, self.username)
    
    def choose_place(self, index):
        place = self.place_btns[index]["text"]
        self.location_entry.delete(0, "end")
        self.location_entry.insert(0, place)
        self.places_frame.destroy()
        self.sidebar.side_btn.grid_forget()
        self.sidebar.sidebar.grid_forget()
        self.window.update()
        self.sidebar = Sidebar(self.window, self.username)

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
        if title == "":
            return
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

        self.window.destroy()
        sub_window = tk.Tk()
        sub_window.title("Events")
        sub_window.tk.call("source", "./oakridge-codefest/forest-dark.tcl")
        ttk.Style().theme_use("forest-dark")
        confirmation = ttk.Label(sub_window, text = "You have successfully created the event!", borderwidth = 1)
        confirmation.pack(padx = 10, pady = 10)
        sub_window.mainloop()
        Event(self.username, cal = self.cal_ics)