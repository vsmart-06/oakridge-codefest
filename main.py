from login_page import Login
from event_page import Event

login_page = Login()
event_page = Event(login_page.username)