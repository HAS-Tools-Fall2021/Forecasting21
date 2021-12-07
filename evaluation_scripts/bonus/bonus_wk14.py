# %%
# Add imports
import sys
sys.path.insert(1, '../')
import eval_functions as ef
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# %%
# Name: Connal Boyd
# Description: Assigning bonus points to the first 3 people
# who's forecasts were most accurate to the observed flow from week to week
# based on the lowest calculated RMSE value for each student

weeknum = 14

first_names = ef.getFirstNames()
print(first_names)

last_names = ef.getLastNames()
print(last_names)

# %%
# Read data in from week 14 results file
week14 = pd.read_csv('../../weekly_results/forecast_week14_results.csv')
forecast = week14[['1week_points', '2week_points']].to_numpy()

# %%
# List of all of the students that got points over both weeks
points = []
for i in range(len(forecast)):
    if forecast[i, 0] > 0 or forecast[i, 1] > 0:
        points.append(last_names[i])
print('People already receiving points:', points)

# List of students that did not get points
no_points = []
for name in last_names:
    if name not in points:
        no_points.append(name)
print('People not yet receiving points:', no_points)

# %%
# Create best fit line function for use in plotting scatter plots


def best_fit(X, Y):
    """ Reference material for this function can be found at the following link:
    https://stackoverflow.com/questions/22239691/code-for-best-fit-straight-line-of-a-scatter-plot-in-python
    
    """
    xbar = sum(X)/len(X)
    ybar = sum(Y)/len(Y)
    n = len(X)

    numer = sum([xi*yi for xi, yi in zip(X, Y)]) - n * xbar * ybar
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


# Initialize RMSE scoring criteria to use in for loop
i = 0
score = np.zeros(6)

# Create scatter plots using for loop format
for name in no_points:
    # Read in forecasted values for each class member
    sim_file = str(name) + '.csv'
    sim_path = os.path.join('..', '..', 'forecast_entries', sim_file)
    frcst = pd.read_csv(sim_path, index_col='Forecast #')
    oneweek = frcst['1week']
    X = obsvd.observed
    Y = oneweek
    # Create scatter plot for each person in no_points list
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
    i = i+1
    score[i] = np.sqrt((np.mean((Y - X) ** 2)))

# Create dataframes for both RMSE values and student last names
rmse_vals = pd.DataFrame(score[1:6], columns=['RMSE Value'])
last_name_df = pd.DataFrame(no_points, columns=['Last Name'])
# Merge these two dataframes into one dataframe
two_df = last_name_df.join(rmse_vals)

# Add first names to dataframe
nopoints_first = []
for i in range(len(forecast)):
    if forecast[i, 0] == 0 and forecast[i, 1] == 0:
        nopoints_first.append(first_names[i])
# print('People eligible for bonus points:', nopoints_first)
first_name_df = pd.DataFrame(nopoints_first, columns=['First Name'])

# Join all the dataframes
rmse_names = first_name_df.join(two_df)

# Sort the joined dataframe to find the lowest three RMSE values
rmse_sort = rmse_names.sort_values(by='RMSE Value')
bonus = rmse_sort.head(4)
print(bonus)

# Award bonus points to three students with lowest RMSE values
bonus_results = [bonus.iloc[0, 0], bonus.iloc[2, 0], bonus.iloc[3, 0]]
print('Bonus point winners are:', bonus_results)

# Use eval function script to create new csv file for bonus results
ef.write_bonus(bonus_results, first_names, weeknum)
