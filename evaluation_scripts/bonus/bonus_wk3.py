# %% 
import sys
sys.path.insert(1, '../')
import eval_functions as ef
import pandas as pd
import random
# %%
# Name: Xueyan Zhang
# Description: Assigning bonus points to the first 3 people alphabetically 
# who are not otherwise getting points
weeknum = 3

all_names = ef.getFirstNames()
print('Everyone:', all_names)
print()

# read forecast_week# to find out people who got points already this week
data = pd.read_csv('../../weekly_results/forecast_week3_results.csv')
forecast = data[['1week_points','2week_points']].to_numpy()
# %%
#make a list of all the people who got points this week
points_list = [ all_names[i] for i in range(len(forecast)) if forecast[i,0] > 0 or forecast[i,1] > 0]
#points_list = ['Sierra','Connal','Kevin','Gigi','Andrew','Stephanie','Xingyu', 'Xueyan', 'Xiang']
print('People getting points already:', points_list)
print()

# Make a list of the names of people not getting points
# Example with a list comprehension
nopoints_list = [name for name in all_names if name not in points_list]

#Choose the first 3 people not getting points
bonus_names = random.sample(nopoints_list,3)

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
