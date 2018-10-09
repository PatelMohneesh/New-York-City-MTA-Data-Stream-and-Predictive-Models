import json
import datetime
import pandas as pd
import numpy as np
from sklearn import linear_model
import tzlocal
from datetime import datetime as dt
import math
import pickle

alerts = pd.read_csv("mtaHistoricalData_2014-11-01-01-01.csv", header=None)
alerts.transpose()
alerts.columns = ["timestamp", "route", "alert", "trip_id", "num_trains"]
del alerts["alert"]
del alerts["trip_id"]
del alerts["num_trains"]


df_route1 = alerts.loc[alerts.route == 1]
df_route2 = alerts.loc[alerts.route == 2]
df_route3 = alerts.loc[alerts.route == 3]
df_route4 = alerts.loc[alerts.route == 4]
df_route5 = alerts.loc[alerts.route == 5]
df_route6 = alerts.loc[alerts.route == 6]

#print(alerts.shape)
#print(df_route1.shape)Learning Shape Abstractions by Assembling Volumetric Primitives,
#print(df_route2.shape)
#print(df_route3.shape)
#print(df_route4.shape)
#print(df_route5.shape)
#print(df_route6.shape)




# convert timestamps to local time
local_timezone = tzlocal.get_localzone()
time_converter = lambda x: dt.fromtimestamp(x, local_timezone)
#alerts["timestamp"] = alerts["timestamp"].apply(time_converter)
alerts["local_time"] = alerts["timestamp"].apply(time_converter)
# modify times
#modify_time = lambda x:
#alerts.drop(alerts.index[:-1])
#df = df[df.trip_id != '0']
#routes = alerts["route"].unique()
#startTime = alerts["local_time"][0]
#endTime   = alerts["local_time"][len(alerts)-1]
#alerts.sort(columns=["route"], inplace=True)
#print(alerts["timestamp"])
#print(alerts.iloc[0])
#print(alerts.iloc[-1])



df_route1["local_time"] = df_route1["timestamp"].apply(time_converter)
df_route2["local_time"] = df_route2["timestamp"].apply(time_converter)
df_route3["local_time"] = df_route3["timestamp"].apply(time_converter)
df_route4["local_time"] = df_route4["timestamp"].apply(time_converter)
df_route5["local_time"] = df_route5["timestamp"].apply(time_converter)
df_route6["local_time"] = df_route6["timestamp"].apply(time_converter)


#for index, row in df_route1.iterrows():
#    print(index)
#    print(row)

#for row in df_route1.iterrows():
#    tmp = row[1]
#    timestamp = tmp[0]
#    route = tmp[1]
#    local_time = tmp[2]
#    print(tmp)

local_times = np.asarray(df_route1["local_time"])
timeBins = np.zeros(len(local_times))
timeIndex = 1




# Bin data into hourly time bins
res = []
binstart = pd.to_datetime(local_times[0])
binstart = binstart.replace(minute = 0, second = 0)
binend   = binstart
hour = binend.hour
if (hour == 23):
    binend = binend.replace(day=binend.day+1, hour = 0)
else:
    binend = binend.replace(hour = hour + 1)
delta = binend - binstart
res.append([binstart, []])

# iterate through data items
for ind, d in enumerate(local_times):
    d_ts = pd.to_datetime(d)
    # if the data item belongs to this bin, append it into the bin
    if d_ts < binstart + delta:
        res[-1][1].append(d_ts)
        timeBins[ind] = timeIndex
        continue

    # otherwise, create new empty bins until this date fits into a bin
    binstart += delta
    while d_ts > binstart + delta:
        timeIndex = timeIndex + 1
        res.append([binstart, []])
        binstart += delta

    timeIndex = timeIndex + 1
    # create a bin with the data
    timeBins[ind] = timeIndex
    res.append([binstart, [d_ts]])



df_route1["timebin"] = timeBins
time_converter2 = lambda x: (pd.to_datetime(x)).replace(minute = 0, second = 0)
df_route1["datetime"] = df_route1["local_time"].apply(time_converter2)
#print(alerts["timestamp"])



start_date = datetime.date(2014, 11, 1)
end_date   = datetime.date(2015, 11, 1)
weather_clean = []
this_date = start_date

while this_date <= end_date:
    name = this_date.strftime("%Y%m%d")
    full_name = "untitled/NYC_" + name + ".json"
    weather = json.loads(open(full_name).read())

    day   = str(this_date.day)
    year  = str(this_date.year)
    month = str(this_date.month)
    for i in range(0, len(weather)):
        weather_dict = {}
        hour = str(i)
        minutes = str("0")
        time_str = year + "-" + month + "-" + day + "-" + hour + "-" + minutes
        time_obj = datetime.datetime.strptime(time_str, "%Y-%m-%d-%H-%M")
        weather_dict["date"] = time_obj
        raining = int(weather[i]["rain"])
        snowing = int(weather[i]["snow"])
        weather_dict["rain"] = raining
        weather_dict["snow"] = snowing
        weather_clean.append(weather_dict)
    this_date += datetime.timedelta(days=1)



dateTimes = np.asarray(df_route1["datetime"])
dateTimes1 = dateTimes
startTime = pd.to_datetime(dateTimes[0])
endTime   = pd.to_datetime(dateTimes[-1])
timeDiff = endTime-startTime
totalHours = 24*timeDiff.days + timeDiff._h
dateTimes = []
dateTimes.append(startTime)
for i in range(1,totalHours):
    startTime = startTime + delta
    dateTimes.append(startTime)




datetime_df = pd.DataFrame(dateTimes)
datetime_df.columns = ["datetime"]
print(datetime_df.iloc[0:1])

#time_converter3 = lambda x: Timestamp(np.datetime64(x))
#datetime_df["datetime"] = datetime_df["datetime"].apply(time_converter3)


unique_times_df = df_route1.drop_duplicates(["datetime"], keep="last")
dateTimes2 = np.asarray(unique_times_df["datetime"])
#print(unique_times_df.iloc[0:1])


#new_time_converter = lambda x : datetime.datetime.utcfromtimestamp(x.tolist()/1e9)
#datetime_df["datetime"] = datetime_df["datetime"].apply(new_time_converter)



#unique_times_df["datetime"] = unique_times_df["datetime"].apply(time_converter3)

#new_df = datetime_df.merge(unique_times_df, left_on="datetime", right_on="datetime")



datetime_unique_df = pd.DataFrame(dateTimes2)
datetime_unique_df.columns = ["datetime"]
datetime_unique_df["route"] = 1

# merge datetimes
df_all = pd.merge(datetime_df, datetime_unique_df, how="left", left_on="datetime", right_on="datetime")
df_all.fillna(0, inplace=True)



weather_df = pd.DataFrame(weather_clean)
weather_np = np.asarray(weather_df["date"])
weather_df["datetime"] = weather_np
del weather_df["date"]

df_final = pd.merge(df_all, weather_df, left_on="datetime", right_on="datetime")

#new_time_converter = lambda x : datetime.datetime.utcfromtimestamp(x.tolist()/1e9)
get_hours = lambda x : x.hour
df_final["hour"] = df_final["datetime"].apply(get_hours)
df_final["weekday"] = df_final["datetime"].dt.weekday

data_y = df_final["route"]
data_x = df_final.copy()

del data_x["route"]
datetimes = data_x["datetime"]
del data_x["datetime"]




datetimes.to_pickle("datetimes2.pkl")

data_y.to_pickle("data_y2.pkl")
data_x.to_pickle("data_x2.pkl")


print("hello")



