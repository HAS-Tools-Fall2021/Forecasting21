# %%
import numpy as np
import pandas as pd
import datetime
import os
import json 
import urllib.request as req
import urllib
# %%
# East of Cottonwood
# Link: https://daymet.ornl.gov/single-pixel/

cottonwood_url = "https://daymet.ornl.gov/single-pixel/api/data?lat=34.7525&lon=-111.9058&vars=dayl,prcp,srad,swe,tmax,tmin,vp&format=json"
response = req.urlopen(cottonwood_url)
responseDict = json.loads(response.read())
responseDict['data'].keys()
year = responseDict['data']['year']
yearday = responseDict['data']['yday']
precip = responseDict['data']['prcp (mm/day)']

#make a dataframe from the data
data = pd.DataFrame({'year': year,
                     'yearday': yearday, "precip": precip})

data.drop(data[data['year']<1989].index,inplace=True)

data["year"] = data['year'].astype(int)
data['yearday'] = data['yearday'].astype(int)

data.drop(data[data['year']<1989].index,inplace=True)

#Datetime
data['datetime'] = data['year'].astype(str)+data['yearday'].astype(str)
data.set_index(data.index-3285, inplace=True)

for i in np.arange(0, 11680):
    temporary = datetime.datetime.strptime(data['datetime'][i], "%Y%j").strftime("%Y-%m-%d")
    data["datetime"][i] = datetime.datetime.strptime(temporary, "%Y-%m-%d")

data['datetime']
data.set_index(data['datetime'], inplace=True)
data.drop(columns=['datetime', 'year', 'yearday'], inplace=True)
data.columns = ['prcp']

# %%
# Near the Forecast Site
forecast_url = "https://daymet.ornl.gov/single-pixel/api/data?lat=34.448&lon=-111.789" \
       "&vars=prcp&years=&format=csv"
data1 = pd.read_table(forecast_url, delimiter=',', skiprows=6)

# Drop data before 1989 so we can match the time with USGS streamflow data
data1.drop(data1[data1['year']<1989].index,inplace=True)

# Generate datetime and set it as data.index
data1['datetime'] = data1['year'].astype(str)+data1['yday'].astype(str)
data1.set_index(data1.index-3285, inplace=True)

for ii in np.arange(0,11680):
     temp = datetime.datetime.strptime(data1['datetime'][ii], '%Y%j').strftime('%Y-%m-%d')
     data1['datetime'][ii] = datetime.datetime.strptime(temp, '%Y-%m-%d')

data1['datetime']
data1.set_index(data1['datetime'], inplace=True)
data1.drop(columns=['datetime', 'year', 'yday'], inplace=True)
data1.columns = ['prcp']

# Generate weekly time series for prcp and streamflow during 1989-2020
W_prcp = data1.resample('W').mean()

# %%
