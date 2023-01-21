import requests
import tkinter as tk
from tkinter import ttk
from pichart import IP
from sidebar import Sidebar


class Calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("How Green Are You?")
        self.root.geometry("350x400")
        self.root.tk.call("source", "./oakridge-codefest/forest-dark.tcl")
        ttk.Style().theme_use("forest-dark")

        frame=ttk.Frame(self.root)
        frame.grid(row=0, column=1, padx=10)

        label = ttk.Label(frame, text="How Green Are You?", style="Accent.TLabel")
        label.grid(row=0, column=1)

        self.value = 1
        

        button = ttk.Button(frame, text="START", command=self.changeValue, style="Accent.TButton")
        ttk.Style().configure('TButton')
        button.grid(row=1, column=1,ipadx=10, ipady=5)

        self.root.update()
        self.sidebar = Sidebar(self.root)


        self.root.mainloop()
        
    def changeValue(self):
        self.root.destroy()
        self.value -= 1
        if self.value == 0:
            obj = IP()
            obj.create_graph()
            Calculator()

            self.value = 1
        else:
            pass       

Calculator()

# , font=('Times', 80)
# , font=(None, 20)
