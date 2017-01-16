# Yield-prediction-exercise
This repository is an example of how to predict winter wheat yield for several counties in the United States.
Source from https://github.com/aerialintel/data-science-challenge

## A brief description of the problem and how you chose to solve it.

- The probelm is we would like to predict the winter weahter yield in the United States by a given geolocation (e.g., latitude and longtitude). The dataset includes two years 1) location and time such as county name, state, latitude, and longtitude, 2) and raw weather features such as temperature, precipitation, wind speed, and pressure, and 3) raw crop physiological features such as NDVI, day in season, and yield (label).  
- Due to the natural of data included weather varaibles, I immediatelly recalled to use weather features to conduct a crop modeling by WOFOST to produce the simulated yield compared to the actual yield (label). In the model, this is several specific winter wheat modules can be used for yield prediction. Pressure and temperature will be used to calculate the ET demand, and leaf area index (LAI) will be caculated by grows degree days (GDD) accumulation.
- However, due to time constrain, I decided to try different machine learning algorithms by scikit leanr libraries includes regression, SVM, and DecisionTree etc. to train the model for predicting yield. 

## A high level timeline telling us what you tried and what the results from that were

1.Data wrangling:
- Read two .csv files and use pandas library to stack them to a single one. The reason is for training the model, it's better to have more yield data. The year variation might be considered due to the weather valirability in two years. However, due to high genetype and enviroment interation (G x E), the year valiration can be ignored.
- Several unecessary columns were droped. Due to data entry is in a daily base, features such as precipitationType and windBearing are not important. Two types of weather features in the dataset are important, temperature and accumulated precipitation. Because temperatureMax and temperatureMin, which determines the daily cummulated heat (GDD = (temperatureMax + temperatureMin) /2 - TemperatureBase). This is the key to decide how fast the weahter will grow. Also, minimum temperature is important for winter wheat because it need vernalization (cold temperature) to inducing flowering. Another feature is precipitation, which determines if wheat can get enough wate supply. The acumulated precipitation is more imporatant than its form or intensity, unless some region get flooded. DayInSeason determines will wheat can grow longer. The longer it grows, the more biomass (yield) it can accumulate.
- The kept columns included precipAccumulation,averge temperature,temperatureMin,temperatureMax,DayInSeason, NDVI ,Yield.

2.Quanlity control of the data:
- The accumulated precipitation was 19 inches maxiumn which makes sense since most of winter wheat region are relative dry. 
- The temperatureMax is greater than temperatureMin whic hsi valid. 
- The NDVI values are not in a range of 0 to 1. After plot NDVI, there is not pattern of increase at the middle of the season and decrease at the end of the season. Thus, NDVI is not considered. 

3.Model selection:
- Regression. Model: Yield ~ precipAccumulatio + TemperatureAverage + temperatureMin + DayInSeason    
  Very low accurary/score: 0.04 , (accuracy = clf.score(X_test, y_test))
- SVM (polynomy): computer not respond
- DecisionTree: computer crushed

4.Iteriate:
  Due to the low accurary, including droped weather features in the training to see whether the accuracy will increase
- Regression. Model: Yield ~ all except CountyName, State, and Date    
  Accracy increased: 0.23 (accuracy = clf.score(X_test, y_test))
- SVM (polynomy): computer not respond
- DecisionTree: 0.48, scores = cross_val_score(clf, X, y)

## What your final / best approach was and how it performed
-  Only the linear regression returns an accuracy score. Other algorithms failed to return a score.

## Technical choices you made during the project
Algorithms:
-  Regression: simple, aoid overfitting.
-  SVM (polynomy): catch interaction weather features
-  
Tool:
-  Python
   pro: easy to test mutiple algorithms (most of time one line of code)
   con: familarity 
-  R
   pro: familar
   con: less libraries in machine linearing compared with python. Later not easy to sacle up the code.
-  Traditional crop model sofeware
   pro: robust mechonitical models built in and tested. Can directly generate simulated wheat yield based on weather feature and crop      physilogical process, and conduct a one vs. one comparison. 
   con: cannot scaling up unless rewrite in python.

## What challenges or compromises did you face during the project?
Challenges
- Training: the features are time series data, while the label are time point. The mismatch caused when training the data each time footpoint printed to a same yield for a same county. This can cause a problem a label is not directly corresponding to a feature value rather than a set of features group by county (geolocaiton). Also, if the NDVI value is actual NDVI, It can actually correposnding to yield better because NDVI has strong correltion with leaf area index (LAI), which is a strong indicator of how well the crop conduct photosynthesis during the season and tthe biomass of the crop.  
- Missing feature: The difficulty was weather feature should has an geo-boundry because the enviroment effect on winter wheat will be different compare the wheat grow in northen to that grow in sourthen.
- Coding: When conduct cross-validation, stack on setting an array element with a sequence, which casue unequal X-train and y_train. The potential solution is to adde an additional values to the missed values position to that array in order to form a 2D array which match all the 1D array dimersionally.

## What did you learn along the way?

-  Use one/mutiple time series features (weather data) to train and predict one label (one yield value) may not be the way to predict yield. Especialy when when the yield is stronly related to the cultivar used (missed in dataset) and enviroment condition (weather, soil, and geolocaiton), only use seasonal weather data to train the model to predict yield is inadequent. 
-  Solution: add geolocation related data to the dataset which representive geo-features. Such as soil features, what soiltype for thegiven geolocations. For example, Farmers business network, an farmer data platform, has tested the cultivar type and soil type combination are the most important interaction which affects corn yield. 
-  When I exclude latitude and longtitude from the model, the accurary score drop to 0.1. While when I include the latitude and longtitude, the accurary score include to 0.23.

## If you had more time, what would you improve?
The part I would improve if I have more time:
-  Use deep neural newwork to predict the yield. The reason the deep learning outperform many other algorithms. Linterature has been reported to use ANN for wheat yield prediction.
And I also would like to add additional higher leavel features.
-  1) Evapotranspiration (ET). Use FAO54 Penman-Monteith method to calculate referece ET for wheat. Use the weather features such as solar radiation (pysolar library), temperature, relative humidity, and wind speed to cauclate ET. ET describes the water demand of the crop from the enviroment.
-  2) Soil data. Access SSURGO database to get the soil property which can determine how many water the soil can hold and provide to crop. This part describe the water supply from soil.
-  3) The ratio of ET/soil water is a good indicator of if crop will have sufficient water during season, thus affect its yield. 
-  4) Use WOFOST crop model modules to generate more higher crop development features such as LAI prediction, total above ground biomass prediction, daily dry matter increase rate. Those features may add weight to predicting yield.

