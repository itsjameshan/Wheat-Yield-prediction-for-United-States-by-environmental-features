# Yield-prediction-exercise
This repository is an example of how to predict winter wheat yield for several counties in the United States.
Source from https://github.com/aerialintel/data-science-challenge

## A brief description of the problem and how you chose to solve it.

- The problem is we would like to predict the winter weather yield in the United States by a given geolocation (e.g., latitude and longitude). The dataset includes two years 1.) location and time such as county name, state, latitude, and longitude, 2.) and raw weather features such as temperature, precipitation, wind speed, and pressure, and 3.) raw crop physiological features such as NDVI, day in season, and yield (label).  
- Due to the natural of data included weather variables, I immediately recalled using weather features to conduct crop modeling by WOFOST model (http://bit.ly/2jnY8mw) to produce the predicted yield compared to the actual yield (label). In the model, this is several specific winter wheat modules can be used for yield prediction. Pressure and temperature will be used to calculate the ET demand, and leaf area index (LAI) will be calculated by grows degree days (GDD) accumulation.
- However, due to time constraint, I decided to try different machine learning algorithms by scikit learn library includes regression, SVM, and DecisionTree etc. to train the model for predicting yield. 

## A high level timeline telling us what you tried and what the results from that were

1.Data wrangling:
- Read two .csv files and use pandas library to stack them to a single one. The reason is for training the model; it's better to have more yield data. The year variation might be considered due to the weather variability in two years. However, due to high genotype and environment interaction (G x E), the year variation can be ignored.
- Several unnecessary columns were dropped. Due to data entry is on a daily base, features such as precipitationType and windBearing are not important. Two types of weather features in the dataset are important, temperature and accumulated precipitation. Because temperatureMax and temperatureMin, which determines the daily accumulated heat (GDD = (temperatureMax + temperatureMin) /2 - TemperatureBase). This is the key to deciding how fast the wheat will grow. Also, the minimum temperature is important for winter wheat because it needs vernalization (cold temperature) to inducing flowering. Another feature is precipitation, which determines if wheat can get enough water supply. The accumulated precipitation is more important than its form or intensity unless some region gets flooded. DayInSeason determines will wheat can grow longer. The longer it grows, the more biomass (yield) it can accumulate.
- The kept columns included precipAccumulation,average temperature,temperatureMin,temperatureMax,DayInSeason, NDVI ,Yield.

2.Quality control of the data:
- The accumulated precipitation was 19 inches maximum which makes sense since most of the winter wheat region are relatively dry. 
- The temperatureMax is greater than temperatureMin which is valid. 
- The NDVI values are not in a range of 0 to 1. After plotting NDVI, there is no pattern of increase NDVI in the middle of the season and decrease at the end of the season. Thus, NDVI is not considered. 

3.Model selection:
- Regression. Model: Yield ~ precipAccumulatio + TemperatureAverage + temperatureMin + DayInSeason    
  Very low accurary/score: 0.04 , (accuracy = clf.score(X_test, y_test))
- SVM (polynomy): computer not respond
- DecisionTree: computer crushed

4.Iteration:
  Due to the low accuracy, including dropped weather features in training to see whether the accuracy will increase
- Regression. Model: Yield ~ all features except CountyName, State, and Date    
  Accracy increased: 0.23 (accuracy = clf.score(X_test, y_test))
- SVM (polynomy): computer not respond
- DecisionTree: 0.48, (scores = cross_val_score(clf, X, y))

## What your final / best approach was and how it performed
-  DecisionTree returns an 0.48 accuracy score which can barely predict yield. Linear regression is worse.

## Technical choices you made during the project
Algorithms:
-  Regression: simple, avoid overfitting.
-  SVM (polynomial): catch interaction weather features
-  DecisionTree: when have a lot of “leaves”, in our case the yield values

Tool:
-  Python
   pro: easy to test multiple machine learning algorithms (most of time one line of code)
   con: familiarity not 
-  R
   pro: familiar
   con: fewer libraries in machine learning compared with python. Later on, not easy to scale up the code.
-  Traditional crop model software
   pro: robust mechanistic models built in and tested. Can directly generate predicted wheat yield based on weather feature and crop physiological process, and conduct a one vs. one comparison. 
   con: cannot scaling up unless rewrite in python.

## What challenges or compromises did you face during the project?
Challenges
- Training: the features are time series data, while the label is time point. The mismatch caused when training the data each time footprint printed to the same yield for the same county. This can cause a problem a label is not directly corresponding to a feature value at one day rather than a set of feature group by a county (geolocation). Also, if the NDVI value is actual true NDVI, It can actually correspond to yield better because NDVI has a strong correlation with leaf area index (LAI), which is a strong indicator of how well the crop conducts photosynthesis during the season and the biomass of the crop.  
- Missing feature: The difficulty was weather feature should have a geo-boundary because the environment effect on winter wheat will be different compare the wheat grow in northern to that grow in southern.
- Coding: When conduct cross-validation, I get stuck on the value error of setting an array element with a sequence, which causes unequal X-train and y_train. The potential solution is to add additional values to the missed values in that array to form a 2D array which matches all the 1D array dimensionally.

## What did you learn along the way?

-  Problem 1: Use one/multiple time series features (weather data) to train and predict one label (one yield value) may not be the best way to predict yield. Especially when the yield is strongly related to the cultivar used (missed in the dataset) and environment condition (weather, soil, and geolocation), only use seasonal weather data to train the model to predict yield is inadequate. 
-  Solution 1: add geolocation related data to the dataset which representative geo-features. Such as soil features, what soil type for the given geolocations. Soil type is very important in yield prediction. For example, Farmers business network, a farmer data platform, has tested the cultivar type and soil type combination are the most important interaction which affects corn yield. 
-  When I exclude latitude and longitude from the model, the accuracy score drops to 0.1. While when I include the latitude and longitude, the accuracy score includes to 0.23.
-  Problem 2: I haven’t found the right machine learning algorithms.
-  Solution 2: Spend more time on exploring other algorithms.

## If you had more time, what would you improve?
The part I would improve if I have more time:
-  Use the deep neural network to predict the yield. The reason the deep learning outperforms many other algorithms. Literature has been reported to use ANN for wheat yield prediction. http://ieeexplore.ieee.org/document/7006239/?reload=true
And I also would like to add additional higher level features.
-  1) Evapotranspiration (ET) (**the code for calculating ET is uploaded**). Use FAO54 Penman-Monteith method to calculate reference ET for wheat. Use the weather features such as solar radiation (pysolar library), temperature, relative humidity, and wind speed to calculate ET. ET describes the water demand of the crop from the environment. 
-  2) Soil data. Access SSURGO database to get the soil property which can determine how many water the soil can hold and provide to the crop. This part describe the water supply from soil.
-  3) The ratio of ET/soil water is a good indicator of if crop will have sufficient water during season, thus affect its yield. 
-  4) Use WOFOST crop model modules to generate higher crop features such as LAI, total above ground biomass, daily dry matter increase rate. Those features may add accuracy to predicting yield.
