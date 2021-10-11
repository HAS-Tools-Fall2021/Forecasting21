# %%
import sys
sys.path.insert(1, '../')
import eval_functions as ef
import pandas as pd

# %%
# Name: Andrew Hoopes
# Description: Assigning bonus points to the 3 people with the lowest overall score as
# of week 4. 

# Getting everyone's names
weeknum = 5
all_names = ef.getFirstNames()
print("Everyone in our class:", all_names)

# %%
# Read and make a pandas dataframe with all of the results from this week
week5 = pd.read_csv('../../weekly_results/forecast_week5_results.csv')
week4 = pd.read_csv('../../weekly_results/scoreboard_week4.csv')
forecast = week5[['1week_points','2week_points']].to_numpy()
# List of all of the names that got points this week 
points = []
for i in range(len(forecast)):
    if forecast[i, 0] > 0 or forecast[i, 1] > 0:
        points.append(all_names[i])
print("The people who received points this week:", points)

# %%
# Determines who has not received points 
no_points = []
for name in week5['name']:
    if name not in points:
        no_points.append(name)
print(no_points)

# %%
score = []
scorename=[]

for x in no_points:
    temp = week4[week4['name']==x]
    scorename.append(temp['name'].values[0])
    score.append(temp['total'].values[0])

name_and_score = pd.DataFrame(list(zip(scorename,score)), columns=['names', 'total'])

sorted = name_and_score.sort_values(by='total', ascending=True).head(3)
print(sorted)

bonus_names = ['Connal', 'Xueyan', 'Xiang']
# %%
# Write out the bonus points
ef.write_bonus(bonus_names, all_names, weeknum)

# %%
