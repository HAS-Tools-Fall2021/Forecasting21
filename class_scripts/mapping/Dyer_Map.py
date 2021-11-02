# %%
import matplotlib.pyplot as plt
import matplotlib as mpl 
import pandas as pd 
import numpy as np
import geopandas as gpd
import fiona
from shapely.geometry import Point
import contextily as ctx

# %%
# Lesson 1 from Earth Data Science: 
# https://www.earthdatascience.org/courses/use-data-open-source-python/intro-vector-data-python/spatial-data-vector-shapefiles/
# Vector data comes in 3 forms:
#       - point, line and polygon 

#  Gauges II USGS stream gauge dataset:
# Download here: 
# https://water.usgs.gov/GIS/metadata/usgswrd/XML/gagesII_Sept2011.xml#stdorder

# Reading it using geopandas
file = os.path.join('..','..', 'data',"gagesII_9322_point_shapefile",
                    'gagesII_9322_sept30_2011.shp')
gages = gpd.read_file(file)

# Lets checkout what we just got: 
# This is basically just a regular pandas dataframe but it has geometry
type(gages)
gages.head()
gages.columns
gages.shape #seeing how many entries there are

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
gages_AZ=gages[gages['STATE']=='AZ']
gages_AZ.shape

#plot our subset
fig, ax = plt.subplots(figsize=(10, 10))
gages_AZ.plot(ax=ax)
plt.show()

# Could plot by some other variable: 
fig, ax = plt.subplots(figsize=(10, 10))
gages_AZ.plot(column='DRAIN_SQKM', categorical=False, 
                legend=True, markersize=45, cmap='YlOrRd',
                ax=ax)
ax.set_title("Arizona stream gauge drainge area\n (sq km)")
plt.show()

#other cmap options - 'set2', 'OrRd'

# %%
# Now look for other datasets here: 
# https://www.usgs.gov/core-science-systems/ngp/national-hydrography/access-national-hydrography-products
# https://viewer.nationalmap.gov/basic/?basemap=b1&category=nhd&title=NHD%20View


# Example reading in a geodataframe
file = os.path.join('..','..', 'data', 'NHDPLUS_H_1506_HU4_GDB.gdb')
fiona.listlayers(file)
HUC6 = gpd.read_file(file, layer="WBDHU6")


#Check the type and see the list of layers
type(HUC6)
HUC6.head()

#Then we can plot just one layer at atime
fig, ax = plt.subplots(figsize=(10, 10))
HUC6.plot(ax=ax)
ax.set_title("HUC Boundaries")
plt.show()

# %%

# Add some points
# UA:  32.22877495, -110.97688412
# Stream gauge:  34.44833333, -111.7891667
# Also added the coordinates for the stream gauges I used last HW in /
# Flagstaff and Sedona
point_list = np.array([[-110.97688412, 32.22877495],
                       [-111.7891667, 34.44833333],
                       [-111.7884475, 34.8485892],
                       [-111.6692414, 35.1403158]])
#make these into spatial features
point_geom = [Point(xy) for xy in point_list]
point_geom

#mape a dataframe of these points
point_df = gpd.GeoDataFrame(point_geom, columns=['geometry'],
                            crs=HUC6.crs)


# plot these on the first dataset 
#Then we can plot just one layer at atime
fig, ax = plt.subplots(figsize=(10, 10))
HUC6.plot(ax=ax)
point_df.plot(ax=ax, color='red', marker='*')
ax.set_title("HUC Boundaries")
plt.show()

# %%
# Some words on projections
# Lesson 2 
# https://www.earthdatascience.org/courses/use-data-open-source-python/intro-vector-data-python/spatial-data-vector-shapefiles/intro-to-coordinate-reference-systems-python/

# Note this is a difernt projection system than the stream gauges
# CRS = Coordinate Reference System
HUC6.crs
gages.crs


# Lets plot with more information this time:
fig, ax = plt.subplots(figsize=(5, 5))
gages_AZ.plot(column='DRAIN_SQKM', categorical=False,
              legend=True, markersize=45, cmap='Set2',
              ax=ax)
point_df.plot(ax=ax, color='r', marker='*')

# The points aren't showing up in AZ because they are in a different project
# We need to project them first
points_project = point_df.to_crs(gages_AZ.crs)
# NOTE: .to_crs() will only work if your original spatial object has a CRS assigned 
# to it AND if that CRS is the correct CRS!

# Now plot again
fig, ax = plt.subplots(figsize=(5, 5))
gages_AZ.plot(column='DRAIN_SQKM', categorical=False,
              legend=True, markersize=45, cmap='Set2',
              ax=ax)
points_project.plot(ax=ax, color='black', marker='D')


# %%
# Now put it all together on one plot
HUC6_project = HUC6.to_crs(gages_AZ.crs)


# Now plot again
fig, ax = plt.subplots(figsize=(5, 5))
gages_AZ.plot(column='DRAIN_SQKM', categorical=False,
              legend=True, markersize=25, cmap='Set2',
              ax=ax)
points_project.plot(ax=ax, color='black', marker='x')
HUC6_project.boundary.plot(ax=ax, color=None, 
                           edgecolor='black', linewidth=1)



# %%
# Adding a basemap:
# Some other basemap choices:
#  https://towardsdatascience.com/free-base-maps-for-static-maps-using-geopandas-and-contextily-cd4844ff82e1
HUC6_project = HUC6.to_crs(gages_AZ.crs)


# My Final Map Plot
# Used 'terrain' color map because I believe it was the most visually /
# distinguishable. Colored my data points red and made them 'X's to stand out./
# I couldn't get the basemap to change, however. No matter what I chose It /
# always came out looking the same.
fig, ax = plt.subplots(figsize=(7, 10))
gages_AZ.plot(column='DRAIN_SQKM', categorical=False,
              legend=True, markersize=25, cmap='terrain',
              ax=ax)
points_project.plot(ax=ax, color='red', marker='X')
HUC6_project.boundary.plot(ax=ax, color=None,
                           edgecolor='black', linewidth=.3)
ctx.add_basemap(ax, crs=gages_AZ.crs, source = ctx.providers.Stamen.Terrain)
fig.savefig("AZ_Watershed")

# %%
