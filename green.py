# importing the requests library
import requests
class IP:

    def __init__(self):

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
        
        print(percentdata)
        #return percentdata

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

IP()  

