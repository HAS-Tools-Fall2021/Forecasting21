# This script summarizes the scores from the weekly evaluations

# Potential additions:
# Get weekly totals
# get totals by forecast type and bonus points
# Condense the bonus points for each week into one column
# Calculate ranks and write this out

# %%
import pandas as pd
import numpy as np
import os

# %%
# User variables
forecast_num = 2

#  %%
# Setup the scoreboard
names = ['name1', 'name2', 'name3']
nstudent = len(names)
scoreboard=pd.DataFrame({'total': np.zeros(nstudent)},  index=names)

# %%
#Read in the weekly forecasts
forecast_num=2
for i in range(1, forecast_num+1):
    print(i)
    # read and add the 1 week forecast
    filename = '1week_forecast' + str(i) + '.csv'
    filepath = os.path.join('..', 'weekly_results', filename)
    if os.path.exists(filepath):
        print(filepath)
        temp = pd.read_csv(filepath, index_col='name')
        label='_F'+str(i)+'W1'
        temp=temp.rename(columns={'points':'points'+label, 'bonus_points': 'bonus'+label})
        scoreboard = pd.merge(left=scoreboard, right=temp[['points'+label, 'bonus'+label]], 
                              left_index=True, right_index=True)
    
    # read and add the 2 week forecast
    filename = '2week_forecast' + str(i) + '.csv'
    filepath = os.path.join('..', 'weekly_results', filename)
    if os.path.exists(filepath):
        print(filepath)
        temp = pd.read_csv(filepath, index_col='name')
        label='_F'+str(i)+'W2'
        temp=temp.rename(columns={'points':'points'+label, 'bonus_points': 'bonus'+label})
        scoreboard = pd.merge(left=scoreboard, right=temp[['points'+label, 'bonus'+label]], 
                              left_index=True, right_index=True)


# %%
scoreboard['total']=scoreboard.sum(axis=1)
# technically this would be a more correct way to do this
# scoreboard.loc[:, scoreboard.columns != 'total'].sum(axis=1)

# Write out the reults
filepath_out = os.path.join('..', 'scoreboard.csv')
scoreboard.to_csv(filepath_out, index_label='name')

# %%
