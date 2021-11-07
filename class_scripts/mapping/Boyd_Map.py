# %%
import os
import geopandas as gpd
import contextily as ctx
import fiona
import matplotlib.pyplot as plt

# %%
# Import stream gage locations for all of the US (get data at link below)
# https://water.usgs.gov/GIS/metadata/usgswrd/XML/gagesII_Sept2011.xml#stdorder
gages_file = os.path.join('..', 'data', 'Shapefiles',
                          'gagesII_9322_sept30_2011.shp')
gages = gpd.read_file(gages_file)
# Import HUC8 data for AZ (get data at link below)
# https://www.sciencebase.gov/catalog/item/5a96cda0e4b06990606c4d0f
huc8_file = os.path.join('..', 'data', 'Shapefiles',
                         'NHD_H_15060203_HU8_GDB.gdb')
fiona.listlayers(huc8_file)
HUC8 = gpd.read_file(huc8_file, layer='WBDHU8')
# Import AZ streams data (get data at link below)
# https://azgeo-open-data-agic.hub.arcgis.com/datasets/azgeo::streams-ephemeral-and-perennial/about
AZstream_file = os.path.join('..', 'data', 'Shapefiles',
                             'Streams___Ephemeral_and_Perennial.shp')
AZstreams = gpd.read_file(AZstream_file)

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
# Reproject the HUC8 layer to the stream gages CRS
HUC8_reproj = HUC8.to_crs(gages_AZ.crs)
AZstreams_reproj = AZstreams.to_crs(gages_AZ.crs)

# Clip gages geodataframe to extent of our watershed to make map more readable
clip_gages = gpd.clip(gages_AZ, HUC8_reproj)
# To see which gages need to be connected to streams on the map, find the head
# of the clipped gages
clip_gages.head(20)

# Create geodataframes of streams in the watershed based on the gages within
# the watershed extent
verde_river = AZstreams[AZstreams['NAME'] == 'Verde River']
east_verde = AZstreams[AZstreams['NAME'] == 'East Verde River']
sycamore = AZstreams[AZstreams['NAME'] == 'Sycamore Creek']
east_syc = AZstreams[AZstreams['NAME'] == 'East Fork Sycamore Creek']
wet_bot = AZstreams[AZstreams['NAME'] == 'Wet Bottom Creek']
clear_creek = AZstreams[AZstreams['NAME'] == 'West Clear Creek']

# Reproject the new river geodataframes so everything is in the same CRS
verde_river_reproj = verde_river.to_crs(gages_AZ.crs)
east_verde_reproj = east_verde.to_crs(gages_AZ.crs)
sycamore_reproj = sycamore.to_crs(gages_AZ.crs)
east_syc_reproj = east_syc.to_crs(gages_AZ.crs)
wetbottom_reproj = wet_bot.to_crs(gages_AZ.crs)
clear_creek_reproj = clear_creek.to_crs(gages_AZ.crs)

# Clip the river geodataframes to the watershed extent
clip_verde = gpd.clip(verde_river_reproj, HUC8_reproj, keep_geom_type=True)
clip_east_verde = gpd.clip(east_verde_reproj, HUC8_reproj, keep_geom_type=True)
clip_syc = gpd.clip(sycamore_reproj, HUC8_reproj, keep_geom_type=True)
clip_east_syc = gpd.clip(east_syc_reproj, HUC8_reproj, keep_geom_type=True)
clip_wetbot = gpd.clip(wetbottom_reproj, HUC8_reproj, keep_geom_type=True)
clip_clrcrk = gpd.clip(clear_creek_reproj, HUC8_reproj, keep_geom_type=True)

# %%
# Plot layers, creating map
fig, ax = plt.subplots(figsize=(15, 15))
fig.patch.set_facecolor("white")
ax.set(title='Lower Verde River Watershed Area, AZ', xlabel='Easting',
       ylabel='Northing')
layer1 = HUC8_reproj.boundary.plot(ax=ax, label='Watershed Boundaries',
                                   edgecolor='navy', linewidth=3)
layer2 = HUC8_reproj.plot(ax=ax, alpha=0.25, zorder=1)
layer3 = clip_verde.plot(ax=ax, color='darkgreen', label='Verde River',
                         zorder=2)
layer3A = clip_east_verde.plot(ax=ax, color='r', linewidth=1, 
                               label='Tributary Rivers',
                               zorder=2)
layer3B = clip_syc.plot(ax=ax, color='r', linewidth=1, zorder=2)
layer3C = clip_east_syc.plot(ax=ax, color='r', linewidth=1, zorder=2)
layer3D = clip_wetbot.plot(ax=ax, color='r', linewidth=1, zorder=2)
layer3E = clip_clrcrk.plot(ax=ax, color='r', linewidth=1, zorder=2)
layer4 = clip_gages.plot(ax=ax, color='aqua', label='Stream Gages', zorder=3)
layer5 = verde_station.plot(ax=ax, color='magenta', marker='^', markersize=200,
                            label='Stream Gage Used for Class Forecasts',
                            zorder=4)
ctx.add_basemap(ax, crs=gages_AZ.crs)
ax.legend(loc='lower right')
plt.show()
# fig.savefig('Verde_Watershed_Map', bbox_inches='tight')

# %%
