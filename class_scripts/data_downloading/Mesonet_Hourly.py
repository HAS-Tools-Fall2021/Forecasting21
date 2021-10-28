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

mytoken = '2937e314803a4e31b8423f6b5da86644' # Insert your token here
base_url = "http://api.mesowest.net/v2/stations/timeseries"
# Specific arguments for the data that we want
args = {
    'start': '201901010000',
    'end': '202001010000',
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
responseDict['STATION'][0].keys()
responseDict['STATION'][0]['PERIOD_OF_RECORD']
responseDict['STATION'][0]['OBSERVATIONS'].keys()

# Long story short we can get to the data we want like this:
dateTime = responseDict['STATION'][0]['OBSERVATIONS']['date_time']
precip = responseDict['STATION'][0]['OBSERVATIONS']['precip_accum_one_hour_set_1']

# Now we can combine this into a pandas dataframe
data = pd.DataFrame({'ACCUMULATION': precip}, index=pd.to_datetime(dateTime))

# Now convert this to daily data using resample
data_daily = data.resample('D').mean()

# %%