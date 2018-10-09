from google.transit import gtfs_realtime_pb2
import google
import tripUpdated as trip
import time
import stops
# import numpy as np
import json
# import sys
from pprint import pprint
from datetime import datetime as dt
import requests
APIkey = ""


def getlist(start,end):

    if start=="14 St" and end=="116 St - Columbia University":

        single = [stops.line1Nbound["14 St"],stops.line1Nbound["116 St - Columbia University"]]
        transfer = [stops.line1Nbound["96 St"],stops.line1Nbound["116 St - Columbia University"]]
        start = [stops.line1Nbound["14 St"],stops.line1Nbound["96 St"]]
        routes = ["1","2", "3"]
        line = stops.line1
        
    elif start=="116 St - Columbia University" and end=="14 St":
        single = [stops.line1Sbound["116 St - Columbia University"],stops.line1Sbound["14 St"]]
        transfer = [stops.line1Sbound["96 St"],stops.line1Sbound["14 St"]]
        start = [stops.line1Sbound["116 St - Columbia University"],stops.line1Sbound["96 St"]]
        routes = ["1","2","3"]
        line = stops.line1

    elif start=="14 St" and end=="34 St - Penn Station":
        single = [stops.line1Nbound["14 St"],stops.line1Nbound["34 St - Penn Station"]]
        # transfer = [stops.line1Nbound["14 St"],stops.line1Nbound["34 St - Penn Station"]]
        transfer = None
        start = [stops.line1Nbound["14 St"],stops.line1Nbound["34 St - Penn Station"]]
        routes = ["1","2", "3"]
        line = stops.line1
        
    elif start=="34 St - Penn Station" and end=="14 St":
        single = [stops.line1Sbound["34 St - Penn Station"],stops.line1Sbound["14 St"]]
        # transfer = [stops.line1Sbound["96 St"],stops.line1Sbound["14 St"]]
        transfer = None
        start = [stops.line1Sbound["34 St - Penn Station"],stops.line1Sbound["14 St"]]
        routes = ["1","2","3"]
        line = stops.line1
    
    elif start=="14 St" and end=="Times Sq - 42 St":
        single = [stops.line1Nbound["14 St"],stops.line1Nbound["Times Sq - 42 St"]]
        # transfer = [stops.line1Nbound["14 St"],stops.line1Nbound["34 St - Penn Station"]]
        transfer = None
        start = [stops.line1Nbound["14 St"],stops.line1Nbound["Times Sq - 42 St"]]
        routes = ["1","2", "3"]
        line = stops.line1
        
    elif start=="Times Sq - 42 St" and end=="14 St":
        single = [stops.line1Sbound["Times Sq - 42 St"],stops.line1Sbound["14 St"]]
        # transfer = [stops.line1Sbound["96 St"],stops.line1Sbound["14 St"]]
        transfer = None
        start = [stops.line1Sbound["Times Sq - 42 St"],stops.line1Sbound["14 St"]]
        routes = ["1","2","3"]
        line = stops.line1
    
    elif start=="14 St" and end=="59 St - Columbus Circle":
        single = [stops.line1Nbound["14 St"],stops.line1Nbound["59 St - Columbus Circle"]]
        transfer = [stops.line1Nbound["Times Sq - 42 St"],stops.line1Nbound["59 St - Columbus Circle"]]
        # transfer = None
        start = [stops.line1Nbound["14 St"],stops.line1Nbound["Times Sq - 42 St"]]
        routes = ["1","2", "3"]
        line = stops.line1
        
    elif start=="59 St - Columbus Circle" and end=="14 St":
        single = [stops.line1Sbound["59 St - Columbus Circle"],stops.line1Sbound["14 St"]]
        transfer = [stops.line1Sbound["Times Sq - 42 St"],stops.line1Sbound["14 St"]]
        # transfer = None
        start = [stops.line1Sbound["59 St - Columbus Circle"],stops.line1Sbound["Times Sq - 42 St"]]
        routes = ["1","2","3"]
        line = stops.line1
    
    elif start=="14 St" and end=="72 St":
        single = [stops.line1Nbound["14 St"],stops.line1Nbound["72 St"]]
        # transfer = [stops.line1Nbound["Times Sq - 42 St"],stops.line1Nbound["72 St"]]
        transfer = None
        start = [stops.line1Nbound["14 St"],stops.line1Nbound["72 St"]]
        routes = ["1","2", "3"]
        line = stops.line1
        
    elif start=="72 St" and end=="14 St":
        single = [stops.line1Sbound["72 St"],stops.line1Sbound["14 St"]]
        # transfer = [stops.line1Sbound["72 St"],stops.line1Sbound["14 St"]]
        transfer = None
        start = [stops.line1Sbound["72 St"],stops.line1Sbound["14 St"]]
        routes = ["1","2","3"]
        line = stops.line1
    #-------------
    elif start=="34 St - Penn Station" and end=="116 St - Columbia University":

        single = [stops.line1Nbound["34 St - Penn Station"],stops.line1Nbound["116 St - Columbia University"]]
        transfer = [stops.line1Nbound["96 St"],stops.line1Nbound["116 St - Columbia University"]]
        start = [stops.line1Nbound["34 St - Penn Station"],stops.line1Nbound["96 St"]]
        routes = ["1","2", "3"]
        line = stops.line1
        
    elif start=="116 St - Columbia University" and end=="34 St - Penn Station":
        single = [stops.line1Sbound["116 St - Columbia University"],stops.line1Sbound["34 St - Penn Station"]]
        transfer = [stops.line1Sbound["96 St"],stops.line1Sbound["34 St - Penn Station"]]
        start = [stops.line1Sbound["116 St - Columbia University"],stops.line1Sbound["96 St"]]
        routes = ["1","2","3"]
        line = stops.line1
    
    elif start=="34 St - Penn Station" and end=="Times Sq - 42 St":
        single = [stops.line1Nbound["34 St - Penn Station"],stops.line1Nbound["Times Sq - 42 St"]]
        # transfer = [stops.line1Nbound["14 St"],stops.line1Nbound["34 St - Penn Station"]]
        transfer = None
        start = [stops.line1Nbound["34 St - Penn Station"],stops.line1Nbound["Times Sq - 42 St"]]
        routes = ["1","2", "3"]
        line = stops.line1
        
    elif start=="Times Sq - 42 St" and end=="34 St - Penn Station":
        single = [stops.line1Sbound["Times Sq - 42 St"],stops.line1Sbound["34 St - Penn Station"]]
        # transfer = [stops.line1Sbound["96 St"],stops.line1Sbound["14 St"]]
        transfer = None
        start = [stops.line1Sbound["Times Sq - 42 St"],stops.line1Sbound["34 St - Penn Station"]]
        routes = ["1","2","3"]
        line = stops.line1
    
    elif start=="34 St - Penn Station" and end=="59 St - Columbus Circle":
        single = [stops.line1Nbound["34 St - Penn Station"],stops.line1Nbound["59 St - Columbus Circle"]]
        # transfer = [stops.line1Nbound["Times Sq - 42 St"],stops.line1Nbound["59 St - Columbus Circle"]]
        transfer = None
        start = [stops.line1Nbound["34 St - Penn Station"],stops.line1Nbound["59 St - Columbus Circle"]]
        routes = ["1","2", "3"]
        line = stops.line1
        
    elif start=="59 St - Columbus Circle" and end=="34 St - Penn Station":
        single = [stops.line1Sbound["59 St - Columbus Circle"],stops.line1Sbound["34 St - Penn Station"]]
        # transfer = [stops.line1Sbound["Times Sq - 42 St"],stops.line1Sbound["14 St"]]
        transfer = None
        start = [stops.line1Sbound["59 St - Columbus Circle"],stops.line1Sbound["34 St - Penn Station"]]
        routes = ["1","2","3"]
        line = stops.line1
    
    elif start=="34 St - Penn Station" and end=="72 St":
        single = [stops.line1Nbound["34 St - Penn Station"],stops.line1Nbound["72 St"]]
        # transfer = [stops.line1Nbound["Times Sq - 42 St"],stops.line1Nbound["72 St"]]
        transfer = None
        start = [stops.line1Nbound["34 St - Penn Station"],stops.line1Nbound["72 St"]]
        routes = ["1","2", "3"]
        line = stops.line1
        
    elif start=="72 St" and end=="34 St - Penn Station":
        single = [stops.line1Sbound["72 St"],stops.line1Sbound["34 St - Penn Station"]]
        # transfer = [stops.line1Sbound["72 St"],stops.line1Sbound["14 St"]]
        transfer = None
        start = [stops.line1Sbound["72 St"],stops.line1Sbound["34 St - Penn Station"]]
        routes = ["1","2","3"]
        line = stops.line1
    #-------------
    elif start=="Times Sq - 42 St" and end=="116 St - Columbia University":

        single = [stops.line1Nbound["Times Sq - 42 St"],stops.line1Nbound["116 St - Columbia University"]]
        transfer = [stops.line1Nbound["96 St"],stops.line1Nbound["116 St - Columbia University"]]
        start = [stops.line1Nbound["Times Sq - 42 St"],stops.line1Nbound["96 St"]]
        routes = ["1","2", "3"]
        line = stops.line1
        
    elif start=="116 St - Columbia University" and end=="Times Sq - 42 St":
        single = [stops.line1Sbound["116 St - Columbia University"],stops.line1Sbound["Times Sq - 42 St"]]
        transfer = [stops.line1Sbound["96 St"],stops.line1Sbound["Times Sq - 42 St"]]
        start = [stops.line1Sbound["116 St - Columbia University"],stops.line1Sbound["96 St"]]
        routes = ["1","2","3"]
        line = stops.line1
    
    elif start=="Times Sq - 42 St" and end=="59 St - Columbus Circle":
        single = [stops.line1Nbound["Times Sq - 42 St"],stops.line1Nbound["59 St - Columbus Circle"]]
        # transfer = [stops.line1Nbound["Times Sq - 42 St"],stops.line1Nbound["59 St - Columbus Circle"]]
        transfer = None
        start = [stops.line1Nbound["Times Sq - 42 St"],stops.line1Nbound["59 St - Columbus Circle"]]
        routes = ["1","2", "3"]
        line = stops.line1
        
    elif start=="59 St - Columbus Circle" and end=="Times Sq - 42 St":
        single = [stops.line1Sbound["59 St - Columbus Circle"],stops.line1Sbound["Times Sq - 42 St"]]
        # transfer = [stops.line1Sbound["Times Sq - 42 St"],stops.line1Sbound["14 St"]]
        transfer = None
        start = [stops.line1Sbound["59 St - Columbus Circle"],stops.line1Sbound["Times Sq - 42 St"]]
        routes = ["1","2","3"]
        line = stops.line1
    
    elif start=="Times Sq - 42 St" and end=="72 St":
        single = [stops.line1Nbound["Times Sq - 42 St"],stops.line1Nbound["72 St"]]
        # transfer = [stops.line1Nbound["Times Sq - 42 St"],stops.line1Nbound["72 St"]]
        transfer = None
        start = [stops.line1Nbound["Times Sq - 42 St"],stops.line1Nbound["72 St"]]
        routes = ["1","2", "3"]
        line = stops.line1
        
    elif start=="72 St" and end=="Times Sq - 42 St":
        single = [stops.line1Sbound["72 St"],stops.line1Sbound["Times Sq - 42 St"]]
        # transfer = [stops.line1Sbound["72 St"],stops.line1Sbound["14 St"]]
        transfer = None
        start = [stops.line1Sbound["72 St"],stops.line1Sbound["Times Sq - 42 St"]]
        routes = ["1","2","3"]
        line = stops.line1
    #-------------
 
    elif start=="59 St - Columbus Circle" and end=="116 St - Columbia University":

        single = [stops.line1Nbound["59 St - Columbus Circle"],stops.line1Nbound["116 St - Columbia University"]]
        # transfer = [stops.line1Nbound["96 St"],stops.line1Nbound["116 St - Columbia University"]]
        transfer=None
        start = [stops.line1Nbound["59 St - Columbus Circle"],stops.line1Nbound["116 St - Columbia University"]]
        routes = ["1","2", "3"]
        line = stops.line1
        
    elif start=="116 St - Columbia University" and end=="59 St - Columbus Circle":
        single = [stops.line1Sbound["116 St - Columbia University"],stops.line1Sbound["59 St - Columbus Circle"]]
        # transfer = [stops.line1Sbound["96 St"],stops.line1Sbound["Times Sq - 42 St"]]
        transfer = None
        start = [stops.line1Sbound["116 St - Columbia University"],stops.line1Sbound["59 St - Columbus Circle"]]
        routes = ["1","2","3"]
        line = stops.line1
    
    elif start=="59 St - Columbus Circle" and end=="72 St":
        single = [stops.line1Nbound["59 St - Columbus Circle"],stops.line1Nbound["72 St"]]
        # transfer = [stops.line1Nbound["Times Sq - 42 St"],stops.line1Nbound["72 St"]]
        transfer = None
        start = [stops.line1Nbound["59 St - Columbus Circle"],stops.line1Nbound["72 St"]]
        routes = ["1","2", "3"]
        line = stops.line1
        
    elif start=="72 St" and end=="59 St - Columbus Circle":
        single = [stops.line1Sbound["72 St"],stops.line1Sbound["59 St - Columbus Circle"]]
        # transfer = [stops.line1Sbound["72 St"],stops.line1Sbound["14 St"]]
        transfer = None
        start = [stops.line1Sbound["72 St"],stops.line1Sbound["59 St - Columbus Circle"]]
        routes = ["1","2","3"]
        line = stops.line1
    
    
    #-------------
    elif start=="72 St" and end=="116 St - Columbia University":

        single = [stops.line1Nbound["72 St"],stops.line1Nbound["116 St - Columbia University"]]
        transfer = [stops.line1Nbound["96 St"],stops.line1Nbound["116 St - Columbia University"]]
        start = [stops.line1Nbound["72 St"],stops.line1Nbound["96 St"]]
        routes = ["1","2", "3"]
        line = stops.line1
        
    elif start=="116 St - Columbia University" and end=="72 St":
        single = [stops.line1Sbound["116 St - Columbia University"],stops.line1Sbound["72 St"]]
        transfer = [stops.line1Sbound["96 St"],stops.line1Sbound["72 St"]]
        start = [stops.line1Sbound["116 St - Columbia University"],stops.line1Sbound["96 St"]]
        routes = ["1","2","3"]
        line = stops.line1
    
    
    return(single, transfer, start, routes, line)
    
def getTrip(event, context):

    try:
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get("http://datamine.mta.info/mta_esi.php?key=%s&feed_id=1"%APIkey)
        
        feed.ParseFromString(response.content)


        (single, transfer, start, routes, line)=getlist(event["start"],event["end"])
                
            

        fastestTrip = trip.getFastestTrip(start,routes, feed)        
        
        if transfer == None:
            fastestTransfer = fastestTrip
        else:
            timeDiff = fastestTrip["arrivalTime"]-int(time.time())
            fastestTransfer = trip.getFastestTransfer(transfer,routes,timeDiff,feed)


        fastestTripSingle = trip.getFastestTrip(single,routes,feed)

        # print fastestTripSingle
            
        if fastestTransfer["arrivalTime"] < fastestTripSingle["arrivalTime"]:

            data = {}
            data["start"]=fastestTrip
            if transfer == None:
                data["transfer"]=None
            else:
                data["transfer"]=fastestTransfer

            json_data = json.dumps(data)

        else:
            
            data = {}
            data["start"]=fastestTripSingle
            data["transfer"]=None
            
            # json_data = json.dumps(data)
            
        return(data)
    except google.protobuf.message.DecodeError:
        print("Stream Error")
        return None
        

    
def getTripUpdate(event, context):
    try:
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get("http://datamine.mta.info/mta_esi.php?key=%s&feed_id=1"%APIkey)
            
        feed.ParseFromString(response.content)
        
        (single, transfer, start, routes, line)=getlist(event["start"],event["end"])
        
        
        
        update = trip.tripUpdate(event["tripstart"], start,feed)
        
        
        udata = {}
        udata["start"]={}
            
        udata["start"]["trip_id"]=update[0]
        
        udata["start"]["departureTime"]=update[1]
        
        udata["start"]["arrivalTime"]=update[2]
        
        udata["start"]["current_stop_id"]=update[3]
        udata["start"]["current_status"]=update[5]
        udata["start"]["train_status"]=update[6]
        
        udata["start"]["time"]=update[7]
        
        
        if event["tripend"]!="":
        
            transfer = trip.tripUpdate(event["tripend"], transfer,feed)
            
            
            udata["transfer"]={}
            udata["transfer"]["trip_id"]=transfer[0]
            
            udata["transfer"]["departureTime"]=transfer[1]
            
            udata["transfer"]["arrivalTime"]=transfer[2]
            
            udata["transfer"]["current_stop_id"]=transfer[3]
            udata["transfer"]["current_status"]=transfer[5]
            udata["transfer"]["train_status"]=transfer[6]
            
            udata["transfer"]["time"]=transfer[7]
        else:
            udata["transfer"]=None
        
        
        
        return(udata)
        
    except google.protobuf.message.DecodeError:
        print("Stream Error")
        return None
            
