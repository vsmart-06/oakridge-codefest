import tkinter as tk
from tkinter import ttk

class Sidebar:
    def __init__(self, window: tk.Tk):
        self.window = window
        self.min_width = 0
        self.max_width = 120
        self.cur_width = self.min_width
        
        self.frame = ttk.Frame(self.window, height = self.window.winfo_height(), width = self.max_width)
        self.frame.grid(row = 0, column = 0)
        self.frame.grid_propagate(False)

        self.side_btn = ttk.Button(self.frame, text = "≡", width = 3, command = self.change)
        self.side_btn.grid(row = 0, column = 0, pady = 10, padx = 10, sticky = "w")

        self.sidebar = ttk.Frame(self.frame, height = self.window.winfo_height(), width = self.cur_width, style = "Card")
        self.sidebar.grid(row = 1, column = 0, sticky = "w")
        self.sidebar.grid_propagate(False)

        self.home_btn = ttk.Button(self.sidebar, text = "Home", style = "Accent.TButton")
        self.green_btn = ttk.Button(self.sidebar, text = "How green?", style = "Accent.TButton")
        self.posts_btn = ttk.Button(self.sidebar, text = "Forum", style = "Accent.TButton")
        self.events_btn = ttk.Button(self.sidebar, text = "Events", style = "Accent.TButton")
        self.logout_btn = ttk.Button(self.sidebar, text = "Log out", style = "Accent.TButton")
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