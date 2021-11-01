# %%
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import fiona
from shapely.geometry import Point
import os

# %%
# Prepare data for AZ State Boundary using Geodatabase:
# https://azgeo-open-data-agic.hub.arcgis.com/datasets/azgeo::arizona-state-boundary/about
file = os.path.join('..', 'data',
                    'Arizona_State_Boundary-fgdb',
                    'd09edca433824603876f0a303adb5404.gdb')
fiona.listlayers(file)
azboundary = gpd.read_file(file, layer='azboundary')

# Prepare data for 2021 AZ wildfires using shapefile:
# https://azgeo-open-data-agic.hub.arcgis.com/datasets/nifc::wfigs-2021-wildland-fire-perimeters-to-date/explore?location=33.938905%2C-111.146632%2C7.92

file = os.path.join('../', 'data',
                    'WFIGS_-_2021_Wildland_Fire_Perimeters_to_Date',
                    'FH_Perimeter.shp')
fires = gpd.read_file(file)

# Select the polygon for Backbone Fire burn area:
fires_backbone = fires[fires['OBJECTID'] == 11575]

# Prepare data for AZ dams using shapefile:
# https://geodata-asu.hub.arcgis.com/datasets/asu::national-inventory-of-dams-arizona-2018/about

file = os.path.join('../', 'data',
                    'National_Inventory_of_Dams_-_Arizona_(2018)',
                    'National_Inventory_of_Dams_-_Arizona_(2018).shp')
dams = gpd.read_file(file)

# Prepare data for Ephemeral and Perennial Streams in AZ using shapefile:
# https://azgeo-open-data-agic.hub.arcgis.com/datasets/azgeo::streams-ephemeral-and-perennial/about
file = os.path.join('..', 'data',
                    'Streams___Ephemeral_and_Perennial-shp',
                    'Streams___Ephemeral_and_Perennial.shp')
streams = gpd.read_file(file)

# Pulling for large river:
verde_river = streams[streams['NAME'] == 'Verde River']
salt_river = streams[streams['NAME'] == 'Salt River']

# Prepare data for HUC1506 watershed using geodatabase:
# https://www.sciencebase.gov/catalog/item/5d30c292e4b01d82ce84aa34

file = os.path.join('..', 'data',
                    'NHDPLUS_H_1506_HU4_GDB',
                    'NHDPLUS_H_1506_HU4_GDB.gdb')
fiona.listlayers(file)
HUC8_1506 = gpd.read_file(file, layer="WBDHU8")

# Prepare data for HUC1408 watershed using shapefile:
# https://azgeo-open-data-agic.hub.arcgis.com/datasets/azgeo::us-4-digit-hus-subregion/explore?filters=eyJzdGF0ZXMiOlsiQVoiLCJBWixDQSxNWCxOViIsIkFaLENPLE5NLFVUIiwiQVosTVgiLCJBWixNWCxOTSIsIkFaLE5NIiwiQVosTlYsVVQiLCJBWixVVCJdfQ%3D%3D
file = os.path.join('..', 'data',
                    'US_4-digit_HUs_AZ',
                    'US_4-digit_HUs_AZ.shp')
HUC4 = gpd.read_file(file)
HUC4_AZ = HUC4.drop(index=4)
fires.total_bounds
dams.total_bounds

# %%
# Reproject vector objects to NAD83 | Lat(N)/Lon(E) | degrees:
HUC4_AZ_nad83 = HUC4_AZ.to_crs(HUC8_1506.crs)
azboundary_nad83 = azboundary.to_crs(HUC8_1506.crs)
fires_backbone_nad83 = fires_backbone.to_crs(HUC8_1506.crs)
dams_nad83 = dams.to_crs(HUC8_1506.crs)
verde_river_nad83 = verde_river.to_crs(HUC8_1506.crs)
salt_river_nad83 = salt_river.to_crs(HUC8_1506.crs)

# %%
dams_nad83_clip = gpd.clip(dams_nad83, HUC8_1506)
HUC4_AZ_nad83_clip = gpd.clip(HUC4_AZ_nad83, azboundary_nad83)

# %%
# Stream gauge:  34.44833333, -111.7891667
point_list = np.array([[-111.7891667, 34.44833333]])
# make these into spatial features
point_geom = [Point(xy) for xy in point_list]
point_geom

# map a dataframe of these points
point_df = gpd.GeoDataFrame(point_geom, columns=['geometry'],
                            crs=HUC8_1506.crs)

# %%
# plot these on the first dataset

fig, ax = plt.subplots(figsize=(15, 15))

azboundary_nad83.boundary.plot(ax=ax,
                               color=None,
                               edgecolor='black',
                               linewidth=1,
                               label='AZ State Boundary')
verde_river_nad83.plot(ax=ax,
                       linewidth=.6,
                       color='dodgerblue',
                       label='Verde River')
salt_river_nad83.plot(ax=ax,
                      linewidth=.5,
                      color='blue',
                      label='Salt River')
HUC8_1506.plot(ax=ax,
               color='lightskyblue',
               alpha=.8,
               legend=True)
HUC4_AZ_nad83_clip.plot(ax=ax,
                        color='lightskyblue',
                        edgecolor='turquoise',
                        alpha=.3)
point_df.plot(ax=ax,
              color='fuchsia',
              marker='o',
              markersize=60,
              label='Stream Gauge')
dams_nad83_clip.plot(ax=ax,
                     marker='x',
                     color='brown',
                     label='Active Dams')
fires_backbone_nad83.plot(ax=ax,
                          color='gold')

ax.set_title("HU4 - 1506 w/ Surrounding HU4 Boundaries")
ax.legend()
plt.show()
# %%
