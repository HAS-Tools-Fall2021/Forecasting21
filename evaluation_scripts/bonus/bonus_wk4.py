# %%
import sys
sys.path.insert(1, '../')
import eval_functions as ef
import pandas as pd

# %%
# Name: Gigi Giralte
# Description: Assigning bonus points to the 3 people that forecasted the lowest flow. 

# Getting everyone's names
weeknum = 4
all_names = ef.getFirstNames()
print("Everyone in our class:", all_names)

# %%
# Reads and makes a panda dataframe with all of the results from this week
week4 = pd.read_csv('../../weekly_results/forecast_week4_results.csv')
forecast = week4[['1week_points','2week_points']].to_numpy()
# List of all of the names that got points this week 
points = []
for i in range(len(forecast)):
    if forecast[i, 0] > 0 or forecast[i, 1] > 0:
        points.append(all_names[i])
print("The people who received points this week:", points)

# %%
# Determines who has not received points 
no_points = []
for name in week4['name']:
    if name not in points:
        no_points.append(name)
print(no_points)

# %%
flow = []

for x in no_points:
    temp = week4[week4['name']==x]
    flow.append(temp['2week_forecast'].values[0])

name_and_flow = pd.DataFrame(list(zip(no_points, flow)), columns=['names', 'flow'])

sorted = name_and_flow.sort_values(by='flow', ascending=True).head(3)
print(sorted)

bonus_names = ['Monique', 'Kevin', 'Andrew']
# %%
# Write out the bonus points
ef.write_bonus(bonus_names, all_names, weeknum)

# %%
