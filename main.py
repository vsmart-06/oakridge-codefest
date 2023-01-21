import tkinter as tk
from tkinter import ttk
from login_page import Login
from event_page import EventCreate

login_page = Login()
event_page = EventCreate(login_page.username)