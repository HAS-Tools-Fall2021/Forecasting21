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
# Link: https://apps.nationalmap.gov/downloader/#/
# USGS National Hydrography Dataset Plus High Resolution (NHDPlus HR) for 4-digit Hydrologic Unit - 1506 (published 20180813)

# Open the files from my computer
file = os.path.join('../data/NHDPLUS_H_1506_HU4_GDB', 'NHDPLUS_H_1506_HU4_GDB.gdb')
fiona.listlayers(file)
HUC6 = gpd.read_file(file, layer="WBDHU6") # Grab the layer we want

# %%
# Plots the watershed area from above^^
fig, ax = plt.subplots(figsize=(10, 10))
HUC6.plot(ax=ax)
ax.set_title("HUC Boundaries")
plt.show()

# %%
# Adding specific points to the map
# Phoenix coords: 33.4484, -112.0740
# Stream gauge:  34.44833333, -111.7891667
# Flagstaff coords: 35.1983, -111.6513

# First make a numpy array
coords = np.array([[-112.0740, 33.4484], [-111.7891667, 34.44833333], [-111.6513, 35.1983]])
point_geo = [Point(xy) for xy in coords]
point_df = gpd.GeoDataFrame(point_geo, columns=['geometry'],
                            crs=HUC6.crs) # Add into a dataframe

# New plot with the points added
fig, ax = plt.subplots(figsize=(10, 10))
HUC6.plot(ax=ax)
point_df.plot(ax=ax, color='black', marker='x')
ax.set_title("HUC Boundaries")
plt.show()

# %%
# Gages (same that Dr. Condon used)
# https://water.usgs.gov/GIS/metadata/usgswrd/XML/gagesII_Sept2011.xml#stdorder 
file2 = os.path.join("../data/gagesII_9322_point_shapefile", 'gagesII_9322_sept30_2011.shp')
gages = gpd.read_file(file2)

# %%
# Plots the gages on the map (but not on the watershed) and also adds the points from above
gages.STATE.unique()
gages_AZ=gages[gages['STATE']=='AZ']
gages_AZ.shape

points_project = point_df.to_crs(gages_AZ.crs)
fig, ax = plt.subplots(figsize=(5, 5))
gages_AZ.plot(column='DRAIN_SQKM', categorical=False,
              legend=True, markersize=45, cmap='Set2',
              ax=ax)
points_project.plot(ax=ax, color='black', marker='x')

# %%
# Plots the gages, the watershed, the points, and a map
HUC6_project = HUC6.to_crs(gages_AZ.crs)

fig, ax = plt.subplots(figsize=(5, 5))
gages_AZ.plot(column='DRAIN_SQKM', categorical=False,
              legend=True, markersize=25, cmap='Set1',
              ax=ax)
points_project.plot(ax=ax, color='black', marker='x', label="N to S, Flagstaff, Our Stream Gage, Phoenix",)
HUC6_project.boundary.plot(ax=ax, color=None,
                           edgecolor='dimgray', linewidth=0.75, label="Watershed boundry")
ctx.add_basemap(ax, crs=gages_AZ.crs)
ax.legend()
fig.savefig("Watershed")

# %%
