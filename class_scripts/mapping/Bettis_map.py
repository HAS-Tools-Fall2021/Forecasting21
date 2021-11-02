# %%
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import geopandas as gpd
import fiona
from shapely.geometry import Point
import contextily as ctx
import os

# %%
# Lesson 1 from Earth Data Science:
# https://www.earthdatascience.org/courses/use-data-open-source-python/intro-vector-data-python/spatial-data-vector-shapefiles/
# Vector data comes in 3 forms:
#       - point, line and polygon

#  Gauges II USGS stream gauge dataset:
# Download here:
# https://water.usgs.gov/GIS/metadata/usgswrd/XML/gagesII_Sept2011.xml#stdorder

# Reading it using geopandas
file = os.path.join('/Users/sierra/Desktop/Desktop - Sierra’s MacBook Pro/Fall 2021/HASTools/homework-sbettis319/data/gagesII_9322_point_shapefile')
gages = gpd.read_file(file)

# Lets checkout what we just got:
# This is basically just a regular pandas dataframe but it has geometry
type(gages)
gages.head()
gages.columns
gages.shape  # Seeing how many entries there are

# Can see the geometry type of each row like this:
gages.geom_type
# can see the projection here
gages.crs
# And the total spatial extent like this:
gages.total_bounds


# %%
# Now to plot:
fig, ax = plt.subplots(figsize=(10, 10))
gages.plot(ax=ax)
plt.show()

# For now lets just plot a subset of them
# see what the state column contains
gages.STATE.unique()
gages_AZ = gages[gages['STATE'] == 'AZ']
gages_AZ.shape

# Plot our subset
fig, ax = plt.subplots(figsize=(10, 10))
gages_AZ.plot(ax=ax)
plt.show()

# Could plot by some other variable:
fig, ax = plt.subplots(figsize=(10, 10))
gages_AZ.plot(column='LAT_GAGE', categorical=False,
                legend=True, markersize=45, cmap='OrRd', ax=ax)
ax.set_title("Arizona stream gauge latitudes")
plt.show()

# Other cmap options - 'set2', 'OrRd'

# %%
# Now look for other datasets here:
# https://www.usgs.gov/core-science-systems/ngp/national-hydrography/access-national-hydrography-products
# https://viewer.nationalmap.gov/basic/?basemap=b1&category=nhd&title=NHD%20View


# Example reading in a geodataframe
file = os.path.join('/Users/sierra/Desktop/Desktop - Sierra’s MacBook Pro/Fall 2021/HASTools/homework-sbettis319/data/Shape')
fiona.listlayers(file)
HU8 = gpd.read_file(file, layer="WBDHU8")


# Check the type and see the list of layers
type(HU8)
HU8.head()

# Then we can plot just one layer at atime
fig, ax = plt.subplots(figsize=(10, 10))
HU8.plot(ax=ax)
ax.set_title("HUC Boundaries")
plt.show()

# %%
# POINTS NOT LINING UP?
# Add some points
## Payson:  32.230869, -111.325134
# Phoenix : 33.448376, -112.074036
# Stream gauge:  34.44833333, -111.7891667
point_list = np.array([[-112.0740, 33.4484], [-111.7891667, 34.44833333]])
# Make these into spatial features
point_geom = [Point(xy) for xy in point_list]

# Map a dataframe of these points
point_df = gpd.GeoDataFrame(point_geom, columns=['geometry'],
                            crs=HU8.crs)

# Plot these on the first dataset
# Then we can plot just one layer at atime
fig, ax = plt.subplots(figsize=(10, 10))
HU8.plot(ax=ax)
point_df.plot(ax=ax, color='black', marker='s')
ax.set_title("HUC Boundaries")
plt.show()

# %%
# Now put it all together on one plot
HU8_project = HU8.to_crs(gages_AZ.crs)
points_project = point_df.to_crs(gages_AZ.crs)
# Now plot again
fig, ax = plt.subplots(figsize=(5, 5))
gages_AZ.plot(column='LAT_GAGE', categorical=False,
              legend=True, markersize=15, cmap='Set1',
              ax=ax)
points_project.plot(ax=ax, color='black', marker='o')
HU8_project.boundary.plot(ax=ax, color=None,
                           edgecolor='blue', linewidth=0.5)

# %%
# Some other basemap choices:
#  https://towardsdatascience.com/free-base-maps-for-static-maps-using-geopandas-and-contextily-cd4844ff82e1
# Plot the gages, watershed, points, and map

fig, ax = plt.subplots(figsize=(5, 5))
gages_AZ.plot(column='LAT_GAGE', categorical=False,
              legend=True, legend_kwds={'label': r'Lat and Longitude'},
              markersize=15, cmap='Set1', ax=ax)
points_project.plot(ax=ax, color='black', marker='D',
                    label ="Stream Gauge, Payson, Phoenix (N-S)")
HU8_project.boundary.plot(ax=ax, color=None,
                edgecolor='blue',linewidth=0.5,
                label="AZ Watershed boundary")
ctx.add_basemap(ax, crs=gages_AZ.crs)
ax.set(title ='AZ points, lines, and projection', xlabel ='latitude',
                ylabel ='longitude')
ax.legend()
fig.savefig("Sub-basin AZ")
# %%
# Converting the previous map to lat and longitude by projecting 
# everything to the HU8 crs
gages_project = gages_AZ.to_crs(HU8.crs)
fig, ax = plt.subplots(figsize=(10, 10))
gages_project.plot(column='LAT_GAGE', categorical=False,
              legend=True, legend_kwds={'label': r'Lat and Longitude'},
              markersize=15, cmap='Set1', ax=ax)
point_df.plot(ax=ax, color='black', marker='D',
                    label ="Stream Gauge and Phoenix (N-S)")
HU8.boundary.plot(ax=ax, color=None,
                edgecolor='blue',linewidth=0.5,
                label="AZ Watershed boundary")
ctx.add_basemap(ax, crs=HU8.crs)
ax.set(title ='AZ points, lines, and projection', xlabel ='latitude',
                ylabel ='longitude')
ax.legend()
fig.savefig("Sub-basin AZ")
# %%
