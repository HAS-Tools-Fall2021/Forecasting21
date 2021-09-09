# This script contains the functions used for plotting different plots in
# other scripts used for evaluation.

# Author: Shweta Narkhede and Camilo Salcedo
# Created on: Oct 24th, 2020

# Edited by: Benjamin Mitchell, Quinn Hull
# Edited on: Nov 15th, 2020
# %%
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import eval_functions as ef
import seaborn as sns

# %% Functions

def get_histogram(savepath, forecasts, obs_week, week):
    """Get Histograms:
    -----------------------------------
    This function plots histograms of predicted weekly flow data and
    the count of the flow value prediction. It also plots observed weekly
    data for last week for comaparision.
    -----------------------------------
    Parameters:
    forecasts  = array
                every student's forecast for either week 1 or 2
    obs_week    = float
                provides week's observed flow
    week        = Week number for the forecast (1 or 2)
    -----------------------------------
    Outputs:
    figure of Histogram plot
    """
    fig2 = plt.figure()
    fig2.set_size_inches(8, 6)
    plt.hist(forecasts, bins=120, color='blue', alpha=0.75,
             label='Student Guesses')
    histogram = plt.plot([obs_week]*3, np.arange(0, 3, 1), color='red',
                         linestyle='-', label='Actual mean')
    title_string = 'Student guesses for Week '+str(week)
    plt.title(title_string)
    plt.xlabel('Flow Forecast (cfs)')
    plt.ylabel('Count')
    plt.legend(loc='upper left')
    fig2.patch.set_facecolor('xkcd:white')
    plt.tight_layout()
    plt.show()

    fig2.savefig(savepath)
    
    return histogram


def get_simpleplot(savepath, forecasts, obs_week, week):
    """Get Simple plot:
    ------------------------------------
    This function plots a simple line plot of student's weekly averaged
    forecast for a week
    ------------------------------------
    Parameters:
    forecasts = array
                provides weekly forecasted flow of each student
    obs_week  = float
                week's observed flow
    week = string
                Week number for the forecast (1 or 2)
    ------------------------------------
    Outputs: figure of simple line plot

    """
    # Get the array of firstnames for the plot
    firstnames = ef.getFirstNames()

    fig3, ax = plt.subplots()
    fig3.set_size_inches(10, 4)
    clean_forecasts = [x for x in forecasts if not np.isnan(x)]
    class_avg = np.mean(clean_forecasts)
    simple_plot = ax.plot(forecasts, '-g', label='Forecast', alpha=.8)
    plt.axhline(y=class_avg, linestyle='dashed',
                label='Class Avg', alpha=.8, color='red')
    plt.axhline(y=obs_week, linestyle='dotted', label='Observed',
                alpha=.8, color='blue')
    plt.xticks(ticks = np.arange(0, len(forecasts), 1), labels = firstnames, rotation = 60)
    title_string = 'Week '+str(week)+' Forecasts'
    ax.set(title=title_string, xlabel="Students",
           ylabel="Weekly Avg Flow [cfs]")
    ax.legend(fancybox=True, framealpha=1, shadow=True,
              borderpad=1)
    fig3.patch.set_facecolor('xkcd:white')
    plt.tight_layout()
    plt.show()
    
    fig3.savefig(savepath)

    return simple_plot


def plot_class_forecasts(df, week_flows, leadtime, type_plot):
    """ plot_class_forecasts()
    ---------------------------------------------------------------------
    This function plots the forecasts submitted by each student for both
    Week 1 & 2 Forecasts. In addition, is capable of plotting the absolute
    error in regards the observed value.
    ---------------------------------------------------------------------
    Parameters:
    df = Dataframe
        Includes the weekly forecast values for Week 1 and 2 for each student.
    week_flows = Dataframe
                 Observed flows per week obtained from USGS.
    leadtime: int
          leadtime for the forecast. It can only be 1 or 2
    type_plot: string
               Enter 'forecasts' to plot all submitted values, or 'abs_error'
               to plot the deviation from the observed value.
    ---------------------------------------------------------------------
    Outputs: Plot of the forecasted values or the absolute error depending the
             user input
    """

    # Request the parameters for the plots
    y_low = (input('Please introduce the lower limit for y-Axis (Hit enter for \
             default value 0):'))
    y_max = (input('Please introduce the upper limit for y-Axis (Hit enter for \
            default values):'))

    plot_weeks_inp = input('Please introduce the list of weeks to consider as \
        ["Week #", "Week #", ...]. Otherwise, if you want to include all weeks\
        hit enter:')

    if plot_weeks_inp == '':
        column_weeks = [i for i in df.columns]
    else:
        column_weeks = [i for i in df.columns if i in plot_weeks_inp]

    # Markers for the plot
    markers = ['o', 'v', '^', 'D', '>', 's', 'P', 'X', '<', '>',
               'X', 'o', 'v', 's', '^', 'P', '<', 'D', 's']

    # Get the array of firstnames for the plot
    firstnames = ef.getFirstNames()

    # Trim and set index the same weekly flow (start 8/23)
    weekly_flows = week_flows.iloc[1:len(column_weeks) + 1, 3:4]
    weekly_flows.set_index(df.columns, append=False, inplace=True)

    # Assign values depending the plot type selected
    if type_plot == 'abs_error':
        df = df.T.subtract(weekly_flows['observed'], axis=0).T
        plot_ylabel = "Deviation from Weekly Avg Flow [cfs]"
        plot_title = 'Absolute Error in '+str(leadtime) + ' Week Forecast for \n\
        HAS-Tools Class'
    elif type_plot == 'forecast':
        plot_ylabel = "Weekly Avg Flow [cfs]"
        plot_title = str(leadtime)+' Week Forecast for HAS-Tools Class \n '

    # Plotting process
    fig, ax = plt.subplots()
    ax.plot(df.T)
    for i, line in enumerate(ax.get_lines()):
        line.set_marker(markers[i])

    # Plot observed flow if the selected plot is the forecast
    if type_plot == 'forecast':
        ax.plot(column_weeks, weekly_flows['observed'], color='black',
                marker='o', linestyle='--', linewidth=3)
        plot_labels = firstnames + ['Observed Flow']
    elif type_plot == 'abs_error':
        plot_labels = firstnames

    # Format for labels and plot title
    ax.set_xlabel('Weeks \n', fontsize=13, fontweight='bold')
    ax.set_ylabel(plot_ylabel, fontsize=13, fontweight='bold')
    ax.set_title(plot_title, fontsize=15, fontweight='bold')

    # Assigns the limits for y-axis based on user's input
    if y_low == '' and y_max != '':
        ax.set_ylim(df[column_weeks].min().min(), float(y_max))
    elif y_max == '' and y_low != '':
        ax.set_ylim(float(y_low), df[column_weeks].max().max())
    elif y_max == '' and y_low == '':
        ax.set_ylim(df[column_weeks].min().min(), df[column_weeks].max().max())
    else:
        ax.set_ylim(float(y_low), float(y_max))

    ax.legend(plot_labels, loc='lower center',
              bbox_to_anchor=(.5, -0.4), ncol=6)
    fig.set_size_inches(9, 5)
    fig.patch.set_facecolor('xkcd:white')
    plt.show()


def plot_class_summary(df, week_flows, week, type_plot):
    """ plot_class_summary()
    ---------------------------------------------------------------------
    This function plots the summary for the forecasts submitted by the students
    for Week 1 & 2 Forecasts. It includes values such as the mean, median, min
    and max values, among others. It can be plotted as a box-whiskers plot or a
    regular plot.
    ---------------------------------------------------------------------
    Parameters:
    df = Dataframe
        Includes the weekly forecast values for Week 1 and 2 for each student.
    week_flows = Dataframe
                 Observed flows per week obtained from USGS.
    week: int
          The week for the forecast. It can only be 1 or 2
    type_plot: string
               Enter 'box' to plot the summary using a Box-Whiskers plot or
               'plot' to plot it as a regular plot.
    ---------------------------------------------------------------------
    Outputs: Plot showing the main properties of the forecast entries for HAS
             Tools class as a either a Box-Whiskers plot or a regular plot
             depending the user input
    """

    # Request the plotting parameters
    y_low = (input('Please introduce the lower limit for y-Axis (Hit enter for \
           default value 0):'))
    y_max = (input('Please introduce the upper limit for y-Axis (Hit enter for \
           default values):'))

    plot_weeks_inp = input('Please introduce the list of weeks to consider as \
        ["Week #", "Week #", ...]. Otherwise, if you want to include all weeks\
        hit enter:')

    if plot_weeks_inp == '':
        column_weeks = [i for i in df.columns]
    else:
        column_weeks = [i for i in df.columns if i in plot_weeks_inp]

    # Plotting process depending on the type of plot selected
    if type_plot == 'box':

        fig, ax = plt.subplots()
        # Setup of the features of the boxplot
        boxprops = dict(linestyle='-', linewidth=0.8, color='#00145A',
                        facecolor='white')
        capprops = dict(color='#00145A')
        whiskerprops = dict(color='#00145A', linestyle='--')
        medianprops = dict(linewidth=1.2, color='#E80B5F')

        # Plot boxplot and stripplot and set labels and title
        total_data = pd.melt(df[column_weeks])
        ax = sns.boxplot(x='variable', y='value', data=total_data,
                         linewidth=0.8, width=0.4, showfliers=False,
                         whiskerprops=whiskerprops, color='w', boxprops=boxprops,
                         medianprops=medianprops, capprops=capprops)
        ax = sns.stripplot(x='variable', y='value', data=total_data,
                           jitter=True, alpha=0.5)
        ax.set_ylabel('Flow (cfs)', fontsize=13, fontweight='bold')
        ax.set_xlabel('\n Weeks', fontsize=13, fontweight='bold')
        ax.set_title('Weekly Discharge Prediction for Week'+str(week)+'\n',
                     fontsize=15, fontweight='bold')

        # Assigns the limits for y-axis based on user's input
        if y_low == '' and y_max != '':
            ax.set_ylim(0, float(y_max))
        elif y_max == '' and y_low != '':
            ax.set_ylim(float(y_low), df[column_weeks].max().max())
        elif y_max == '' and y_low == '':
            ax.set_ylim(0, df[column_weeks].max().max())
        else:
            ax.set_ylim(float(y_low), float(y_max))

        # Plot mean and observed values
        ax.plot(np.mean(df[column_weeks]), linestyle='dashed', linewidth=1.5,
                marker='o', markersize=4, color='#0E6FDC',
                label='Class Average')
        ax.plot(column_weeks, week_flows['observed'][1:len(column_weeks)+1],
                color='black', marker='o', linestyle='--', markersize=4,
                label='Observed')

        # Legend
        ax.legend(loc='lower center',
                  bbox_to_anchor=(.5, -0.4), ncol=5)

    elif type_plot == 'plot':

        plt.style.use('seaborn-whitegrid')

        # Plot boxplot and stripplot and set labels and title
        ay = plt.plot(column_weeks, df[column_weeks].mean(), marker='o',
                      label='Class Average')
        ay = plt.plot(column_weeks, df[column_weeks].quantile(0.25), marker='o',
                      label='Lower Quantile')
        ay = plt.plot(column_weeks, df[column_weeks].quantile(0.75), marker='o',
                      label='Upper Quantile')
        ay = plt.plot(column_weeks, df[column_weeks].min(), marker='o',
                      label='Min')
        ay = plt.plot(column_weeks, df[column_weeks].max(), marker='o',
                      label='Max')
        ay = plt.plot(column_weeks, week_flows['observed'][1:len(column_weeks)+1], color='black', marker='o', linestyle='--',
                      label='Observed')
        plt.ylabel('Flow (cfs)', fontsize=13, fontweight='bold')
        plt.xlabel('\n Weeks', fontsize=13, fontweight='bold')
        plt.title('Weekly Discharge Prediction for Week # '+str(week)+'\n',
                  fontsize=15, fontweight='bold')

        # Assigns the limits for y-axis based on user's input
        if y_low == '' and y_max != '':
            plt.ylim(0, float(y_max))
        elif y_max == '' and y_low != '':
            plt.ylim(float(y_low), df[column_weeks].max().max())
        elif y_max == '' and y_low == '':
            plt.ylim(0, df[column_weeks].max().max())
        else:
            plt.ylim(float(y_low), float(y_max))

        # Legend
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.4), ncol=3)
        fig.patch.set_facecolor('xkcd:white')


#%%
# Week 10 Additions

def plot_seasonal_rmse(savepath, seasonal_rmse):
    """Seasonal Root Mean Square Error:
    -----------------------------------
    This function plots the root mean square error of seasonal flow
    data for week 1 to the most recent entry.
    You have the option of entering in minumum and maximum y values.
    -----------------------------------
    Parameters:
    Seasonal_rmse = pandas dataframe
                    every student's seasonal root meet square error
    -----------------------------------
    Output:
    Figure of long term weekly prediction root mean square errors
    """
    # Request the parameters for the plots
    y_low = (input('Please introduce the lower limit for y-Axis (Hit enter for \
             default value 0):'))
    y_max = (input('Please introduce the upper limit for y-Axis (Hit enter for \
            default values):'))
    column_weeks = [i for i in seasonal_rmse.columns]

    # Markers for the plot
    markers = ['o', 'v', '^', 'D', '>', 's', 'P', 'X', '<', '>',
               'X', 'o', 'v', 's', '^', 'P', '<', 'D', 's']

    # Get the array of firstnames for the plot
    firstnames = ef.getFirstNames()

    # plotting
    fig10, ax = plt.subplots()
    ax.plot(seasonal_rmse)
    for i, line in enumerate(ax.get_lines()):
        line.set_marker(markers[i])
    ax.set_xlabel('Weeks', fontsize=13, fontweight='bold')
    ax.set_ylabel("Root Mean Square Error", fontsize=13, fontweight='bold')
    ax.set_title("Seasonal Root Mean Square Error", fontsize=13,
                 fontweight='bold')

    # Assigns the limits for y-axis based on user's input
    if y_low == '' and y_max != '':
        ax.set_ylim(seasonal_rmse[column_weeks].min().min(), float(y_max))
    elif y_max == '' and y_low != '':
        ax.set_ylim(float(y_low), seasonal_rmse[column_weeks].max().max())
    elif y_max == '' and y_low == '':
        ax.set_ylim(seasonal_rmse[column_weeks].min().min(),
                    seasonal_rmse[column_weeks].max().max())
    else:
        ax.set_ylim(float(y_low), float(y_max))
    # showing the legend
    ax.legend(firstnames, loc='lower center', 
              bbox_to_anchor=(.5, -0.4), ncol=6)
    fig10.patch.set_facecolor('xkcd:white')
    plt.show()

    fig10.savefig(savepath)


def rmse_histogram(savepath, weekly_rmse):
    """Root Mean Square Error Histogram:
    -----------------------------------
    This function plots a histogram of the root mean square error
    of weekly flow data
    -----------------------------------
    Parameters:
    weekly_rmse   = pandas dataframe
                    every student's weekly root meet square error
    -----------------------------------
    Outputs:
    Histogram plot of week 1 and 2 root mean square errors
    """
    fig11 = plt.figure()
    plt.hist(weekly_rmse.iloc[:, 0], bins=20, rwidth=0.8, color='green',
             alpha=0.3, label='Week 1')
    plt.hist(weekly_rmse.iloc[:, 1], bins=20, rwidth=0.8, color='red',
             alpha=0.3, label='Week 2')
    plt.xlabel('Root Mean Square Error', fontweight='bold')
    plt.ylabel('Frequency', fontweight='bold')
    plt.title('Weekly Root Mean Square Errors', fontweight='bold')
    plt.legend()
    fig11.patch.set_facecolor('xkcd:white')
    plt.tight_layout()
    plt.show()

    fig11.savefig(savepath)


# %%
# Week 12 Additions
def noIinTEAM(savepath, class_list, obs_week, oneweek_forecasts, twoweek_forecasts, bar_width):
    # Gettting team names for data collection
    team1 = ['Adam', 'Lourdes', 'Patrick', 'Ben']
    team2 = ['Alcely', 'Shweta', 'Richard', 'Scott']
    team3 = ['Camilo', 'Diana', 'Xenia', 'Danielle']
    team4 = ['Alexa', 'Quinn', 'Abigail']
    team5 = ['Jill', 'Mekha', 'Jake']
    team_names = ['Big_Brain_Squad', 'Team_SARS', 'Aquaholics',
                  'Dell_for_the_Win?', 'Team_MJJ']
    team_tol = [*team1, *team2, *team3, *team4, *team5]

    class_pre_dict = pd.DataFrame({'oneweek_forecasts':oneweek_forecasts,
                                   'twoweek_forecasts':twoweek_forecasts},
                                   index = class_list,
                                   columns = ['oneweek_forecasts', 'twoweek_forecasts'])

    # Organizing by team name
    Big_Brain_Squad = class_pre_dict.loc[team1]
    Team_SARS = class_pre_dict.loc[team2]
    Aquaholics = class_pre_dict.loc[team3]
    Dell_for_the_Win = class_pre_dict.loc[team4]
    Team_MJJ = class_pre_dict.loc[team5]

    #Ploting time!
    x = np.arange(0, 18, 1)
    fig12 = plt.figure()
    fig12.set_size_inches(25, 8)
    ax = fig12.add_subplot()
    w = bar_width
    plt.xticks(x + w/2, team_tol, rotation = 60, fontsize=15)
    plt.yticks(fontsize=15)
    ax.bar(x[0:4], Big_Brain_Squad.oneweek_forecasts, width=w, align='center', label = 'team1')
    ax.bar(x[0:4]+w, Big_Brain_Squad.twoweek_forecasts, width=w, align='center', label = 'single1')
    ax.bar(x[4:8], Team_SARS.oneweek_forecasts, width=w, align='center', label = 'team2')
    ax.bar(x[4:8]+w, Team_SARS.twoweek_forecasts, width=w, align='center', label = 'single2')
    ax.bar(x[8:12], Aquaholics.oneweek_forecasts, width=w, align='center', label = 'team3')
    ax.bar(x[8:12]+w, Aquaholics.twoweek_forecasts, width=w, align='center', label = 'single3')
    ax.bar(x[12:15], Dell_for_the_Win.oneweek_forecasts, width=w, align='center', label = 'team4')
    ax.bar(x[12:15]+w, Dell_for_the_Win.twoweek_forecasts, width=w, align='center', label = 'single4')
    ax.bar(x[15:18], Team_MJJ.oneweek_forecasts, width=w, align='center', label = 'team5')
    ax.bar(x[15:18]+w, Team_MJJ.twoweek_forecasts, width=w, align='center', label = 'single5')
    ax.axhline(y=obs_week, linewidth=2, linestyle = '--', color='k')
    plt.xlabel('Student', fontsize=15)
    plt.ylabel('Average Flow', fontsize=15)
    ax.legend( loc='lower center', fontsize=20,
              bbox_to_anchor=(.5, -0.4), ncol=5)
    plt.text(0.7, obs_week, 'Observed Flow', fontsize=21)
    fig12.patch.set_facecolor('xkcd:white')
    plt.tight_layout()
    plt.show()

    fig12.savefig(savepath)


def last_2_weeks(savepath, obs_week, oneweek_forecasts, twoweek_forecasts, bar_width):
      
    # Get the array of firstnames for the plot
    firstnames = ef.getFirstNames()
    class_forecasts = pd.DataFrame({'oneweek_forecasts':oneweek_forecasts,
                                     'twoweek_forecasts':twoweek_forecasts},
                                     index = firstnames,
                                     columns = ['oneweek_forecasts', 'twoweek_forecasts'])
    
    stu = np.arange(0, 19, 1)
    fig13 = plt.figure()
    fig13.set_size_inches(25, 8)
    ax = fig13.add_subplot()
    w = bar_width
    plt.xticks(stu + w/2, firstnames, rotation = 60, fontsize=15)
    ax.bar(stu, class_forecasts.oneweek_forecasts, width=w, align='center', label = 'week1')
    ax.bar(stu+w, class_forecasts.twoweek_forecasts, width=w, align='center', label = 'week2')
    ax.axhline(y=obs_week, linewidth=2, linestyle = '--', color='k')
    plt.xlabel('Student', fontsize=15)
    plt.ylabel('Average Flow', fontsize=15)
    ax.legend( loc='lower center', fontsize=20,
              bbox_to_anchor=(.5, -0.4), ncol=5)
    plt.text(0.7, obs_week, 'Observed Flow', fontsize=21)
    fig13.patch.set_facecolor('xkcd:white')
    plt.tight_layout()
    plt.show()

    fig13.savefig(savepath)

    
def last_2_weeks_diff(savepath, obs_week, oneweek_forecasts, twoweek_forecasts, bar_width):
      
    # Get the array of firstnames for the plot
    firstnames = ef.getFirstNames()
    class_forecasts = pd.DataFrame({'oneweek_forecasts':oneweek_forecasts,
                                  'twoweek_forecasts':twoweek_forecasts},
                                   index = firstnames,
                                   columns = ['oneweek_forecasts', 'twoweek_forecasts'])

    class_forecasts.insert(2, 'Diff_1', np.array(class_forecasts['oneweek_forecasts'] - obs_week), True)
    class_forecasts.insert(3, 'Diff_2', np.array(class_forecasts['twoweek_forecasts'] - obs_week), True)
    
    # Plotting Diff
    stu = np.arange(0, 19, 1)
    fig14 = plt.figure()
    fig14.set_size_inches(25, 8)
    ax = fig14.add_subplot()
    w = bar_width
    plt.xticks(stu + w/2, firstnames, rotation = 60, fontsize=15)
    ax.bar(stu, class_forecasts.Diff_1, width=w, align='center', label = 'week1')
    ax.bar(stu+w, class_forecasts.Diff_2, width=w, align='center', label = 'week2')
    ax.axhline(y=0, linewidth=2, linestyle = '--', color='k')
    plt.xlabel('Student', fontsize=15)
    plt.ylabel('Average Flow', fontsize=15)
    ax.legend( loc='lower center', fontsize=20,
              bbox_to_anchor=(.5, -0.4), ncol=5)
    # plt.text(0, 0, 'Observed Flow', fontsize=21)
    fig14.patch.set_facecolor('xkcd:white')
    plt.tight_layout()
    plt.show()

    fig14.savefig(savepath)


# %%
