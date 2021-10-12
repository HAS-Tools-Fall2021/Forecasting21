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
# Name: David Eduardo Morales
# Description: Assigning bonus points to greatest combined distance from 
# the one and two week 1st standard deviations

# %%
weeknum = 6

# Generate lists of names
first_names = ef.getFirstNames()
last_names = ef.getLastNames()

# %%
# Get names of students who did and did not receive points this week 
# (from Andrew's code)

# Reading from weekly_results .csv files
week6 = pd.read_csv('../weekly_results/forecast_week6_results.csv')
week5 = pd.read_csv('../weekly_results/scoreboard_week5.csv')
forecast = week6[['1week_points','2week_points']].to_numpy()

# Create lists to capture values from floops:
points = []
no_points = []

# Floop for students who did receive points
for i in range(len(forecast)):
    if forecast[i, 0] > 0 or forecast[i, 1] > 0:
        points.append(first_names[i])
print("Students who received points this week:", points)

# Floop for students who did not receive points
for name in week5['name']:
    if name not in points:
        no_points.append(name)
print("Students who did not receive points this week:", no_points)

# %%
# Create floop to consolidate students' one and two week forecasts into 
# a single dataframe for calculation of mean and standard deviation values.

# Change directory for function
# os.chdir('../')
# Create lists to capture values from floop
student_name = []
wk1_est_list = []
wk2_est_list = []

for name in last_names:
    # Read students' .csv into floop
    student_table = ef.student_csv(name)

    # Pull week 1 & 2 estimates from .csv
    wk1_est = student_table.iloc[5, 1]
    wk2_est = student_table.iloc[4, 2]

    # Add name and estimates to lists
    student_name.append(name)
    wk1_est_list.append(wk1_est)
    wk2_est_list.append(wk2_est)
    
# Convert lists into dataframes
student_name_df = pd.DataFrame(first_names)
wk1_est_df = pd.DataFrame(wk1_est_list)
wk2_est_df = pd.DataFrame(wk2_est_list)

# Concatenate dfs into one main df of student names and their forecasts
est_6_df = pd.concat([student_name_df, wk1_est_df, wk2_est_df], axis=1)
est_6_df.columns = ['FirstName', 'Wk1 Forecast', 'Wk2 Forecast']

# %%
# Gather statistics from Forecast 6 df generated in above floop
est_6_stat = est_6_df.describe()

# Create list to capture mean + std value (mean_std) for each week forecast 
mean_std_list = []

# Use floop to calculate the mean + std value
for i in range(2):
    mean_std = est_6_stat.iloc[1, i] + est_6_stat.iloc[2, i]
    mean_std_list.append(mean_std)

# Add mean + std row to statistic dataframe
est_6_stat.loc['mean + std'] = mean_std_list

# %%
# Create floop for calculating distance of each week projection from the 1st std
# using absolute value: sqrt(x**2)

# Create lists to capture forecast - mean_std for each week
wk1_std_dist_list = []
wk2_std_dist_list = []

for i in range(len(student_name)):
    # Find the difference between students' est and the mean_std for both weeks
    wk1_std_dist = math.sqrt((est_6_df.iloc[i,1] - est_6_stat.iloc[-1, 0]) ** 2)
    wk2_std_dist = math.sqrt((est_6_df.iloc[i,2] - est_6_stat.iloc[-1, 1]) ** 2)
    
    # Add these values to respective lists
    wk1_std_dist_list.append(wk1_std_dist)
    wk2_std_dist_list.append(wk2_std_dist)

# Convert lists into dataframes
wk1_std_dist_df = pd.DataFrame(wk1_std_dist_list)
wk2_std_dist_df = pd.DataFrame(wk2_std_dist_list)

# Concatenate dfs of std_dist values for each week with students' name
std_dist_df = pd.concat([student_name_df, wk1_std_dist_df, wk2_std_dist_df], axis=1)
std_dist_df.columns = ['firstname', 'wk1_std_dist', 'wk2_std_dist']

# %%
# Create floop for removing students' name from df if they receieved points

for name in points:
    index_name = std_dist_df[std_dist_df['firstname'] == name].index
    std_dist_df.drop(index_name, inplace=True)

# Add column of the combined distance from weekly std to df
std_dist_df['total_std_dist'] = std_dist_df['wk1_std_dist'] + \
                                std_dist_df['wk2_std_dist']

# Sort dataframe to find highest combined distances
final_sort = std_dist_df.sort_values(by='total_std_dist', ascending=False)
final_sort

# %%
bonus_names = ['Stephanie', 'Sierra', 'Xueyan']

ef.write_bonus(bonus_names, first_names, weeknum)
# %%
