# importing the requests library
import requests
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from sidebar import Sidebar
class IP:
    
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
        coal = float(percentdata["coal"])*10
        gas = float(percentdata["gas"])*10
        diesel = float(percentdata["diesel"])*10
        thermal_total = float(percentdata["thermal_total"])*10
        nuclear = float(percentdata["nuclear"])*10
        hydro = float(percentdata["hydro"])*10
        res = float(percentdata["res"])*10
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
        root.geometry("490x500")
        root.tk.call("source", "./oakridge-codefest/forest-dark.tcl")
        ttk.Style().theme_use("forest-dark")

        def prop(n):
            return 360.0 * n / 1000

        frame=ttk.Frame(root)
        frame.grid(row=0, column=1, padx=10)

        myLabel = ttk.Label(frame, text='Pie Chart').grid(row=0, column=1)
        c = tk.Canvas(frame, width=200, height=200)
        c.grid(row=1, column=1)
        sum1=0
        array = self.percentdata()
        c.create_arc((10,10,190,190), fill="#7FFFD4", outline="#000000", start=prop(0), extent = prop(array[0]))
        sum1+=array[0]
        c.create_arc((10,10,190,190), fill="#AAFF00", outline="#000000", start=prop(sum1), extent = prop(array[1]))
        sum1+=array[1]
        c.create_arc((10,10,190,190), fill="#097969", outline="#000000", start=prop(sum1), extent = prop(array[2]))
        sum1+=array[2]
        c.create_arc((10,10,190,190), fill="#355E3B", outline="#000000", start=prop(sum1), extent = prop(array[3]))
        sum1+=array[3]
        c.create_arc((10,10,190,190), fill="#C1E1C1", outline="#000000", start=prop(sum1), extent = prop(array[4]))
        sum1+=array[4]
        c.create_arc((10,10,190,190), fill="#93C572", outline="#000000", start=prop(sum1), extent = prop(array[5]))
        sum1+=array[5]
        c.create_arc((10,10,190,190), fill="#00FF7F", outline="#000000", start=prop(sum1), extent = prop(array[6]))

        myLabel = ttk.Label(frame, text="KEY:",foreground="#FFFFFF").grid(row=2, column=1)
        coal = ttk.Label(frame, text=" COAL ", background="#7FFFD4", foreground="#000000").grid(row=3, column=1)
        gas = ttk.Label(frame, text=" GAS ", background="#AAFF00", foreground="#000000").grid(row=4, column=1)
        diesel = ttk.Label(frame, text=" DIESEL ", background="#097969", foreground="#000000").grid(row=5, column=1)
        thermal_total = ttk.Label(frame, text=" TOTAL THERMAL ", background="#355E3B", foreground="#000000").grid(row=6, column=1)
        nuclear = ttk.Label(frame, text=" NUCLEAR ", background="#C1E1C1", foreground="#000000").grid(row=7, column=1)
        hydro = ttk.Label(frame, text=" HYDRO ", background="#93C572", foreground="#000000").grid(row=8, column=1)
        res = ttk.Label(frame, text=" RENEWABLE ENERGY SOURCES ", background="#00FF7F", foreground="#000000").grid(row=9, column=1)
        empty = ttk.Label(frame, text="").grid(row=10, column=1)

        self.value = 1
        def changeValue():
            self.value -= 1
            if self.value == 0:
                root.destroy()

                self.value = 1
            else:
                pass

        button = ttk.Button(frame, text="GO BACK", command=changeValue, style="Accent.TButton")
        ttk.Style().configure('TButton')
        button.grid(row=11, column=1, ipadx=10, ipady=5)

        root.update()
        self.sidebar = Sidebar(root)
        

        root.mainloop()

