# @Date:   2021-10-26T09:07:24-07:00
# @Last modified time: 2021-10-26T09:10:36-07:00



# %%
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

import dataretrieval.nwis as nwis
import json
import urllib.request as req
import urllib

# %%
# Read in data process

mytoken = [] # enter token here
base_url = "http://api.mesowest.net/v2/stations/timeseries"

# Specify arguments for API string
args = {
    'start': '199701010000',
    'end': '202110230000',
    'obtimezone': 'UTC',
    'vars': 'precip_accum_24_hour',
    'stids': 'KPRC',
    'units': 'temp|F,precip|mm',
    'token': mytoken}

# Connect arguments into single string
apiString = urllib.parse.urlencode(args)

# Add the API string to the base_url
fullUrl = base_url + '?' + apiString

# Generate API response
response = req.urlopen(fullUrl)

# Read the response into Python dictionary
responseDict = json.loads(response.read())

# Define variables using .keys() method to find relevant data
kprc_var = 'precip_accum_24_hour_set_1'
header = 'Precipitation'

dateTime = responseDict['STATION'][0]['OBSERVATIONS']['date_time']
precip_accum = responseDict['STATION'][0]['OBSERVATIONS'][kprc_var]

# Combine into Pandas DataFrame
data = pd.DataFrame({header: precip_accum},
                    index=pd.to_datetime(dateTime))

# Convert into weekly mean
data_weekly = data.resample('W').mean()
data_weekly = data_weekly.fillna(0)

# %%
