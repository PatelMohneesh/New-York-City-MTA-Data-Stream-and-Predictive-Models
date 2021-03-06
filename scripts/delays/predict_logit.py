import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression

def trainlogit(X, y, test_size=0.3):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=None)

    logistic = LogisticRegression()


    logistic.fit(X_train, y_train)
    train_accuracy = logistic.score(X_train, y_train)
    test_accuracy = logistic.score(X_test, y_test)
    print("Training accuracy: {}".format(train_accuracy))
    print("Testing accuracy: {}".format(test_accuracy))

    return logistic


if __name__ == "__main__":
    with open(os.getcwd() + '/data_x2.pkl', 'rb') as f:  ###load x_data
        x_obj = pickle.load(f)

    with open(os.getcwd() + '/data_y2.pkl', 'rb') as f:  ###load y_data
        y_obj = pickle.load(f)

    clf = trainlogit(x_obj, y_obj)  ###Not dumping classifier as I am not this is not my final classifier
    pickle.dump(clf, open("Classifier_params2_logit.pkl", "wb"))
