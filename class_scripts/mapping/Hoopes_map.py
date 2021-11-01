# %%
import os
import matplotlib.pyplot as plt
# import matplotlib as mpl
# import pandas as pd
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
file = os.path.join('Map_Data', 'gagesII_9322_point_shapefile',
                    'gagesII_9322_sept30_2011.shp')
gages = gpd.read_file(file)

# Get data just from the state of Arizona
gages_AZ = gages[gages['STATE'] == 'AZ']
gages_AZ.shape
gages_AZ.head()

# Plot our subset
fig, ax = plt.subplots(figsize=(10, 10))
gages_AZ.plot(ax=ax)
plt.show()

# %%
# Could plot by some other variable:
fig, ax = plt.subplots(figsize=(10, 10))
gages_AZ.plot(column='DRAIN_SQKM', categorical=False,
              legend=True, markersize=45, cmap='cividis',
              ax=ax)
ax.set_title("Arizona stream gauge drainge area\n (sq km)")
plt.show()

# %%
# Now look for other datasets here:
# https://www.usgs.gov/core-science-systems/ngp/national-hydrography/access-national-hydrography-products
# https://viewer.nationalmap.gov/basic/?basemap=b1&category=nhd&title=NHD%20View


# Example reading in a geodataframe
file = os.path.join('Map_Data', 'WBD_15_HU2_GDB', 'WBD_15_HU2_GDB.gdb')
fiona.listlayers(file)
HUC4 = gpd.read_file(file, layer="WBDHU4")


# Check the type and see the list of layers
# Isolate HUC4 basin of interest (Salt River, includes verde)
type(HUC4)
HUC4.head()
HUC4 = HUC4.set_index('name')
saltverde = HUC4.loc[['Salt']]

# %%
# Add some points corresponding with those used in forecast
# PSR: 34.6501, -112.4283
# FGZ: 35.1403, -111.6710
# Daymet Data:  34.5582, -111.8591
# Stream gauge:  34.44833333, -111.7891667
point_list = np.array([[-112.4283, 34.6501],
                       [-111.6710, 35.1403],
                       [-111.8591, 34.5582],
                       [-111.7891667, 34.44833333]])

# Convert these into spatial features, make a geodataframe
point_geom = [Point(xy) for xy in point_list]
point_geom
point_df = gpd.GeoDataFrame(point_geom, columns=['geometry'],
                            crs=HUC4.crs)

# %%
# Plot these on the first dataset, one layer at a time
fig, ax = plt.subplots(figsize=(10, 10))
saltverde.plot(ax=ax)
point_df.plot(ax=ax, color='crimson')
ax.set_title("Salt River HUC4 Boundaries")
plt.show()

# %%
# Get Arizona River data from
# https://uair.library.arizona.edu/item/292543/browse-data/Water
file = os.path.join('Map_Data', 'Major_Rivers', 'Major_Rivers.shp')
rivers = gpd.read_file(file)

# %%
# Some words on projections
# Lesson 2
# https://www.earthdatascience.org/courses/use-data-open-source-python/intro-vector-data-python/spatial-data-vector-shapefiles/intro-to-coordinate-reference-systems-python/

# Note this is a different projection system than the stream gauges
# CRS = Coordinate Reference System
saltverde.crs
gages.crs
rivers.crs

# The points won't show up in AZ because they are in a different projection
# We need to project them first
# points_project = point_df.to_crs(gages_AZ.crs)

# NOTE: .to_crs() will only work if your original spatial object has a CRS
# assigned to it AND if that CRS is the correct CRS!

# Now put it all together on one plot, clip to limit extent to Salt River
gages_project = gages_AZ.to_crs(saltverde.crs)
gages_project = gpd.clip(gages_project, saltverde)
river_project = rivers.to_crs(saltverde.crs)
river_project = gpd.clip(river_project, saltverde)

# %%
# Now plot again
fig, ax = plt.subplots(figsize=(5, 5))
gages_project.plot(column='DRAIN_SQKM', categorical=False,
                   legend=True, markersize=25, cmap='cividis',
                   ax=ax)
river_project.plot(ax=ax, color='blue')
point_df.plot(ax=ax, color='crimson')
saltverde.boundary.plot(ax=ax, color=None,
                        edgecolor='black', linewidth=1)
ax.set(title="Salt River Basin", xlabel="Longitude",
       ylabel="Latitude")
plt.show()

# %%
# Adding a basemap:
# Some other basemap choices:
#  https://towardsdatascience.com/free-base-maps-for-static-maps-using-geopandas-and-contextily-cd4844ff82e1

# Now plot again
fig, ax = plt.subplots(figsize=(10, 10))
gages_project.plot(column='DRAIN_SQKM', categorical=False,
                   legend=True, markersize=25, cmap='cividis',
                   ax=ax)
river_project.plot(ax=ax, color='blue')
point_df.plot(ax=ax, color='crimson')
saltverde.boundary.plot(ax=ax, color=None,
                        edgecolor='black', linewidth=1)
ax.set(title="Salt River Basin Drainage (km^2)", xlabel="Longitude",
       ylabel="Latitude")
ctx.add_basemap(ax, crs=saltverde.crs)
plt.show()
fig.savefig('streamflow_map.png')
