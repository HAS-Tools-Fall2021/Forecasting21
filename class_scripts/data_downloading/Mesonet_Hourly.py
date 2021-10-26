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