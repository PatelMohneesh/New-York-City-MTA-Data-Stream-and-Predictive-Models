import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier

def trainAdaboost(X, y, test_size=0.3):
        
    X_train, X_test, y_train, y_test = train_test_split(                ###I split the data into testing and training
            X, y, test_size=test_size, random_state=None)
    
    
    adaboostclf = AdaBoostClassifier(DecisionTreeClassifier(max_depth=5),       ###I apply appropriate parameters for the Adaboost classifier
                         algorithm="SAMME",                                     ###Paramters obtained from sklearn documentation
                         n_estimators=600)
    
    adaboostclf.fit(X_train,y_train)                                ###I generate the classifer
    train_accuracy = adaboostclf.score(X_train, y_train)            ###I compute the training error
    test_accuracy = adaboostclf.score(X_test, y_test)               ###I compute the testing error 
    print("Training accuracy: {}".format(train_accuracy))
    print("Testing accuracy: {}".format(test_accuracy))
    
    return adaboostclf
    

if __name__ == "__main__":



    with open(os.getcwd()+'/data_x2.pkl', 'rb') as f:        ###load x_data
        x_obj = pickle.load(f)
     
    with open(os.getcwd()+'/data_y2.pkl', 'rb') as f:        ###load y_data
        y_obj = pickle.load(f)
        
        
    #min_max_scaler = preprocessing.MinMaxScaler()                       ###Perform min_max scaling
    #x_obj = min_max_scaler.fit_transform(x_obj)
    
    #normalizer = preprocessing.Normalizer().fit(x_obj)                  ###Perform normalization
    #normalizer.transform(x_obj)
    
    clf = trainAdaboost(x_obj,y_obj)                                    ###Train classifer
    
    pickle.dump(clf, open( "Classifier_params2.pkl", "wb" ) )          ###Dump into Classifer_params pickle file, this is my final submission
    
