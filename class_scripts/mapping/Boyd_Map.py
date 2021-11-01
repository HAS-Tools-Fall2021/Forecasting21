# %%
import os
import geopandas as gpd
import contextily as ctx
import fiona
import matplotlib.pyplot as plt

# %%
# Import stream gage locations for all of the US
gages_file = os.path.join('..', 'data', 'Shapefiles',
                          'gagesII_9322_sept30_2011.shp')
gages = gpd.read_file(gages_file)
# Import HUC8 data for AZ
huc8_file = os.path.join('..', 'data', 'Shapefiles',
                         'NHD_H_15060203_HU8_GDB.gdb')
fiona.listlayers(huc8_file)
HUC8 = gpd.read_file(huc8_file, layer='WBDHU8')
# Import AZ streams data
AZstream_file = os.path.join('..', 'data', 'Shapefiles',
                             'NHD_H_Arizona_State_GDB.gdb')
fiona.listlayers(AZstream_file)
AZstreams = gpd.read_file(AZstream_file, layer='WBDLine')

# %%
# See first 5 entries in geodataframes:
gages.head()
HUC8.head()
AZstreams.head()
# See column names in geodataframes:
gages.columns
HUC8.columns
AZstreams.columns
# Check projection of geodataframes using the following code:
gages.crs
HUC8.crs
AZstreams.crs


# %%
# Get list of States in the geodataframe
gages.STATE.unique()
# Create smaller geodataframe for just the AZ stream gages
gages_AZ = gages[gages['STATE'] == 'AZ']
# Show how many entries in the AZ geodataframe:
gages_AZ.shape

# See if our station (09506000) is in the list of station IDs
gages_AZ.STAID.unique()
# Create geodataframe of just our station
verde_station = gages_AZ[gages_AZ['STAID'] == '09506000']
verde_station.head()

# %%
# Reproject the HUC8 layer and AZ streams layer to the stream gages CRS
HUC8_reproj = HUC8.to_crs(gages_AZ.crs)
AZstreams_reproj = AZstreams.to_crs(gages_AZ.crs)

# Focus geodataframes only on extent of our watershed to make map more readable
clip_gages = gpd.clip(gages_AZ, HUC8_reproj)
clip_streams = gpd.clip(AZstreams_reproj, HUC8_reproj, keep_geom_type=True)

# %%
# Plot layers, creating map
fig, ax = plt.subplots(figsize=(15, 15))
ax.set(title='Lower Verde River Watershed Area, AZ', xlabel='Easting',
       ylabel='Northing')
layer1 = HUC8_reproj.boundary.plot(ax=ax, label='Watershed Boundaries',
                                   edgecolor='navy', linewidth=3)
layer2 = HUC8_reproj.plot(ax=ax, alpha=0.25)
layer3 = clip_streams.plot(ax=ax, color='darkgreen',
                           label='Streams in Watershed')
layer4 = clip_gages.plot(ax=ax, color='aqua', label='Stream Gages')
layer5 = verde_station.plot(ax=ax, color='magenta', marker='^', markersize=200,
                            label='Stream Gage Used for Class Forecasts')
ctx.add_basemap(ax, crs=gages_AZ.crs)
ax.legend(loc='lower right')
plt.show()
# fig.savefig('Verde_Watershed_Map', bbox_inches='tight')
