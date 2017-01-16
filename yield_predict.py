import csv
import pandas as pd
import numpy as np
from sklearn import linear_model, cross_validation, svm, preprocessing
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import math
from sklearn.model_selection import GroupShuffleSplit
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.model_selection import GroupKFold
from sklearn.model_selection import LeavePGroupsOut
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score

#read data
data1 = pd.read_csv('wheat-2013-supervised.csv')
data2 = pd.read_csv('wheat-2014-supervised.csv')

#print(data1.head())
#merge two dataset for train the model later
merged = data1.append(data2, ignore_index=True)
merged = merged[["CountyName","State","Latitude","Longitude","Date","apparentTemperatureMax","apparentTemperatureMin","cloudCover","dewPoint","humidity","precipIntensity","precipIntensityMax","precipProbability","precipAccumulation","precipTypeIsRain","precipTypeIsSnow","precipTypeIsOther",	"pressure",	"temperatureMax","temperatureMin","visibility",	"windBearing","windSpeed","NDVI","DayInSeason","Yield" ]]
merged.to_csv('merged.csv', index=None, header=True)
mg = pd.read_csv('merged.csv')
#mg = mg[["CountyName",	"State","Latitude",	"Longitude","Date","precipAccumulation","temperatureMax","temperatureMin","NDVI","DayInSeason","Yield"]]
#mg = mg[["CountyName","precipAccumulation","temperatureMax","temperatureMin","NDVI","DayInSeason","Yield"]]
#mg["avgTemp"] = (mg["temperatureMax"] + mg["temperatureMin"]) / 2
#mg = mg[["CountyName","precipAccumulation","avgTemp","temperatureMin","DayInSeason","Yield"]]
#mg = mg[["precipAccumulation","avgTemp","temperatureMin","DayInSeason","Yield"]]
#mg = mg[["apparentTemperatureMax","apparentTemperatureMin","cloudCover","dewPoint","humidity","precipIntensity","precipIntensityMax","precipProbability","precipAccumulation","precipTypeIsRain","precipTypeIsSnow","precipTypeIsOther",	"pressure",	"temperatureMax","temperatureMin","visibility",	"windBearing","windSpeed","NDVI","DayInSeason","Yield" ]]
mg = mg[["Latitude","Longitude","apparentTemperatureMax","apparentTemperatureMin","cloudCover","dewPoint","humidity","precipIntensity","precipIntensityMax","precipProbability","precipAccumulation","precipTypeIsRain","precipTypeIsSnow","precipTypeIsOther",	"pressure",	"temperatureMax","temperatureMin","visibility",	"windBearing","windSpeed","NDVI","DayInSeason","Yield" ]]

#print(mg.head())
#print(mg.columns.values)

#stacked = mg[['CountyName']].stack()
#mg["id"] = pd.Series(stacked.factorize()[0], index=stacked.index).unstack()
#mg['id'] = mg['id'].convert_objects(convert_numeric=True) + 1
#print (mg['id'])

mg.dropna(inplace=True)
#mg = mg[np.isfinite(mg['NDVI'])]

#X = np.array(mg.drop(["Yield","CountyName", "id"],1))
#X = np.array(mg.drop(["Yield","CountyName"],1))
X = np.array(mg.drop(["Yield"],1))
#X = np.array(mg["temperatureMin"])
#X = preprocessing.scale(X)
#y = np.array(mg["Yield"])
y = np.asarray(mg['Yield'], dtype="|S6")
#X = mg[["precipAccumulation"]]
#y = mg[["Yield"]]

#colsRes = ['Yield']
#X_train = np.array(mg.drop(["Yield","CountyName"], axis = 1))
#Y_train = np.asarray(mg['Yield'], dtype="|S6")
#rf = RandomForestClassifier(n_estimators=10)
#rf.fit(X_train, Y_train)

#groups = mg['id'].tolist()
#gss = GroupShuffleSplit(n_splits=4, test_size=0.5, random_state=0)
#logo = LeaveOneGroupOut()
#gkf = GroupKFold(n_splits=4)
#lpgo = LeavePGroupsOut(n_groups=2)
#X_train, X_test, y_train, y_test = gss.split(X, y, groups=groups)
#X_train, X_test, y_train, y_test = logo.split(X, y, groups=groups)
#X_train, X_test, y_train, y_test = gkf.split(X, y, groups=groups)
#X_train, X_test, y_train, y_test = lpgo.split(X, y, groups=groups)

# Code for regression
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)



# Code for decision tree and cross_validation
clf = DecisionTreeClassifier(max_depth=None, min_samples_split=2,random_state=0)
scores = cross_val_score(clf, X, y)
print(scores.mean())
'''
#Code for SVM
#clf = svm.SVR(kernel="poly")
clf = LinearRegression()
#clf.fit(X, y)
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)

print(accuracy)

#visualize results
X = mg[["NDVI"]]
y = mg[["Yield"]]
plt.scatter(X, y)
plt.plot(X, clf.predict(X))
plt.show()
'''
