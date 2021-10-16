# %%
import numpy as np
import os
import pandas as pd
import sys
sys.path.insert(1, '..\\')
import eval_functions as ef

# %%
# Name: Xiang Zhong
# Description: Assigning bonus points to lowest frequency of
#              getting points

weeknum = 7

all_names = ef.getFirstNames()
print(all_names)

# %%
# Get the frequency of getting points for each student
nstudent = len(all_names)
freq = pd.DataFrame({'freq': np.zeros(nstudent)},
                    index=all_names)

for i in range(1, (weeknum + 1)):
    filename = "forecast_week"+str(i)+"_results.csv"
    filepath = os.path.join("..", "..", "weekly_results", filename)
    print(filepath)
    temp = pd.read_csv(filepath, index_col='name')
    temp_week1 = np.ceil(temp.loc[freq.index, '1week_points']/2)
    temp_week2 = np.ceil(temp.loc[freq.index, '2week_points']/2)
    freq.loc[:, 'freq'] += (temp_week1 + temp_week2)

print(freq)

# %%
# Make a list of the names of people not getting points
# nor the evaluator ("Xiang")
all_list = pd.read_csv(filepath, index_col='name')
nopoints_list = all_list[(all_list["1week_points"] +
                          all_list["2week_points"]) == 0].index
freq = freq.loc[nopoints_list, :]
freq = freq.sort_values(by=['freq'])

# %%
# Pick bonux getting names by lowest frequency of getting points
bonus_names = freq.index[0:3]
print(bonus_names)

# Write out the bonus points
ef.write_bonus(bonus_names, all_names, weeknum)
