# -*- coding: utf-8 -*-
"""
Created on Janu 28 2019

@author: Md sohag miah
"""

import pandas as pd
import numpy as np

#Import Data Set
dataSet = pd.read_csv("diabetes.csv")

#print(dataSet.head())

#Total Null Value Check
print("How many Null value are here: ")
print(dataSet.isnull().sum())

## print(dataSet.isnull().values.any())

#All Column Data Type Check
dataSet.dtypes

# dataSet.corr()
# Diabetes True/False Count
diabetes_true_count = len(dataSet.loc[dataSet['Outcome'] == True])
diabetes_false_count = len(dataSet.loc[dataSet['Outcome'] == False])

print("True Outcome: {0}, False Outcome: {1}".format(diabetes_true_count, diabetes_false_count))

#Missing Zeros without Outcome Column
print("How many Zero value are here: ")
print(dataSet.iloc[:, 0 : 8].eq(0).sum())

# Feature Cloumn or Independent Variable
X = dataSet.iloc[:,:-1].values

#Dependent column or Predict Class
y = dataSet.iloc[:,8].values

# Zero fill with mean of the column
from sklearn.impute import SimpleImputer
fill_values = SimpleImputer(missing_values= 0, strategy = 'mean')
X[:,1:8] = fill_values.fit_transform(X[:,1:8])

#Trin/Test Split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 0)

#Feature Scaling

from sklearn.preprocessing import StandardScaler
scale_X = StandardScaler()
X_train = scale_X.fit_transform(X_train)
X_test = scale_X.transform(X_test) 

#SVM Classifier
from sklearn.svm import SVC
SVM_classifier = SVC(kernel = 'rbf', gamma = 'auto', random_state = 0)
SVM_classifier.fit(X_train, y_train)

SVM_y_pred = SVM_classifier.predict(X_test)


# Train/test Accuracy
from sklearn.metrics import confusion_matrix, accuracy_score
cm_SVM = confusion_matrix(y_test, SVM_y_pred)
ac_SVM = accuracy_score(y_test, SVM_y_pred)
print("Confusion Matrix :")
print(cm_SVM)
print("SVM Train/test Split Accurary: ", ac_SVM)

# K Fold Cross validation of decision Tree
from sklearn.model_selection import cross_val_score
SVMscore = cross_val_score(SVM_classifier, X, y, cv= 10).mean()
print("Accuracy of K fold cross validation using SVM:", SVMscore)

#Startified k Fold

from sklearn.model_selection import StratifiedKFold

accuracy = []
skf = StratifiedKFold(n_splits=10, random_state = None)
skf.get_n_splits(X, y)

#print("Confusion Matrix of K fold Cross validation ")
for train_index, test_index in skf.split(X,y):
   # print("Train: ",train_index, "Validation: ", test_index)
    X1_train, X1_test = X[train_index], X[test_index]
    y1_train, y1_test = y[train_index], y[test_index] 
    
    SVM_classifier.fit(X1_train, y1_train)
    prediction = SVM_classifier.predict(X1_test)
    #print( confusion_matrix(y1_test, prediction) )
    score = accuracy_score(y1_test, prediction ) 
    accuracy.append(score)
# print(accuracy)
# numpy
print("Accuracy of Startified K fold cross validation using SVM:", np.array(accuracy).mean())