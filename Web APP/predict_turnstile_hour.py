#function call: pred()
#inputs: hour: int from [0-23]
#outputs: 
#Option 1: Creates a text file in the same folder 'turnstile_pred.txt'
#		   Each line in text file: station_name , scale (range [0,5]), actual_value 
#Option2: Returns a list of length 4(will increase when functionality added for more stations)
#		  Each row in list: [station_name (str) , scale (int, range [0,5]), actual_value (int) ]

flag_api=False

from sklearn.externals import joblib
import datetime
import numpy as np
from weatherRealTime3 import getCurrentWeather

def pred(hr):
    file = open('./turnstile_pred.txt','w')   
    stations=['14st','34st','42st','59st', '72st', '116st']
    results=[]
    #prepare input feature
    
    if flag_api==False:
        rain=np.asarray([0])
        snow=np.asarray([0])
        tempi=np.asarray([45])
    else:
        #get weather now
        weather=getCurrentWeather()
        rain=np.asarray([weather['rain']])
        snow=np.asarray([weather['snow']])
        tempi=np.asarray([weather['tempi']])
    
    curr_time=datetime.datetime.now()
    curr_hour=hr#curr_time.hour 
    curr_day=curr_time.weekday()
    curr_month=curr_time.month

    #create vector
    hour=np.zeros((24))
    hour[curr_hour]=1
    day=np.zeros((7))
    day[curr_day]=1
    month=np.zeros((12))
    month[curr_month]=1
    vec=np.concatenate((hour,day,month,rain,snow,tempi))

    for name in stations:
        #load saved model and params
        model = joblib.load('./pickles/'+name+'_model.pkl') 
        params = joblib.load('./pickles/'+name+'_params.pkl') 

        pred=model.predict(vec.reshape(1,-1))
        scale=np.round(pred)[0]
        value=(((pred*params[1])/params[2])+params[0])[0]
        results.append([name,int(scale),int(value)])
    

    c14_lat = 40.737826
    c14_lon = -74.000201
    c34_lat = 40.750373
    c34_lon = -73.993391
    c42_lat = 40.75529
    c42_lon = -73.987495
    c59_lat = 40.762526
    c59_lon = -73.967967
    c72_lat = 40.778453
    c72_lon = -73.98197
    c116_lat = 40.807722
    c116_lon = -73.96411
    
    
    results[0].append(c14_lat)
    results[0].append(c14_lon)
    
    results[1].append(c34_lat)
    results[1].append(c34_lon)
    
    results[2].append(c42_lat)
    results[2].append(c42_lon)
    
    results[3].append(c59_lat)
    results[3].append(c59_lon)
    
    results[4].append(c72_lat)
    results[4].append(c72_lon)

    results[5].append(c116_lat)
    results[5].append(c116_lon)
    
    return( results) #Option2: comment if don't want this option 
    