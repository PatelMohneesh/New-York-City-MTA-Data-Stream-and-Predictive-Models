import os
import pickle
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import matplotlib.pyplot as plt


def predict(X_test):
    """This function takes a dataset and predict the class label for each datapoint should be in.
    Parameters ----------dataset: M X D numpy array
    A dataset represented by numpy-array
    Returns -------M x 1 numpy array
    Returns a numpy array of predicted class labels
    """        
    with open(os.getcwd()+'/Classifier_params2_adaboost.pkl', 'rb') as f:      ####The classifier is stored in the Classifer_params pickle file which I am calling
        clf = pickle.load(f)
    
    #print(clf)
    y_pred = clf.predict(X_test)                                            ###I obtain obtain predicted values by calling the predict function for the classifer
    
    return(y_pred)                                                          ###I return the result
    

if __name__ == "__main__":

    with open(os.getcwd()+'/data_x2.pkl', 'rb') as f:        ###load x_data
        x_obj = pickle.load(f)
    x_train = x_obj
    with open(os.getcwd()+'/data_y2.pkl', 'rb') as f:        ###load y_data
        y_obj = pickle.load(f)
    with open(os.getcwd() + '/datetimes2.pkl', 'rb') as f:
        datetimes = pickle.load(f)
    y_actual = np.asarray(y_obj)
    y_pred = predict(x_train)

    x_train["y_actual"] = y_actual
    x_train["y_pred"] = y_pred
    """
    tmp = x_train.copy()
    del tmp["snow"]
    del tmp["rain"]
    tmp2 = tmp.groupby("hour").sum()


    hours_y = tmp.groupby(["hour"]).sum().reset_index()
    weekdays_y = tmp.groupby(["weekday"]).sum().reset_index()

    del hours_y["weekday"]
    del weekdays_y["hour"]

    
    hour_data_x = np.asarray(hours_y["hour"])
    hour_data_y = np.asarray(hours_y["y_actual"])
    width = 1/1.5
    N = len(hour_data_x)
    x = range(N)
    plt.bar(hour_data_x,hour_data_y,width,color="blue")
    plt.ylabel("Delays")
    plt.xlabel("Hour")
    plt.title("Delays per hour (11/01/2014 - 10/29/2015)")
    
    weekday_data_x = np.asarray(weekdays_y["weekday"])
    weekday_data_y = np.asarray(weekdays_y["y_actual"])
    width = 1 / 1.5
    plt.bar(weekday_data_x, weekday_data_y, width, color="blue")
    plt.ylabel("Delays")
    plt.xlabel("Weekday")
    plt.title("Delays per day of the week (11/01/2014 - 10/29/2015)")
    plt.xticks([0,1,2,3,4,5,6], ["Mon","Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"])
    """


    data_all = x_train.copy()
    data_all["y_actual"] = y_actual
    data_all["y_predic"] = y_pred
    print(data_all["y_actual"].sum())
    print(data_all["y_predic"].sum())
    data_all.to_pickle("data_all.pkl")



    datetimes_filt = datetimes[0:300]
    y_actual_filt  = y_actual[0:300]
    y_pred_filt    = y_pred[0:300]
    x_rain_filt    = x_train["rain"]
    x_rain_filt    = np.asarray(x_rain_filt)
    x_rain_filt = x_rain_filt[0:300]
    x_snow_filt    = x_train["snow"]
    x_snow_filt    = np.asarray(x_snow_filt)
    x_snow_filt = x_snow_filt[0:300]
    plt.plot(datetimes_filt, y_actual_filt, "ro", datetimes_filt, x_rain_filt, "b+")
    plt.ylabel("Delay")
    plt.xlabel("Dates")
    plt.title("Delays (from 11/01/2014 - 11/13/2014)")
    print("hello")
