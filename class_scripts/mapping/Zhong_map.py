# %%
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import fiona
from shapely.geometry import Point
import contextily as ctx
import os

# %%
# Gauges II USGS stream gauge dataset:
# https://water.usgs.gov/GIS/metadata/usgswrd/XML/gagesII_Sept2011.xml#stdorder

# Read it using geopandas
file = os.path.join('..', 'data', 'gagesII_9322_point_shapefile',
                    'gagesII_9322_sept30_2011.shp')
gages = gpd.read_file(file)

# Check the vector format of the data
gages.geom_type  # All points

# Subset grids in AZ
gages_AZ = gages[gages['STATE'] == 'AZ']

# %%
# Add two points
# UA:  32.22877495, -110.97688412
# Stream gauge:  34.44833333, -111.7891667
point_list = np.array([[-110.97688412, 32.22877495],
                       [-111.7891667, 34.44833333]])
# Make these into spatial features
point_geom = [Point(xy) for xy in point_list]

# Make a dataframe of these points
point_df = gpd.GeoDataFrame(point_geom, columns=['geometry'],
                            crs="WGS84")

# Change CRS
point_pr_gages = point_df.to_crs(gages.crs)

# %%
# HUC6
# https://viewer.nationalmap.gov/basic/?basemap=b1&category=nhd&title=NHD%20View
file = os.path.join('..', 'data', 'WBD_15_HU2_GDB', 'WBD_15_HU2_GDB.gdb')
fiona.listlayers(file)
HUC6 = gpd.read_file(file, layer="WBDHU6")
HUC6_pr_gages = HUC6.to_crs(gages.crs)

# %%
# Plot
fig, ax = plt.subplots(figsize=(6, 8))
# Layer 1
HUC6_pr_gages.plot(ax=ax, color='white', edgecolor='black',
                   linewidth=1, alpha=0.5)
# Layer 2
gages_AZ.plot(column='DRAIN_SQKM', categorical=False,
              legend=True, markersize=25, cmap='RdBu',
              ax=ax)
# Layer 3
point_pr_gages.plot(ax=ax, color='black', marker='*',
                    markersize=150)
# Layer 4
ctx.add_basemap(ax, source=ctx.providers.Stamen.TonerLite, crs=gages_AZ.crs)
# Add axes labels
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
# Save the figure
fig.savefig("Zhong_map.png")

# %%
