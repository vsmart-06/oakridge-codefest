# importing the requests library
import requests
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from sidebar import Sidebar
from PIL import Image,ImageTk
class IP:
    def __init__(self, username: str):
        self.username = username


    def percentdata(self):

        # Python Program to Get IP Address
        IPAddr = self.getIp()

        #getting geolocation
        geodata = self.getGeoLocation(IPAddr)

        #check if it is in india
        if(geodata["country"]!="India"):
            return False

        #find tbe distribution of fuel
        state_data = self.fuelDistribution(geodata)

        #check percentage
        percentdata = state_data 
        for x in list(percentdata)[4:] :
            percentdata[x]=(float)(percentdata[x])/float(percentdata["grand_total"])*100
        
        #print(percentdata)
        #return percentdata
        coal = float(percentdata["coal"])
        gas = float(percentdata["gas"])
        diesel = float(percentdata["diesel"])
        thermal_total = float(percentdata["thermal_total"])
        nuclear = float(percentdata["nuclear"])
        hydro = float(percentdata["hydro"])
        res = float(percentdata["res"])
        arr = [coal, gas, diesel, thermal_total, nuclear, hydro, res]
        return arr

    # Python Program to Get IP Address
    def getIp(self):
        ip = requests.get('https://api.ipify.org').content.decode('utf8')
        IPAddr = format(ip)
        return IPAddr
        #print(IPAddr)

    #getting geolocation
    def getGeoLocation(self, IPAddr):
        URL = f"http://ip-api.com/json/{IPAddr}?fields=country,regionName"
        r = requests.get(URL)
        geodata = r.json()
        return geodata
        #print(geodata)

    def fuelDistribution(self, geodata):
        #find tbe distribution of fuel
        URL= "https://cea.nic.in/api/installed_capacity_statewise.php"
        r = requests.get(URL)
        data = r.json()
        data = data[::-1]
        states = [x["state"] for x in data]
        index = states.index(geodata["regionName"])
        state_data = data[index]
        #print(state_data)
        return state_data

    def create_graph(self):
        root = tk.Tk()
        root.title("How Green Are You?")
        root.geometry("850x650")
        root.tk.call("source", "./oakridge-codefest/forest-dark.tcl")
        ttk.Style().theme_use("forest-dark")

        frame=ttk.Frame(root)
        frame.grid(row=0, column=1, padx=10)

        ttk.Label(frame, text='Pie Chart').grid(row=0, column=1)

        # create pie chart and save as image How Green?
        array = self.percentdata()
        y = np.array([array[0], array[1], array[2], array[3], array[4], array[5], array[6]])
        mylabels = ["Coal", "Gas", "Diesel", "Total Thermal", "Nuclear", "Hydro", "Renewable Energy Sources"]
        colors=['#7FFFD4','#097969','#AAFF00','#228B22','#32CD32','#2AAA8A','#98FB98']

        plt.pie(y, colors=colors, autopct='%1.2f%%')
        plt.legend(labels=mylabels)
        plt.savefig("./oakridge-codefest/How_Green.png")  
        
        # Create an object of tkinter ImageTk
        img = ImageTk.PhotoImage(Image.open("./oakridge-codefest/How_Green.png"))

        # Create a Label Widget to display the text or Image
        label = ttk.Label(frame, image = img)
        label.grid(row=1, column=1)

        root.update()
        self.sidebar = Sidebar(root, self.username, True)
        

        root.mainloop()




