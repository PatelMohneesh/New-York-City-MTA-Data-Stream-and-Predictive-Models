from google.transit import gtfs_realtime_pb2
import requests
from pprint import pprint
import json
import time
# import numpy as np
import stops
APIkey = ''

# while True:

vehicleStopStatus={
    '0':'comming at',
    '1':'stopped at',
    '2':'in transit to',
    None:None}

def getTripId(stationName,route,wait_time,feed):
    
        
    dictTrip = {}
    departureList = []
    time_now = time.time()
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            for stop_time_update in entity.trip_update.stop_time_update:
                
                if stop_time_update.stop_id == stationName and entity.trip_update.trip.route_id == route:
                    
                    trip_id = entity.trip_update.trip.trip_id
                    departure = int(stop_time_update.departure.time)
                    # print departure
                    # if 30 < (departure - time.time()):
                    departure30min = abs(departure - time_now - wait_time)
                    # print departure30min
                    departureList.append(departure30min)
                    # print(route,departure,departure30min,trip_id)
                    # else:
                        # continue
                    
                    dictTrip[str(departure30min)]=trip_id
                    
    # print departureList
    try:
        departureTime = min(departureList)
        trip_id = str(dictTrip[str(departureTime)])
    except:
        trip_id = None

    return (trip_id)
    

    
def getTransferTripId(stationName,route,wait_time, feed):

    dictTrip = {}
    departureList = []
    time_now = time.time()
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            for stop_time_update in entity.trip_update.stop_time_update:
                # print stop_time_update.stop_id
                if stop_time_update.stop_id == stationName and entity.trip_update.trip.route_id == route:
                
                    trip_id = entity.trip_update.trip.trip_id
                    departure = int(stop_time_update.departure.time)
                    # if 30 < (departure - time.time()):
                    departure30min = departure - time_now - wait_time
                    if departure30min > 0:
                        departureList.append(departure30min)
                        # print(route,departure,departure30min,trip_id)
                    # else:
                        # continue
                    
                        dictTrip[str(departure30min)]=trip_id
                    
    try:
        departureTime = min(departureList)
        trip_id = str(dictTrip[str(departureTime)])
    except:
        trip_id = None

    return (trip_id)
    # return (trip_id,departureTime)
    
def getTripStatus(trip_id,startStationName, endStationName, feed):

    departureTime=None
    arrivalTime=None
    current_stop_sequence=None
    current_status=None
    timestamp = None
    current_stop_id=None
    train_status = None
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            if entity.trip_update.trip.trip_id == trip_id:
                for stop_time_update in entity.trip_update.stop_time_update:
                    if stop_time_update.stop_id == startStationName:
                        departureTime = int(stop_time_update.departure.time)

                    if stop_time_update.stop_id == endStationName:
                        arrivalTime = int(stop_time_update.arrival.time)

            
                
        if entity.HasField('vehicle'):
            if entity.vehicle.trip.trip_id == trip_id:
                current_stop_sequence = int(entity.vehicle.current_stop_sequence)
                current_status = str(entity.vehicle.current_status)
                timestamp = int(entity.vehicle.timestamp)
                current_stop_id = entity.vehicle.stop_id
        
        if entity.HasField('alert'):
			for informed_entity in entity.alert.informed_entity:
				if informed_entity.trip.trip_id == trip_id:
					
					if entity.alert.HasField('header_text'):
						
                        			train_status = entity.alert.header_text.translation[0].text
        
    return(departureTime,arrivalTime,current_stop_id,current_stop_sequence,current_status,train_status,timestamp)   

def getFastestTrip(stationNames,routes, feed):

    start_stop_id = stationNames[0]
    end_stop_id = stationNames[1]
    
    trip_ids = {}
    for route in routes:
        trip_id = getTripId(start_stop_id, route, 120, feed)
        if trip_id != None:
            trip_ids[trip_id] = {}
    # pprint(trip_ids.keys())
    
    arrivalTimes = {}
    for key in trip_ids.keys():
        trip_data = getTripStatus(key, start_stop_id, end_stop_id, feed)
        
        trip_ids[key]['departureTime'] = trip_data[0]
        trip_ids[key]['arrivalTime'] = trip_data[1]
        trip_ids[key]['currentStopId'] = trip_data[2]
        trip_ids[key]['currentStopSequence'] = trip_data[3]
        trip_ids[key]['currentStatus'] = vehicleStopStatus[trip_data[4]]
        trip_ids[key]['train_status'] = trip_data[5]
        trip_ids[key]['vehicleTime'] = trip_data[6]
        trip_ids[key]['trip_id'] = key
        
        
        
            
        if trip_ids[key]['currentStopSequence'] != None:
            
            currentStopName = stops.line1Seq[len(stops.line1Seq)-trip_ids[key]['currentStopSequence']]

        if trip_ids[key]['departureTime'] == None:
            arrivalMinutes = ((trip_ids[key]['arrivalTime'])-int(time.time()))/60
            arrivalTimes[key] = trip_ids[key]['arrivalTime']
            
        else:
            departMinutes = ((trip_ids[key]['departureTime'])-int(time.time()))/60
            try:
                arrivalMinutes = ((trip_ids[key]['arrivalTime'])-int(time.time()))/60
                arrivalTimes[key] = trip_ids[key]['arrivalTime']
            except:
                # print('No arrival information avaialble')
                pass
            
    # pprint(trip_ids)

    tempTimes = []
    for key in arrivalTimes:
        tempTimes.append(arrivalTimes[key])
    leastTime = min(tempTimes)
    for key in arrivalTimes:
        if arrivalTimes[key] == leastTime:
            trip_id_leastTime = key
    return(trip_ids[trip_id_leastTime])
    
    
def getFastestTransfer(stationNames,routes,timeDiff, feed):

    start_stop_id = stationNames[0]
    end_stop_id = stationNames[1]
    
    trip_ids = {}
    for route in routes:
        trip_id = getTransferTripId(start_stop_id, route, timeDiff, feed)
        if trip_id != None:
            trip_ids[trip_id] = {}
    # pprint(trip_ids.keys())
    
    arrivalTimes = {}
    for key in trip_ids.keys():
    
        trip_data = getTripStatus(key, start_stop_id, end_stop_id, feed)
        
        trip_ids[key]['departureTime'] = trip_data[0]
        trip_ids[key]['arrivalTime'] = trip_data[1]
        trip_ids[key]['currentStopId'] = trip_data[2]
        trip_ids[key]['currentStopSequence'] = trip_data[3]
        trip_ids[key]['currentStatus'] = vehicleStopStatus[trip_data[4]]
        trip_ids[key]['train_status'] = trip_data[5]
        trip_ids[key]['vehicleTime'] = trip_data[5]
        trip_ids[key]['trip_id'] = key
        
        
            
        if trip_ids[key]['currentStopSequence'] != None:
            
            currentStopName = stops.line1Seq[len(stops.line1Seq)-trip_ids[key]['currentStopSequence']]

        if trip_ids[key]['departureTime'] == None:
            arrivalMinutes = ((trip_ids[key]['arrivalTime'])-int(time.time()))/60
            arrivalTimes[key] = trip_ids[key]['arrivalTime']
            
        else:
            departMinutes = ((trip_ids[key]['departureTime'])-int(time.time()))/60
            try:
                arrivalMinutes = ((trip_ids[key]['arrivalTime'])-int(time.time()))/60
                arrivalTimes[key] = trip_ids[key]['arrivalTime']
            except:
                
                pass
            
    

    tempTimes = []
    for key in arrivalTimes:
        tempTimes.append(arrivalTimes[key])
    leastTime = min(tempTimes)
    for key in arrivalTimes:
        if arrivalTimes[key] == leastTime:
            trip_id_leastTime = key
    return(trip_ids[trip_id_leastTime])
    
    
    
def tripUpdate(trip_id,stationNames,feed):   
    
    startStationName = stationNames[0]
    endStationName = stationNames[1]
    
    departureTime=None
    arrivalTime=None
    current_stop_sequence=None
    current_status=None
    timestamp = None
    current_stop_id=None
    train_status = None
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            if entity.trip_update.trip.trip_id == trip_id:
                for stop_time_update in entity.trip_update.stop_time_update:
                    if stop_time_update.stop_id == startStationName:
                        departureTime = int(stop_time_update.departure.time)
                    
                    if stop_time_update.stop_id == endStationName:
                        arrivalTime = int(stop_time_update.arrival.time)

                
        if entity.HasField('vehicle'):
            if entity.vehicle.trip.trip_id == trip_id:
                current_stop_sequence = int(entity.vehicle.current_stop_sequence)
                current_status = str(entity.vehicle.current_status)
                timestamp = int(entity.vehicle.timestamp)
                current_stop_id = entity.vehicle.stop_id
        
        if entity.HasField('alert'):
			for informed_entity in entity.alert.informed_entity:
				if informed_entity.trip.trip_id == trip_id:
					if entity.alert.HasField('header_text'):
                        			train_status = entity.alert.header_text.translation[0].text

    return(trip_id,departureTime,arrivalTime,current_stop_id,current_stop_sequence,current_status,train_status,timestamp)

