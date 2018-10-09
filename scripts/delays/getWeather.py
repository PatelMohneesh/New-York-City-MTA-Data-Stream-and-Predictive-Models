from urllib.request import urlopen
import json
from dateutil.rrule import *
from dateutil.parser import *

# Variables
daySt = "20141101" # state date
dayEnd = "20151101" # end date
outPath =  # output path
api =  # developer API key

# Create list of dates between start and end
days = list(rrule(DAILY, dtstart=parse(daySt), until=parse(dayEnd)))

# Create daily url, fetch json file, write to disk
def formatData(data):
    formattedData = []
    history = data.get('history')
    observations = history.get('observations')
    for observation in observations:
        del observation['dewptm']
        del observation['dewpti']
        del observation['wspdm']
        del observation['wspdi']
        del observation['wgustm']
        del observation['wgusti']
        del observation['wdird']
        del observation['wdire']
        del observation['vism']
        del observation['visi']
        del observation['pressurem']
        del observation['pressurei']
        del observation['windchillm']
        del observation['windchilli']
        del observation['heatindexm']
        del observation['heatindexi']
        del observation['precipm']
        del observation['precipi']
        del observation['icon']
        del observation['hail']
        del observation['thunder']
        del observation['tornado']
        del observation['metar']
        del observation['utcdate']
        del observation['fog']
        del observation['conds']
        formattedData.append(observation)
    return formattedData


def getclosesttimes(formattedData):
    newData = []
    # Only get 24 observations (corresponding to 24 hours)
    for i in range(0, 24):
        formattedTime = i * 60
        currMin = 9999
        currObs = formattedData[0]
        for d in formattedData:
            timeData = d.get('date')
            hour = int(timeData['hour'])
            min = int(timeData['min'])
            tmpTime = hour * 60 + min
            tDiff = abs(formattedTime - tmpTime)
            if (tDiff < currMin):
                currObs = d
                currMin = tDiff
        newData.append(currObs)
    return newData

for day in days:
    url = 'http://api.wunderground.com/api/' + api + '/history_' + day.strftime("%Y%m%d") + '/q/' + 'NY/New_York_City/' + '.json'
    response = urlopen(url)
    data = json.load(response)
    formattedData = formatData(data)
    newData = getclosesttimes(formattedData)
    with open(outPath + 'NYC' + '_' + day.strftime("%Y%m%d") + '.json', 'w') as outfile:
        json.dump(newData, outfile)



