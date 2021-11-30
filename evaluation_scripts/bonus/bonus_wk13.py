# %%
import os
import sys
import pandas as pd
import numpy as np
from pandas.core.arrays.categorical import contains
sys.path.insert(1, '../')
import eval_functions as ef
import math
import string

# %%
# Steph Serrano: Assigning bonus points to people that didn't recieve points
# and whose names add up to the highest value

# Retreiving everyone's name in the class
weeknum = 13

all_names = ef.getFirstNames()
print(all_names)

# Reading from weekly_results .csv files
week13 = pd.read_csv('../../weekly_results/forecast_week13_results.csv')
forecast = week13[['1week_points', '2week_points']].to_numpy()

# %%
# List of all of the names that got points over both weeks
points = []
for i in range(len(forecast)):
    if forecast[i, 0] > 0 or forecast[i, 1] > 0:
        points.append(all_names[i])
print("People who received points this week:", points)

# %%
# List of names that did not get points
no_points = []
for name in week13['name']:
    if name not in points:
        no_points.append(name)
print(no_points)

# %%
# Assign values to each letter of alphabet
v = dict()
for index, letter in enumerate(string.ascii_lowercase):
   v[letter] = index + 1
print(v)

#%%
#Add values for everyone's names
Sierra = v['s']+v['i']+v['e']+2*v['r']+v['a']
Sierra
Connal = v['c']+v['o']+2*v['n']+v['a']+v['l']
Connal
Kevin = v['k']+v['e']+v['v']+v['i']+v['n']
Kevin
Gigi = 2*v['g']+2*v['i']
Gigi
Andrew = v['a']+v['n']+v['d']+v['r']+v['e']+v['w']
Andrew
David = 2*v['d']+v['a']+v['v']+v['i']
David
Jason = v['j']+v['a']+v['s']+v['o']+v['n']
Jason
Stephanie = v['s']+v['t']+2*v['e']+v['p']+v['h']+v['a']+v['n']+v['i']
Stephanie
Xingyu = v['x']+v['i']+v['n']+v['g']+v['y']+v['u']
Xingyu
Xueyan = v['x']+v['u']+v['e']+v['y']+v['a']+v['n']
Xueyan
Xiang = v['x']+v['i']+v['a']+v['n']+v['g']
Xiang

#%%
#Add values into a Pandas Dataframe 
value_points = {'Name': all_names, 'Value': [Sierra, Connal, Kevin,
    Gigi, Andrew, David, Jason, Stephanie, Xingyu, Xueyan, Xiang]}
points_value_df = pd.DataFrame(value_points)
points_value_df

#%%
#Dataframe with no_points names
#Removed "points" columns
no_points_df = points_value_df.drop(labels=
    [0, 1, 2, 4, 6, 7, 8], axis=0)
no_points_df

#%%
#Sorted top 3 values in no_points DataFrame
no_points_sort = no_points_df.sort_values(by='Value', 
    ascending = False).head(3)
no_points_sort

#%%
#Converted 'Name' column from DataFrame to a list
bonus_names = no_points_sort['Name'].to_list()
print(bonus_names)

#%%
#Eval Function to push bonus points to a CSV
ef.write_bonus(bonus_names, all_names, weeknum)
