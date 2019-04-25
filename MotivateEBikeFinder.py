#Jason Chan
#Motivate E-Bike Finder

import requests
import time
from geopy.distance import geodesic
import datetime
import geocoder


print("\nWelcome Motivate Bike-Share E-Bike Finder\n")


nystationJson = requests.get('https://gbfs.citibikenyc.com/gbfs/es/station_information.json').json()
nystationStatus = requests.get('https://gbfs.citibikenyc.com/gbfs/es/station_status.json').json()

sfStationStatus = requests.get('https://gbfs.fordgobike.com/gbfs/en/station_status.json').json()
sfStationJson = requests.get('https://gbfs.fordgobike.com/gbfs/es/station_information.json').json()


dcStationStatus = requests.get('https://gbfs.capitalbikeshare.com/gbfs/en/station_status.json').json()
dcStationJson = requests.get('https://gbfs.capitalbikeshare.com/gbfs/en/station_information.json').json()


print("Which System are You Interested In?")
print(" NYC CitiBike: Press 0")
print(" SF FordGoBike: Press 1")
print(" DC Capital Bikeshare: Press 2")
print()
bikeSystem = int(input("Please input number: "))

stationJson = None
stationStatus = None

if bikeSystem == 0:
    print('Citi Selected')
    stationJson = nystationJson
    stationStatus = nystationStatus
elif bikeSystem == 1:
    print("Ford Selected")
    stationJson = sfStationJson
    stationStatus = sfStationStatus
else:
    print("DC Selected")
    stationJson = dcStationJson
    stationStatus = dcStationStatus

print()

stationDict = {}

#but bike stations and location into local dict
with open('bikeShareData.csv', 'w', newline='') as f:
    fieldnames = ['id', 'name', 'lat', 'long']

    for each in stationJson['data']['stations']:
        #print(each['name'])
        id = int(each['station_id'])
        stationDict[id] = [each['name'], each['lat'], each['lon']]

#print(stationDict)


loc = input("Please enter your address or zipcode: ")

g = geocoder.arcgis(loc)  #coodinates of your address
print("Your location: \n", g.latlng)


while 1:
    coords_1 = g.latlng

    ebikeDict = {}

    sum = 0
    timeNow = datetime.datetime.now()
    print("\nLast checked: {:%m/%d/%Y  %I:%M %p}\n".format(timeNow))

    for each in stationStatus['data']['stations']:
        id = int(each['station_id'])
        ebikeNum = each['num_ebikes_available']
        #print(stationDict[id][0])

        #save all bike stations with ebikes into ebikeDict
        if ebikeNum > 0:
            key = "{} bike(s) at {}.".format(ebikeNum, stationDict[id][0])
            coords_2 = (stationDict[id][1], stationDict[id][2])
            sum += ebikeNum
            value = geodesic(coords_1, coords_2).miles
            value = str(round(value, 2))
            ebikeDict[key] = value

    #sort ebikeDict
    sorted_d = dict(sorted(ebikeDict.items(), key=lambda x: x[1]))
    for k, v in sorted_d.items():
        print(k, "   Distance from you: ", v, " miles")


    print("Total ebikes available: {}".format(sum))
    print("--------------------------------------------------\n")
    print("Refresh in 60 seconds")
    time.sleep(60)  #wait 60 seconds before checking again.