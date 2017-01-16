# Yield-prediction-exercise
This repository is an example of how to predict winter wheat yield for several counties in the United States.
Source from https://github.com/aerialintel/data-science-challenge

## A brief description of the problem and how you chose to solve it.

The probelm is we would like to predict the winter weahter yield in the United States by a given geolocation (e.g., latitude and longtitude). The dataset includes two years 1) location and time such as county name, state, latitude, and longtitude, 2) and raw weather features such as temperature, precipitation, wind speed, and pressure, and 3) raw crop physiological features such as NDVI, day in season, and yield (label).  
Due to the natural of data included weather varaibles, I immediatelly recalled to use weather valiables to conduct a crop modeling by WOFOST to produce the simulated yield compared to the actual yield (label). In the model, this is several specific winter wheat modules can be used for yield simulation. Pressure and temperature will be used to calculate the ET demand, and leaf area index (LAI) will be caculated by GDD
However, I decided to try different machine learning algorithm includes regression, randomforest to train the model for predicting yield. 

## A high level timeline telling us what you tried and what the results from that were

1.Data wrangling
Read two .csv files and use pandas library to stack them to a single one. The reason is for training the model, it's better to have more yield data. The year variation may be considered.   
## What your final / best approach was and how it performed

A short description of the motivation behind the creation and maintenance of the project. This should explain **why** the project exists.

## Technical choices you made during the project

Provide code examples and explanations of how to get the project.

## What challenges or compromises did you face during the project?

Depending on the size of the project, if it is small and simple enough the reference docs can be added to the README. For medium size to larger projects it is important to at least provide a link to where the API reference docs live.

## What did you learn along the way?

Describe and show how to run the tests with code examples.

## If you had more time, what would you improve?

Let people know how they can dive into the project, include important links to things like issue trackers, irc, twitter accounts if applicable.

