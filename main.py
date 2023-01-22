from login_page import Login
from home_page import Home

while True:
    login_page = Login()
    try:
        if login_page.logged_in:
            home_page = Home(login_page.username)
        else:
            break
    except:
        break