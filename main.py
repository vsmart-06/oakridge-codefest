from login_page import Login
from home_page import Home

login_page = Login()
home_page = Home(login_page.username)