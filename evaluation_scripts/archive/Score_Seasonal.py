# This script summarizes the scores from the weekly evaluations
# Potential additions:
# Adding a scoring component
# Adding something to output ranks by week 

# %%
import pandas as pd
import numpy as np
import os

# %% 
# User settings
forecast_num = 2
names = ['name1', 'name2', 'name3']
nstudent = len(names)

# %%
# load the observations
filepath = os.path.join('..','weekly_results', 'weekly_observations.csv')
observations = pd.read_csv(filepath, index_col='forecast_week')

# %% 
# Pull in everyones forecasts for a given week and write it out
forecasts = np.zeros((nstudent, 16))
for i in range(nstudent):
    #i = 0
    filename = names[i] + '.csv'
    filepath = os.path.join('..', 'forecast_entries', filename)
    print(filepath)
    temp = pd.read_csv(filepath, index_col='Forecast')
    forecasts[i,:] = temp.loc[forecast_num][3:]


# put it inot a data frame for labeling rows and columns
col_names = [str(x) for x in range(1, 17)]
forecastsDF = pd.DataFrame(data=forecasts, index=names, columns=col_names)

filename_out = 'seasonalVAL_forecast'+ str(forecast_num) + '.csv'
filepath_out = os.path.join('..', 'weekly_results', filename_out)
forecastsDF.to_csv(filepath_out, index_label='name')

# %%
# Calculate the RMSE values by week given the most updated observations
seasonal_score=np.zeros((nstudent, forecast_num ))

for i in range(1, forecast_num+1):
    print('Week' , i)
    filepath = os.path.join('..',
        'weekly_results', 'seasonalVAL_forecast' + str(i) + '.csv')
    temp = pd.read_csv(filepath, index_col='name')

    for s in range(nstudent):
        print(names[s])
        ftemp = np.array(temp.iloc[s][0:forecast_num])
        otemp = np.array(observations.observed[0:forecast_num])
        seasonal_score[s,(i-1) ]= np.sqrt(np.mean((ftemp-otemp)**2))

col_names = [str(x) for x in range(1, forecast_num+1)]
scoresDF = pd.DataFrame(data=seasonal_score, index=names, columns=col_names)

filename_out = 'seasonalRMSE_forecast' + str(forecast_num) + '.csv'
filepath_out = os.path.join('..', 'weekly_results', filename_out)
scoresDF.to_csv(filepath_out, index_label='name')
