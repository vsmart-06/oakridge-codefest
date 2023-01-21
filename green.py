# importing the requests library
import requests

# Python Program to Get IP Address
ip = requests.get('https://api.ipify.org').content.decode('utf8')
IPAddr = format(ip)
#print(IPAddr)

#getting geolocation
URL = f"http://ip-api.com/json/{IPAddr}?fields=country,regionName"
r = requests.get(URL)
geodata = r.json()
#print(geodata)

#find tbe percentage of green fuel
URL= "https://cea.nic.in/api/installed_capacity_statewise.php"
r = requests.get(URL)
data = r.json()
data = data[::-1]
states = [x["state"] for x in data]
index = states.index(geodata["regionName"])
state_data = data[index]
print(state_data)