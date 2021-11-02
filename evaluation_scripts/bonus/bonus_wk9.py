# %%
import os
import sys
import pandas as pd
import numpy as np
from pandas.core.arrays.categorical import contains
sys.path.insert(1, '../')
import eval_functions as ef
import math

# %%
# Sierra Bettis: Assigning bonus points to people that forecasted the highest flow values
# and have not received points yet

# Retreiving everyone's name in the class
weeknum = 9

all_names = ef.getFirstNames()
print(all_names)

# Reading from weekly_results .csv files
week9 = pd.read_csv('../../weekly_results/forecast_week9_results.csv')
forecast = week9[['1week_points','2week_points']].to_numpy()
# %%
# List of all of the names that got points this week
points = []
for i in range(len(forecast)):
    if forecast[i, 0] > 0 or forecast[i, 1] > 0:
        points.append(all_names[i])
print("The people who received points this week:", points)

# %%
# List of all of the names that did not get points this week
no_points = []
for name in week9['name']:
    if name not in points:
        no_points.append(name)
print(no_points)
# %%
# Finding the 3 people who did not receive points this week
# and reported the highest flow values
flow = []
for i in no_points:
    temp = week9[week9['name'] == i]
    flow.append(temp['2week_forecast'].values[0])

name_and_flow = pd.DataFrame(list(zip(no_points, flow)), columns=['names','flow'])

sorted = name_and_flow.sort_values(by='flow', ascending=False).head(3)
print(sorted)

bonus_names = ['Xingyu', 'Stephanie', 'Andrew']

# %%
# Write out the bonus points
ef.write_bonus(bonus_names, all_names, weeknum)
# %%
