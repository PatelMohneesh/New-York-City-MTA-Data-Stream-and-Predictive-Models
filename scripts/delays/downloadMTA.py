import os
from pprint import pprint
from google.protobuf import text_format
import google.protobuf
import csv
import ssl
import gtfs_realtime_pb2 as gtfs_rt
import urllib.request
from datetime import datetime
from datetime import timedelta
#01, 06, 11, 16, 21, 26, 31, 36, 41, 46, 51, and 56

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

delta = timedelta(minutes = 30)
startDate = datetime(2015, 9, 30, 11, 1)
finalDate = datetime(2015, 11, 1, 1, 1)

forbiddenTimes = []

while startDate < finalDate:
    year_str   = str(startDate.year)
    month_str  = str(startDate.month).zfill(2)
    day_str    = str(startDate.day).zfill(2)
    hour_str   = str(startDate.hour).zfill(2)
    minute_str = str(startDate.minute).zfill(2)
    url = "https://datamine-history.s3.amazonaws.com/gtfs-" + year_str + "-" + month_str + "-" + day_str + "-" + hour_str + "-" + minute_str
    file_name = "gtfs_data"


    try:
        with urllib.request.urlopen(url, context=ctx) as u, open(file_name, "wb") as f:
            f.write(u.read())
    except urllib.error.URLError as e:
        ResponseData = e.read().decode("utf8", "ignore")
        forbiddenTimes.append(startDate)
        print("Error: " + year_str + "-" + month_str + "-" + day_str + "-" + hour_str + "-" + minute_str)
        startDate = startDate + delta
        continue

    f = open("gtfs_data", "rb")
    raw_str = f.read()
    msg = gtfs_rt.FeedMessage()
    try:
        msg.ParseFromString(raw_str)
    except:
        forbiddenTimes.append(startDate)
        print("Error: " + year_str + "-" + month_str + "-" + day_str + "-" + hour_str + "-" + minute_str)
        startDate = startDate + delta
        continue


    with open("mtaHistoricalData_2014-11-01-01-01.csv", "a") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=",")


        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        count5 = 0
        count6 = 0
        alert = False
        for entity in msg.entity:
            timestamp = msg.header.timestamp
            if entity.HasField("trip_update"):
                if entity.trip_update.trip.route_id == '1':
                    count1 += 1
                if entity.trip_update.trip.route_id == '2':
                    count2 += 1
                if entity.trip_update.trip.route_id == '3':
                    count3 += 1
                if entity.trip_update.trip.route_id == '4':
                    count4 += 1
                if entity.trip_update.trip.route_id == '5':
                    count5 += 1
                if entity.trip_update.trip.route_id == '6':
                    count6 += 1
            if entity.HasField("alert"):
                alert = True
                try:
                    for trip in entity.alert.informed_entity:
                        if trip.trip.route_id == "1":
                            trip_id = trip.trip.trip_id
                            spamwriter.writerow([timestamp, "1", "alert", trip_id, count1])
                        if trip.trip.route_id == '2':
                            trip_id = trip.trip.trip_id
                            spamwriter.writerow([timestamp, "2", "alert", trip_id, count2])
                        if trip.trip.route_id == '3':
                            trip_id = trip.trip.trip_id
                            spamwriter.writerow([timestamp, "3", "alert", trip_id, count3])
                        if trip.trip.route_id == '4':
                            trip_id = trip.trip.trip_id
                            spamwriter.writerow([timestamp, "4", "alert", trip_id, count4])
                        if trip.trip.route_id == '5':
                            trip_id = trip.trip.trip_id
                            spamwriter.writerow([timestamp, "5", "alert", trip_id, count5])
                        if trip.trip.route_id == '6':
                            trip_id = trip.trip.trip_id
                            spamwriter.writerow([timestamp, "6", "alert", trip_id, count6])
                except:
                    pass


    print(year_str + "-" + month_str + "-" + day_str + "-" + hour_str + "-" + minute_str)
    startDate  = startDate + delta



print("hello")