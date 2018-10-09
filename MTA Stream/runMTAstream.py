from gtfs import getTrainScheduleUpdated as sc
from datetime import datetime as dt
import time
from gtfs import stops

from pprint import pprint

vehicleStopStatus={
    '0':'comming at',
    '1':'stopped at',
    '2':'in transit to',
    None:None}

print(' ')
print('Available stations:')

stations = ["14 St","34 St - Penn Station","Times Sq - 42 St","59 St - Columbus Circle", "72 St", "116 St - Columbia University"]

for i in range(1,len(stations)+1):
    print("%s: %s"%(i,stations[i-1]))

event = {}
print(' ')
start = -1
while start > 5 or start < 0:
    start = int(raw_input("Please enter a valid starting station: "))-1
    print(' ')
    
event["start"] = stations[start]

end = -1
while end > 5 or end < 0 or end == start:
    end = int(raw_input("Please enter a valid destination station different from starting station: "))-1
    print(' ')


event["end"] = stations[end]

initial = sc.getTrip(event, 1)
loop=1
while initial==None:
    initial = sc.getTrip(event, 1)
    time.sleep(30)
    
if initial["transfer"] == None:
    print("The fastest route to %s from %s is by taking the %s train."%(event["end"], event["start"], initial["start"]["trip_id"][7]))
    
    event["tripstart"] = initial["start"]["trip_id"]
    event["tripend"] = ""
    
    while loop:
        update = sc.getTripUpdate(event, 1)
        
        while update==None:
            update = sc.getTripUpdate(event, 1)
            time.sleep(30)
        
        print(' ')
        try:
            if time.time()<update["start"]["departureTime"]:
                departure = dt.fromtimestamp(update["start"]["departureTime"]).strftime("%I:%M:%S %p")
                diff = (update["start"]["departureTime"]-time.time())/60
                
                stop_name = stops.get_stop_name(update["start"]["current_stop_id"]) 
                 
                print("Your train will depart at %s, %s minutes from now."%(departure, int(diff)))
                print("Currently it is %s %s"%(vehicleStopStatus[update["start"]["current_status"]], stop_name))
        
            elif time.time()>=update["start"]["departureTime"]:
                arrival = dt.fromtimestamp(update["start"]["arrivalTime"]).strftime("%I:%M:%S %p")
                diff = (update["start"]["arrivalTime"]-time.time())/60
                
                stop_name = stops.get_stop_name(update["start"]["current_stop_id"]) 
                 
                print("Your train has departed and will arrive at your destination at %s, %s minutes from now."%(arrival, int(diff)))
                print("Currently it is %s %s"%(vehicleStopStatus[update["start"]["current_status"]], stop_name))
            
            if time.time()>=update["start"]["arrivalTime"]:
                print("You have reached your destination! Goodbye!")
                loop = 0
                
        except TypeError:
            pass
            
        time.sleep(30)
else:
    print("The fastest route to %s from %s is by taking the %s train and transfering to the %s train."%(event["end"], event["start"], initial["start"]["trip_id"][7],initial["transfer"]["trip_id"][7]))
    
    event["tripstart"] = initial["start"]["trip_id"]
    event["tripend"] = initial["transfer"]["trip_id"]
    
    while loop:
        update = sc.getTripUpdate(event, 1)
        
        while update==None:
            update = sc.getTripUpdate(event, 1)
            time.sleep(30)
            
        print(' ')
        if update["start"]["arrivalTime"] != None:
            if time.time()<update["start"]["departureTime"]:
                departure = dt.fromtimestamp(update["start"]["departureTime"]).strftime("%I:%M:%S %p")
                diff = (update["start"]["departureTime"]-time.time())/60
                
                stop_name = stops.get_stop_name(update["start"]["current_stop_id"]) 
                 
                print("Your train will depart at %s, %s minutes from now."%(departure, int(diff)))
                print("Currently it is %s %s"%(vehicleStopStatus[update["start"]["current_status"]], stop_name))
            
            elif time.time()>=update["start"]["departureTime"]:
                arrival = dt.fromtimestamp(update["start"]["arrivalTime"]).strftime("%I:%M:%S %p")
                diff = (update["start"]["arrivalTime"]-time.time())/60
                
                stop_name = stops.get_stop_name(update["start"]["current_stop_id"]) 
                 
                print("Your train has departed and will arrive at your transfer station at %s, %s minutes from now."%(arrival, int(diff)))
                print("Currently it is %s %s"%(vehicleStopStatus[update["start"]["current_status"]], stop_name))
            
            if time.time()>=update["start"]["arrivalTime"]:
                print("You have reached your transfer station. Please transfer to the %s train."%initial["transfer"]["trip_id"][7])
                print("You transfer train is %s %s"%(vehicleStopStatus[update["transfer"]["current_status"]], stop_name))
            
        else:
            if time.time()<update["transfer"]["departureTime"]:
                departure = dt.fromtimestamp(update["transfer"]["departureTime"]).strftime("%I:%M:%S %p")
                diff = (update["transfer"]["departureTime"]-time.time())/60
                
                stop_name = stops.get_stop_name(update["transfer"]["current_stop_id"]) 
                 
                print("Your train will depart at %s, %s minutes from now."%(departure, int(diff)))
                print("Currently it is %s %s"%(vehicleStopStatus[update["transfer"]["current_status"]], stop_name))
            
            elif time.time()>=update["transfer"]["departureTime"]:
                arrival = dt.fromtimestamp(update["transfer"]["arrivalTime"]).strftime("%I:%M:%S %p")
                diff = (update["transfer"]["arrivalTime"]-time.time())/60
                
                stop_name = stops.get_stop_name(update["transfer"]["current_stop_id"]) 
                 
                print("Your train has departed and will arrive at your transfer station at %s, %s minutes from now."%(arrival, int(diff)))
                print("Currently it's %s %s"%(vehicleStopStatus[update["transfer"]["current_status"]], stop_name))
            
            if time.time()>=update["transfer"]["arrivalTime"]:
                print("You have reached your destination! Goodbye!")
                loop = 0
        
        time.sleep(30)
