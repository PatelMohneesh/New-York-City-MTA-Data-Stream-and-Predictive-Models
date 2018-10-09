#function call: pred()
#inputs: hour: int from [0-23]
#outputs: 
#Option 1: Creates a text file in the same folder 'turnstile_pred.txt'
#		   Each line in text file: station_name , scale (range [0,5]), actual_value 
#Option2: Returns a list of length 4(will increase when functionality added for more stations)
#		  Each row in list: [station_name (str) , scale (int, range [0,5]), actual_value (int) ]

from sklearn.externals import joblib
import datetime
import numpy as np
from weatherRealTime3 import getCurrentWeather

def pred(hr):

	file = open('./turnstile_pred.txt','w')   

	stations=['14st','34st','42st','59st', '72st', '116st']
	results=[]
	#prepare input feature
	for name in stations:
	    #load saved model and params
	    model = joblib.load('./pickles/'+name+'_model.pkl') 
	    params = joblib.load('./pickles/'+name+'_params.pkl') 
	        
	    #get time now
	    curr_time=datetime.datetime.now()
	    curr_hour=hr#curr_time.hour 
	    curr_day=curr_time.weekday()
	    curr_month=curr_time.month
	    #get weather now
	    weather=getCurrentWeather()
	    rain=np.asarray([weather['rain']])
	    snow=np.asarray([weather['snow']])
	    tempi=np.asarray([weather['tempi']])
        #create vector
	    hour=np.zeros((24))
	    hour[curr_hour]=1
	    
	    day=np.zeros((7))
	    day[curr_day]=1
	    
	    month=np.zeros((12))
	    month[curr_month]=1
	    
	    vec=np.concatenate((hour,day,month,rain,snow,tempi))
	    pred=model.predict(vec.reshape(1,-1))
	    scale=np.round(pred)[0]
	    value=(((pred*params[1])/params[2])+params[0])[0]

	    results.append([name,int(scale),int(value)])

	    #print('Fetching Time Now... '+str(curr_time))
	    #print('Fetching Weather Now... '+str(weather))
	    #print(vec)
	    #print(scale)
	    #print(value)
	    
	    with open('./turnstile_pred.txt', 'a') as file: #Option 1
	        file.write(name+','+str(int(scale))+','+str(int(value))+' \n')
	    file.close()

	return results #Option2: comment if don't want this option 





