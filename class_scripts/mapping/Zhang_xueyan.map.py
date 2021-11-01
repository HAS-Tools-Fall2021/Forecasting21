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
# Gauges II USGS stream gauge dataset:
# Download here: 
# https://water.usgs.gov/GIS/metadata/usgswrd/XML/gagesII_Sept2011.xml#stdorder

# Reading it using geopandas
file = os.path.join('..', '..', '..', 'homework-XUEYANZZZ', 'data', 'gagesII_9322_point_shapefile', 'gagesII_9322_sept30_2011.shp')
gages = gpd.read_file(file)

# Lets checkout what we just got: 
# This is basically just a regular pandas dataframe but it has geometry
type(gages)
gages.head()
gages.columns
gages.shape #seeing how many entries there are
gages.geom_type
gages.crs
gages.total_bounds

# %% Plot
# Select gages in AZ using column filter
gages.STATE.unique()
gages_AZ = gages[gages['STATE'] == 'AZ']
gages_AZ.shape

# Plot gages in AZ
fig, ax = plt.subplots(figsize=(10, 10))
gages_AZ.plot(column='DRAIN_SQKM', categorical=False,
              legend=True, markersize=45, cmap='Reds',
              ax=ax)
ax.set_title("Arizona stream gauge drainge area\n (sq km)")
plt.axis('equal')
plt.show()

# %%
# WBD: https://www.usgs.gov/core-science-systems/ngp/national-hydrography/access-national-hydrography-products
# https://viewer.nationalmap.gov/basic/?basemap=b1&category=nhd&title=NHD%20View

file = os.path.join('..','..', '..', 'homework-XUEYANZZZ', 'data/WBD_15_HU2_GDB', 'WBD_15_HU2_GDB.gdb')
# list layers of a gdb file
fiona.listlayers(file)
HUC6 = gpd.read_file(file, layer="WBDHU6")

type(HUC6)
HUC6.head()

# %% Add some points
# UA:  32.22877495, -110.97688412
# STream gauge:  34.44833333, -111.7891667
point_list = np.array([[-110.97688412, 32.22877495],
                       [-111.7891667, 34.44833333]])
# Make these into spatial features
point_geom = [Point(xy) for xy in point_list]
point_geom

# Map a dataframe of these points
point_df = gpd.GeoDataFrame(point_geom, columns=['geometry'],
                            crs=HUC6.crs)

# %% All layers on the same plot should the same projection
HUC6.crs
gages.crs

# Modify crs of gages to HUC6
gages_AZ_project = gages_AZ.to_crs(HUC6.crs)

# Now plot 
fig, ax = plt.subplots(figsize=(5, 5))
gages_AZ_project.plot(column='DRAIN_SQKM', categorical=False,
                      markersize=10, cmap='Reds', ax=ax,
                      legend=True,
                      legend_kwds={'label': r'Drainage area ($km^{2}$)'})

point_df.plot(ax=ax, color='black', marker='*', markersize=30)
HUC6.boundary.plot(ax=ax, color=None, 
                   edgecolor='black', linewidth=1)
ax.set_title(" Study region")
ctx.add_basemap(ax, crs=HUC6.crs)
fig.savefig('studyregion.jpg', dpi=400)
# %%
