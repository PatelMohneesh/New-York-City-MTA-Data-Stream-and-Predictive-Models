
from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import certifi
import json
import requests
import sys
from predict_turnstile_hour import pred
#from predict_turnstile import add_cordinates

application = Flask(__name__)

keyword_dict = {'keyword 0':0,'keyword 1':1,'keyword 2':2,'keyword 3':3,'keyword 4':4,'keyword 5':5,'keyword 6':6,'keyword 7':7,'keyword 8':8,'keyword 9':9,'keyword 10':10,'keyword 11':11,'keyword 12':12,'keyword 13':13,'keyword 14':14,'keyword 15':15,'keyword 16':16,'keyword 17':17,'keyword 18':18,'keyword 19':19,'keyword 20':20,'keyword 21':21,'keyword 22':22,'keyword 23':23,"":0}

#Handle POST Requests
@application.route ('/',methods = ['POST','GET'])
def update_map2():
    
    key = ""
    #r = ""
    center_lat = 40.768331
    center_long = -73.977533
    #40.768331, -73.977533
    
    
    if request.method == 'POST':
        key = request.form['keyword']
              
                
           
    
    #Update HTML webpage()
    result = pred(keyword_dict[key])
    
    return render_template("index.html",lat = center_lat, long = center_long, Stations = result)

if __name__ == "__main__":
    
    application.run(host='0.0.0.0', debug = True)
