
# This script downloads the observations from USGS aggreages
# to weekly and saves as a csv

# Potential additions:
# Make this a function

# Modify so it reads in the previous observation file
# and only adds in the new obs

# Have this automatically check what day it is
# and figure out what weeks are complete
# rather than requiring a week nummber input

# %%
import pandas as pd
import numpy as np
import os
import dataretrieval.nwis as nwis


# %%
# User settings
# refer to Seasonal_Forecast_Dates.pdf for the
# list of dates associated with each forecast week
# you should set forecast_week equal to the forecast
# week that just completed
week = int(input('What forecast week is it? (1-16): ')) # Week 12, 11/13, Quinn and Ben
station_id = "09506000"

# %%
# read in the forecast data and setup a dataframe
# filepath = os.path.join('..', 'Seasonal_Foercast_Dates.csv')
filepath = os.path.join('../weekly_results',
                        'weekly_observations.csv')
print(filepath)
obs_table = pd.read_csv(filepath, index_col='forecast_week')


# %%
# Read in the observations and get weekly averages
for i in range(1, week+1):
    print(i)
    starti = obs_table.loc[i, 'start_date']
    endi = obs_table.loc[i, 'end_date']

    # read in the data from USGS
    # Read in the streamflow data and get the weekly average
    obs_day = nwis.get_record(sites=station_id, service='dv',
                              start=starti, end=endi, parameterCd='00060')
    obs_table.loc[i, 'observed'] = np.round(np.mean(obs_day['00060_Mean']), 3)


# %%
# Write the updated observations out
filepath_out = os.path.join('..', 'weekly_results', 'weekly_observations.csv')
obs_table.to_csv(filepath_out, index_label='forecast_week')

# %%
