# Yield-prediction-exercise
This repository is an example of how to predict winter wheat yield for several counties in the United States.
Source from https://github.com/aerialintel/data-science-challenge

## A brief description of the problem and how you chose to solve it.

The probelm is we would like to predict the winter weahter yield in the United States by a given geolocation (e.g., latitude and longtitude). The dataset includes two years 1) location and time such as county name, state, latitude, and longtitude, 2) and raw weather features such as temperature, precipitation, wind speed, and pressure, and 3) raw crop physiological features such as NDVI, day in season, and yield (label).  
Due to the natural of data included weather varaibles, I immediatelly recalled to use weather features to conduct a crop modeling by WOFOST to produce the simulated yield compared to the actual yield (label). In the model, this is several specific winter wheat modules can be used for yield simulation. Pressure and temperature will be used to calculate the ET demand, and leaf area index (LAI) will be caculated by grows degree days (GDD) accumulation.
However, I decided to try different machine learning algorithms includes regression, SVM, and randomforest etc. to train the model for predicting yield. 

## A high level timeline telling us what you tried and what the results from that were

1.Data wrangling:
- Read two .csv files and use pandas library to stack them to a single one. The reason is for training the model, it's better to have more yield data. The year variation might be considered due to the weather valirability in two years. However, due to high genetype and enviroment interation (G x E), the year valiration can be ignored.
- Several unecessary columns were droped. Due to data entry is in a daily base, features such as precipitationType and windBearing are not important. Two types of weather features in the dataset are important, temperature and accumulated precipitation. Because temperatureMax and temperatureMin, which determines the daily cummulated heat (GDD = (temperatureMax + temperatureMin) /2 - TemperatureBase). This is the key to decide how fast the weahter will grow. Also, minimum temperature is important for winter wheat because it need vernalization (cold temperature) to inducing flowering. Another feature is precipitation, which determines if wheat can get enough wate supply. The acumulated precipitation is more imporatant than its form or intensity, unless some region get flooded.
- The keeped columns included precipAccumulation,averge temperature,temperatureMin,temperatureMax, DayInSeason,NDVI ,Yield.

2.Quanlity control of the data:
- The accumulated precipitation was 19 inches which make sense since most of winter wheat region are relative dry. 
- The temperatureMax is greater than temperatureMin whic hsi valid. 
- The NDVI values are not in a range of 0 to 1. After plot NDVI, there is not pattern of increase at the middle of the season and decrease at the end of the season. Thus, NDVI is not considered. 

3.Model selection:
- Regression. 
## What your final / best approach was and how it performed



## Technical choices you made during the project

Provide code examples and explanations of how to get the project.

## What challenges or compromises did you face during the project?



## What did you learn along the way?

Describe and show how to run the tests with code examples.

## If you had more time, what would you improve?

Let people know how they can dive into the project, include important links to things like issue trackers, irc, twitter accounts if applicable.

