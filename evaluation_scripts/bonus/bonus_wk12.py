# %% 
import sys
sys.path.insert(1, '../')
import eval_functions as ef
import random
import numpy as np
import pandas as pd
# %%
# Name: Laura Condon 
# Description: Assigning bonus points to the first 3 people alphabetically 
# who are not otherwise getting points
weeknum = 12

all_names = ef.getFirstNames()
print('Everyone:', all_names)
print()

#make a list of all the people who got points this week
points_list = ['Connal', 'Andrew', 'Stephanie', 'Xingyu','Sierra']
print('People getting points already:', points_list)
print()

# Make a list of the names of people not getting points
# Example with a list comprehension
nopoints_list = [name for name in all_names if name not in points_list]

filename = "scoreboard_week"+str(weeknum-1)+".csv"
filepath = os.path.join("..", "..", "weekly_results", filename)
#print(filepath)
temp = pd.read_csv(filepath, index_col='name')
temp_no= temp.loc[nopoints_list, :]
temp_no=temp_no.sort_values(by=['bonus'])
bonus_names = temp_no.index[0:3]
#print(bonus_names)
bonus_names=['Gigi', 'Xiang', 'David']

temp=temp.sort_values(by=['bonus'])
print("People Getting bonus points:", bonus_names)
print()

#Write out the bonus points
ef.write_bonus(bonus_names, all_names, weeknum)


#Example doing the same thing with a loop
#nopoints_list = []
#for name in all_names:
#    if name not in points_list:
#        nopoints_list.append(name)

# %%
