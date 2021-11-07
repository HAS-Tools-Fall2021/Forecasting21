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
# Kevin Dyer: Assigning bonus points to people that didn't recieve points
# and have an 'E' in their first name

# Retreiving everyone's name in the class
weeknum = 10

all_names = ef.getFirstNames()
print(all_names)

# Reading from weekly_results .csv files
week10 = pd.read_csv('../../weekly_results/forecast_week10_results.csv')
forecast = week10[['1week_points','2week_points']].to_numpy()
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
for name in week10['name']:
    if name not in points:
        no_points.append(name)
print(no_points)
# %%
# Finding the 3 people who didn't recieve points
# and have an 'E' in their first name


bonus_names = ['']

# %%
# Write out the bonus points
ef.write_bonus(bonus_names, all_names, weeknum)