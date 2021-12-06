# %%
# Add imports
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.insert(1, '../')
import eval_functions as ef

import hydroeval as hyd

# %%
# Name: Connal Boyd
# Description: Assigning bonus points to the first 3 people 
# who's forecasts were most accurate to the observed flow from week to week
# based on best fit slope value of scatter plot comparisons

weeknum = 14

first_names = ef.getFirstNames()
print(first_names)

last_names = ef.getLastNames()
print(last_names)

# %%
# Reading data in from weekly_results .csv files

week14 = pd.read_csv('../../weekly_results/forecast_week14_results.csv')
forecast = week14[['1week_points', '2week_points']].to_numpy()

# %%
# List of all of the names that got points over both weeks
points = []
for i in range(len(forecast)):
    if forecast[i, 0] > 0 or forecast[i, 1] > 0:
        points.append(first_names[i])
print('People already receiving points:', points)

# List of names that did not get points
no_points = []
for name in week14['name']:
    if name not in points:
        no_points.append(name)
print('People not yet receiving points:', no_points)

# %%
obs_file = 'weekly_observations.csv'
obs_path = os.path.join('..', '..', 'weekly_results', obs_file)
temp = pd.read_csv(obs_path, index_col='forecast_week')
obsvd = temp[0:14]

sim_file = str('Boyd') + '.csv'
sim_path = os.path.join('..', '..', 'forecast_entries', sim_file)
frcst = pd.read_csv(sim_path, index_col='Forecast #')
oneweek = frcst['1week']

# Create best fit line function for use plotting scatter plots

def best_fit(X, Y):

    xbar = sum(X)/len(X)
    ybar = sum(Y)/len(Y)
    n = len(X) # or len(Y)

    numer = sum([xi*yi for xi,yi in zip(X, Y)]) - n * xbar * ybar
    denum = sum([xi**2 for xi in X]) - n * xbar**2

    b = numer / denum
    a = ybar - b * xbar

    print('best fit line:\ny = {:.2f} + {:.2f}x'.format(a, b))

    return a, b

# %%
# Read in observed values file
obs_file = 'weekly_observations.csv'
obs_path = os.path.join('..', '..', 'weekly_results', obs_file)
temp = pd.read_csv(obs_path, index_col='forecast_week')
obsvd = temp[0:14]
i = 0
score = np.zeros(len(last_names))
# Create scatter plots using for loop format
for name in last_names: # loop over no_points
    # Read in forecasted values for each class member
    sim_file = str(name) + '.csv'
    sim_path = os.path.join('..', '..', 'forecast_entries', sim_file)
    frcst = pd.read_csv(sim_path, index_col='Forecast #')
    oneweek = frcst['1week']
    X = obsvd.observed
    Y = oneweek
    # Create scatter plot for each person in class
    fig, ax = plt.subplots(figsize=(15, 15))
    fig.patch.set_facecolor("white")
    plot1 = ax.scatter(X, Y, c='b')
    # Create best fit line
    a, b = best_fit(X, Y)
    yfit = [a + b * xi for xi in X]
    plot2 = ax.plot(X, yfit, color='r')
    # Format plot
    ax.set(xlabel='Observed Streamflow (mm)',
           ylabel='Forecasted Streamflow (mm)')
    ax.set_title(str(name) + ' Scatter Plot', fontweight='bold')
    ax.grid('major')
    fig.tight_layout()
    plt.show()
    score[i] = i # Replace i with calc of rmse ((use hydroeval)
    i = i+1

# join w/ no point names




# %%
# Create array that holds the slopes of each person's forecasted
# values compared to the observed for this semester
# (wasn't sure how to do this automatically, so just pulled slope from
# equations printed with scatter plots)
fit_arr = np.array([0.57, 0.48, 1.02, 0.52, 0.82, 0.02, -0.01,
                    -0.02, 0.28, 0.49])
print('Best Fit Values =', fit_arr)








# Find the differences of each slope from 1
dif_arr = abs(1 - fit_arr)
print('Distance from 1 =', dif_arr)
# Compile the differences into a single dataframe with each student's name
dif_df = pd.DataFrame(dif_arr, columns=['Difference'])
bonus = pd.DataFrame(first_names, columns=['Names'])
bonus = bonus.join(dif_df)

print(no_points)
print(bonus)




# How to cut the bonus list down to just the people getting no points???
bonus_sort = bonus.sort_values('Difference')
print(bonus_sort)

bonus_results = ['Sierra', 'Gigi', 'Xueyan']








# Use eval function script to create new csv file for bonus results
ef.write_bonus(bonus_results, first_names, weeknum)
