# %%
import os
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json 
import urllib.request as req
import urllib

# %%
#Sierra:

mytoken = '2937e314803a4e31b8423f6b5da86644'

# This is the base url that will be the start our final url
base_url = "http://api.mesowest.net/v2/stations/timeseries"

# Specific arguments for Montezuma Castle near Camp Verde
args = {
    'start': '200001014000',
    'end': '202110230000',
    'obtimezone': 'UTC',
    'vars': 'air_temp',
    'stids': 'MCZA3',
    'units': 'precip|mm',
    'token': mytoken}
# Takes your arguments and paste them together
# Into a string for the api
# (Note you could also do this by hand, but this is better)
apiString = urllib.parse.urlencode(args)
print(apiString)

# Add the API string to the base_url
fullUrl = base_url + '?' + apiString
print(fullUrl)

# Now we are ready to request the data
response = req.urlopen(fullUrl) 
responseDict = json.loads(response.read())
dateTime = responseDict['STATION'][0]['OBSERVATIONS']['date_time']
precip = responseDict['STATION'][0]['OBSERVATIONS']['precip_accum_1']

precip_data = pd.DataFrame({'Precipitation (mm)': precip},
                           index=pd.to_datetime(dateTime))

# Now we can combine this into a pandas dataframe
data = pd.DataFrame({'Precipitation': precip}, index=pd.to_datetime(dateTime))

# -----------------------------------------

# Connal:

base_url = "http://api.mesowest.net/v2/stations/timeseries"

# Specific arguments for the data that we want
args = {
    'start': '200611200000',
    'end': '201911070000',
    'obtimezone': 'UTC',
    'vars': 'precip_accum_one_hour',
    'stids': 'VDCA3',
    'units': 'precip|mm',
    'token': mytoken}

# Takes your arguments and paste them together
# into a string for the api
# (Note you could also do this by hand, but this is better)
apiString = urllib.parse.urlencode(args)
print(apiString)

# add the API string to the base_url
fullUrl = base_url + '?' + apiString
print(fullUrl)

# Now we are ready to request the data
# this just gives us the API response... not very useful yet
response = req.urlopen(fullUrl)

# What we need to do now is read this data
# The complete format of this
responseDict = json.loads(response.read())

# This creates a dictionary for you
# The complete format of this dictonary is descibed here:
# https://developers.synopticdata.com/mesonet/v2/getting-started/
# Keys shows you the main elements of your dictionary
responseDict.keys()
# You can inspect sub elements by looking up any of the keys in the dictionary
responseDict['UNITS']
responseDict['QC_SUMMARY']
responseDict['STATION']
responseDict['SUMMARY']
# Each key in the dictionary can link to differnt data structures
# For example 'UNITS is another dictionary'
type(responseDict['UNITS'])
responseDict['UNITS'].keys()
responseDict['UNITS']['position']

# where as STATION is a list
type(responseDict['STATION'])
# If we grab the first element of the list that is a dictionary
type(responseDict['STATION'][0])
# And these are its keys
responseDict['STATION'][0].keys()

# Long story short we can get to the data we want like this:
dateTime = responseDict['STATION'][0]['OBSERVATIONS']['date_time']
precip = responseDict['STATION'][0]['SENSOR_VARIABLES']['precip_accum_one_hour']

# Now we can combine this into a pandas dataframe
data = pd.DataFrame({'ACCUMULATION': precip}, index=pd.to_datetime(dateTime))

# Now convert this to daily data using resample
data_daily = data.resample('D').mean()
