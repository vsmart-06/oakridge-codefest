import tkinter as tk
from tkinter import ttk
from records import *

class Login:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Login")
        self.window.tk.call("source", "./my-private-repo/forest-dark.tcl")
        ttk.Style().theme_use("forest-dark")

        self.username_lbl = ttk.Label(self.window, text = "Username: ")
        self.password_lbl = ttk.Label(self.window, text = "Password: ")
        self.username_lbl.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.password_lbl.grid(row = 1, column = 0, padx = 10)

        self.username_ent = ttk.Entry(self.window)
        self.password_ent = ttk.Entry(self.window)
        self.username_ent.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.password_ent.grid(row = 1, column = 1, padx = 10)

        self.login_btn = ttk.Button(self.window, text = "Login", command = self.login)
        self.signup_btn = ttk.Button(self.window, text = "Sign up", style = "Accent.TButton", command = self.signup)
        self.login_btn.grid(row = 2, column = 0, columnspan = 2, pady = 10)
        self.signup_btn.grid(row = 3, column = 0, columnspan = 2)

        self.error_lbl = ttk.Label(self.window, text = "")
        self.error_lbl.grid(row = 4, column = 0, columnspan = 2)

        self.window.mainloop()

    def login(self):
        username = self.username_ent.get()
        password = self.password_ent.get()
        result = user_login(username, password)
        if not result:
            msg = "Invalid username or password"
            colour = "red"
        else:
            msg = "Logged in successfully!"
            colour = "green"
        self.error_lbl.config(text = msg, foreground = colour)

    def signup(self):
        username = self.username_ent.get()
        password = self.password_ent.get()
        result = user_signup(username, password)
        if not result:
            msg = "Username already exists"
            colour = "red"
        else:
            msg = "Account created successfully!"
            colour = "green"
        self.error_lbl.config(text = msg, foreground = colour)