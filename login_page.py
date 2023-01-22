import tkinter as tk
from tkinter import ttk
from records import *

class Login:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Login")
        self.window.tk.call("source", "./oakridge-codefest/forest-dark.tcl")
        ttk.Style().theme_use("forest-dark")

        self.username_lbl = ttk.Label(self.window, text = "Username: ")
        self.password_lbl = ttk.Label(self.window, text = "Password: ")
        self.username_lbl.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.password_lbl.grid(row = 1, column = 0, padx = 10)

        self.username_frame = ttk.Frame(self.window)
        self.password_frame = ttk.Frame(self.window)
        self.username_frame.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.password_frame.grid(row = 1, column = 1, padx = 10)
        self.username_ent = ttk.Entry(self.username_frame)
        self.password_ent = ttk.Entry(self.password_frame)
        self.username_ent.grid(row = 0, column = 0)
        self.password_ent.grid(row = 0, column = 0)

        self.login_btn = ttk.Button(self.window, text = "Login", command = self.login)
        self.signup_btn = ttk.Button(self.window, text = "Sign up", style = "Accent.TButton", command = self.signup)
        self.login_btn.grid(row = 2, column = 0, columnspan = 2, pady = 10)
        self.signup_btn.grid(row = 3, column = 0, columnspan = 2)

        self.error_lbl = ttk.Label(self.window, text = "")
        self.error_lbl.grid(row = 4, column = 0, columnspan = 2)

        self.window.mainloop()

    def login(self):
        self.username = self.username_ent.get().strip()
        self.password = self.password_ent.get().strip()
        result = user_login(self.username, self.password)
        if not result:
            msg = "Invalid username or password"
            colour = "red"
        else:
            msg = "Logged in successfully!"
            colour = "green"
            self.logged_in = True
        self.error_lbl.config(text = msg, foreground = colour)
        if result:
            self.window.destroy()

    def signup(self):
        self.username = self.username_ent.get().strip()
        self.password = self.password_ent.get().strip()
        try:
            self.error_lbl_usr.grid_forget()
        except:
            pass
        if self.username == "":
            self.error_lbl_usr = ttk.Label(self.username_frame, text = "Invalid username", foreground = "red")
            self.error_lbl_usr.grid(row = 1, column = 0, pady = 10)
            return
        for x in self.username:
            if not (x.isalpha() or x.isnumeric() or x in ["-", "_"]):
                self.error_lbl_usr = ttk.Label(self.username_frame, text = "Invalid username", foreground = "red")
                self.error_lbl_usr.grid(row = 1, column = 0, pady = 10)
                return
        try:
            self.error_lbl_pwd.grid_forget()
        except:
            pass
        if self.password == "":
            self.error_lbl_pwd = ttk.Label(self.username_frame, text = "Invalid password", foreground = "red")
            self.error_lbl_pwd.grid(row = 1, column = 0, pady = 10)
            return
        caps = False
        small = False
        spcl = False
        num = False
        for x in self.password:
            if not(x.isnumeric() or x.isalpha()):
                spcl = True
            elif x.isnumeric():
                num = True
            elif x.upper() == x:
                caps = True
            elif x.lower() == x:
                small = True
        if not (caps and small and spcl and num):
            self.error_lbl_pwd = ttk.Label(self.password_frame, text = "Invalid password", foreground = "red")
            self.error_lbl_pwd.grid(row = 1, column = 0, pady = 10)
            return
        result = user_signup(self.username, self.password)
        if not result:
            msg = "Username already exists"
            colour = "red"
        else:
            msg = "Account created successfully!"
            colour = "green"
        self.error_lbl.config(text = msg, foreground = colour)