# %%
import os
import sys
import pandas as pd
sys.path.insert(1, '../')
import eval_functions as ef
import math

# %%
# Name: David Eduardo Morales
# Description: Assigning bonus points to greatest 
# value of each std

weeknum = 6

# Generate lists of names
first_names = ef.getFirstNames()
last_names = ef.getLastNames()

# %%
# Create floop to consolidate students' one and two week forecasts into 
# a single dataframe for calculation of mean and standard deviation values.

# Change directory for function
os.chdir('../')
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
    
# Convert lists into
student_name_df = pd.DataFrame(first_names)
wk1_est_df = pd.DataFrame(wk1_est_list)
wk2_est_df = pd.DataFrame(wk2_est_list)

# Concatenate dfs into one main df of student names and their forecasts
est_6_df = pd.concat([student_name_df, wk1_est_df, wk2_est_df], axis=1)
est_6_df.columns = ['LastName', 'Wk1 Forecast', 'Wk2 Forecast']

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
# Create floop for identifying which students came closest to weekly std
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
std_dist_df.columns = ['lastname', 'wk1_std_dist', 'wk2_std_dist']

# %%
std_dist_df.sort_values(by='wk1_std_dist')
std_dist_df.sort_values(by='wk2_std_dist')

# %%
# need to include code that determines who has already gotten points and then
# remove their row from the dataframe in order to sort_values for only those
# who are eligible for points

# creat variable that contains list of eligible names and 

std_dist_df[std_dist_df['lastname'] == 'Kevin']

