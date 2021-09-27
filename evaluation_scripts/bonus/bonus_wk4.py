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

# Determines who has already received points from the week1 and week2 forecasts
points_set = set({})
for x in week4['1week_ranking']:
    if week4['1week_ranking'][x] <= 3:
        points_set.add(week4['name'][x])

for x in week4['2week_ranking']:
    if week4['2week_ranking'][x] <= 3:
        points_set.add(week4['name'][x])
print("The people who received points this week:", points_set)

# %%
# Determines who has not received points 
no_points = []
for name in week4['name']:
    if name not in points_set:
        no_points.append(name)
print(no_points)

# %%
flow = []

for x in no_points:
    print(x)
    temp = week4[week4['name']==x]
    flow.append(temp['1week_forecast'].values[0])

name_and_flow = pd.DataFrame(list(zip(no_points, flow)), columns=['names', 'flow'])
print(name_and_flow)

sorted = name_and_flow.sort_values(by='flow', ascending=True).head(3)
print(sorted)

bonus_names = []

# worst case just add the names to bonus_names from ^^

# %%
#isn't working

print(sorted[['names']][:])

bonus_names.append(sorted['names'])
print(bonus_names)

# %%
# Write out the bonus points
ef.write_bonus(bonus_names, all_names, weeknum)
