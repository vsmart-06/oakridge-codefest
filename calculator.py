import requests
import tkinter as tk
from tkinter import ttk
from pichart import IP
from sidebar import Sidebar


class Calculator:
    def __init__(self, username: str):
        self.username = username
        self.root = tk.Tk()
        self.root.title("How Green?")
        self.root.geometry("350x400")
        self.root.tk.call("source", "./oakridge-codefest/forest-dark.tcl")
        ttk.Style().theme_use("forest-dark")

        frame = ttk.Frame(self.root)
        frame.grid(row = 0, column = 1, padx = 10)

        label = ttk.Label(frame, text = '''
Upon initiation, our code utilises your IP address 
to determine your location. This information is 
utilised to determine the proportion of renewable 
and non-renewable sources of electricity in your 
region. This is of paramount importance as society 
is increasingly utilising electrical appliances, 
such as electric vehicles, and it is crucial to 
have knowledge of the environmental impact of 
the electricity being consumed.''')
        label.grid(row = 0, column = 1, pady = 10)

        self.value = 1
        

        button = ttk.Button(frame, text = "Start", command = self.changeValue, style = "Accent.TButton")
        button.grid(row = 1, column = 1, ipadx = 10, ipady = 5)

        self.root.update()
        self.sidebar = Sidebar(self.root, self.username)

        self.root.mainloop()
        
    def changeValue(self):
        self.root.destroy()
        self.value -= 1
        if self.value == 0:
            obj = IP()
            obj.username = self.username
            obj.create_graph()
            Calculator(self.username)

            self.value = 1
        else:
            pass