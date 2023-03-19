# ENVIREMENTAL DATA PROCESSING TRAINING

* Things done :
- Data Restructuring reducing size from 10.4 GB to 2.1 GB
- Federated Learning, Machine Learning
- Multi threaded programming
- SciKitLearn
- Model - Data Pipelining

* This project was being researched for learning how to prosess enviremental data and federated learning.

* The data was downloaded in .nc (netcdf) format, which was then extracted to csv format but since the .nc format is wierdly packed the csv that was generated was also in a very bad format. It was so bad that it was capturing roughly around 10.7 GB space on disk for just 1 year data, also it was in a format that can never be used to train any machine learning model without rigerous preprocessing and restructuring.

* On a rough idea descrobing the dataset originally recieved : The data was in format of permutation and combinations of longitude, latitude and time.

* All this restructuring has to be done for every feature inside a seperate csv file (humidity, temperature, visibility, mean sea level, surface pressure, total precipitation, x comp of wind 1, y comp of wind 1, x comp of wind 2, y comp of wind 2)

* So the first part was surely to convert the data to trainable format. Then the model train could be trained.

* Also the this size of data can't be loaded in memory on a normal computer.

* Whole data for training the model was present in DATA directory relatative to the current path of all the programs used.

* Currently only generic methods are tested on thedataset and they are performing just OK, next step i am working is to create new model which performs better than the regular models.

* After all these the final part for this one is to meret the federated learning with the models and create a deplyment design.

# pre process 1 convert long lati tudinal data to discrete location data.py

* This program convert all the data fro the wierd format to tabular form (the CSV format), this is to be done for all types of features individually, by running the program for all the features individually, so I ran the program for all features at the same time using multi core processing of the data.

* This program creates a directory PREPROCESSED_DATA_1 inside which it creates directories (HUMIDITY, TEMPERATURE, VISIBILITY, MEAN_SEA_LEVEL, SURFACE_PRESSURE, TOTAL_PRECIPITATION, WIND_U_COMPONENT_1, WIND_V_COMPONENT_2, WIND_U_COMPONENT_2, WIND_V_COMPONENT_2)

* And inside these DIRECTORIES, there is data for locations, but thed ata has been formatted or segeragated wrt to different locations, each file is in the format FEATURE-NAME(longitude,latitude).csv .

* Now the format of data in csv files is in the format (time, value); also after using this program, the size of data on disk was reduced to 4.7 GB.

* The next task to perform is to merge all the features of a location in a single file. This has to be done for every location.

# pre process 2 merge discrete location data.py

* This program reads all the locations from the file LOCATIONS.txt and then searches for them in the directory PREPROCESSED_DATA_1 and its sub directories which contain data of location for each specfic feature.

* This program creates the directory PREPROCESSED_DATA_2 containing all features merged in single file for a location, and this is done for all locations; hence this directory contains all the locations data.

* Now the fomat of the data in csv file is in the format (time, feature 1, feature 2, ... feature n); also after running this program, the size of data on disk was reduced to 2.1 GB.

* Next part is to train and test models, that will be done using multi threaded training as it will reduce the training time by the fact of number of CPU cores in the computer.

# model 1 1.py

* This program trains the models for every location and test them for accuracy.

* The main models used are :
- KnnRegressor
- RandomForestRegressor
- LinearRegressor(SVR)

* Also the models were trained for different degree of polynomials usinf PolynomialFeaturesa and by creating a Pipeline.

* The models were trained on multi threads to reduce the training time, the tests were done on comparing the time required to train the models.

* The tests were done on 16 core CPU and 64 GB ram computer, on multi threaded training the program took 13.5 hours and the program was estimated to take 13.5 x 15 hours on single threaded training.

* Next to do apply federated learning on optimised models.
