# New-York-City-MTA-Data-Stream-and-Predictive-Models
Monitored fastest routes, predicted delays and calculated station crowdedness using Machine Learning techniques for NYC Subway


MTA Trains and Weather

This project proposes a real-time application to provide New York MTA data to customers in a more informative manner. We do so by using MTA streaming updates in conjunction with real-time weather and historical turnstile data to give well-rounded information on fastest routes available, destination ETA. In addition we also provide a metric to inform riders on crowd conditions in their trip.  Our application is built on top of GTFS real-time format.  We used turnstile data for the past 2 years to employ Random Forest Regression to predict station entries. Our best model gives 0.90 R-squared on the validation set whereas the average R-squared achieved is generally 0.74.

## Getting Started

Run application.py, open http://0.0.0.0:5000 in web browser, works best in Safari & Google Chrome. 

Follow the instructions described in the video: 

Link: https://www.youtube.com/watch?v=2HE18vCyBig

##
To run the MTA Stream application. Open MTAStream folder and run runMTAstream.py and follow the onscreen instructions.

Links to use the API: 

For trip initialization: https://ed35eyqphd.execute-api.us-east-1.amazonaws.com/prod/getTrip?start=14%20St&end=116%20St%20-%20Columbia%20University 
For trip updates: https://ed35eyqphd.execute-api.us-east-1.amazonaws.com/prod/getTripUpdate?start=14%20St&end=116%20St%20-%20Columbia%20University&tripstart=130550_2..N01R&tripend=132800_1..N02R

Replace the start, end, tripstart, and tripend query parameters as necessary.
Current available options: 14 St, 34 St - Penn Station, Times Sq - 42 St, 59 St - Columbus Circle, 72 St, 116 St - Columbia University


