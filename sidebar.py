import tkinter as tk
from tkinter import ttk
from home_page import Home
from calculator import Calculator
from event_page import Event

class Sidebar:
    def __init__(self, window: tk.Tk, username: str, expand: bool = False):
        self.username = username
        self.window = window
        self.min_width = 0
        self.max_width = 120

        self.frame = ttk.Frame(self.window, height = self.window.winfo_height(), width = self.max_width)
        self.frame.grid(row = 0, column = 0)
        self.frame.grid_propagate(False)

        if not expand:
            self.cur_width = self.min_width
            self.expanded = False
            self.side_btn = ttk.Button(self.frame, text = "≡", width = 3, command = self.change)
        else:
            self.cur_width = self.max_width
            self.expanded = True
            self.side_btn = ttk.Button(self.frame, text = "|||", width = 3, command = self.change)

        self.side_btn.grid(row = 0, column = 0, pady = 10, padx = 10, sticky = "w")

        self.sidebar = ttk.Frame(self.frame, height = self.window.winfo_height(), width = self.cur_width, style = "Card")
        self.sidebar.grid(row = 1, column = 0, sticky = "w")
        self.sidebar.grid_propagate(False)

        self.home_btn = ttk.Button(self.sidebar, text = "Home", style = "Accent.TButton", command = lambda m = 0: self.open_tab(m))
        self.green_btn = ttk.Button(self.sidebar, text = "How green?", style = "Accent.TButton", command = lambda m = 1: self.open_tab(m))
        self.posts_btn = ttk.Button(self.sidebar, text = "Forum", style = "Accent.TButton", command = lambda m = 2: self.open_tab(m))
        self.events_btn = ttk.Button(self.sidebar, text = "Events", style = "Accent.TButton", command = lambda m = 3: self.open_tab(m))
        self.logout_btn = ttk.Button(self.sidebar, text = "Log out", style = "Accent.TButton", command = lambda m = 4: self.open_tab(m))
        self.home_btn.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.green_btn.grid(row = 1, column = 0, padx = 10)
        self.posts_btn.grid(row = 2, column = 0, padx = 10, pady = 10)
        self.events_btn.grid(row = 3, column = 0, padx = 10)
        self.logout_btn.grid(row = 4, column = 0, padx = 10, pady = 10)

        self.expanded = False
    
    def change(self):
        if not self.expanded:
            rep = self.window.after(5, self.change)
            self.cur_width += 10
            self.sidebar.config(width = self.cur_width)
            if self.cur_width >= self.max_width:
                self.window.after_cancel(rep)
                self.expanded = True
                self.side_btn.config(text = "|||")
        else:
            rep = self.window.after(5, self.change)
            self.cur_width -= 10
            self.sidebar.config(width = self.cur_width)
            if self.cur_width <= self.min_width:
                self.window.after_cancel(rep)
                self.expanded = False
                self.side_btn.config(text = "≡")

    def open_tab(self, index):
        self.window.destroy()
        if index == 0:
            Home(self.username)
        elif index == 1:
            Calculator(self.username)
        elif index == 3:
            Event(self.username)
