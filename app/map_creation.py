import sys
sys.path.append('C:/Users/reett/AppData/Local/conda/conda')

import geopandas as gpd
import folium
import matplotlib
import mapclassify
import pandas as pd
import shapely


world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
cities = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

activities = pd.read_json('../filut/activities_review.json')

gdf = gpd.GeoDataFrame(activities.drop(['latitude', 'longitude'], axis=1),
                       crs={'init': 'epsg:4326'},
                       geometry=[shapely.geometry.Point(xy)
                                for xy in zip(activities.longitude, activities.latitude)])


m = world.explore(
    column="pop_est",  # make choropleth based on "BoroName" column
    scheme="naturalbreaks",  # use mapclassify's natural breaks scheme
    legend=True, # show legend
    k=10, # use 10 bins
    legend_kwds=dict(colorbar=False), # do not use colorbar
    name="countries" # name of the layer in the map
)

cities.explore(
    m=m, # pass the map object
    color="red", # use red color on all points
    marker_kwds=dict(radius=10, fill=True), # make marker radius 10px with fill
    tooltip="name", # show "name" column in the tooltip
    tooltip_kwds=dict(labels=False), # do not show column label in the tooltip
    name="cities" # name of the layer in the map
)

folium.TileLayer('Stamen Toner', control=True).add_to(m)  # use folium to add alternative tiles
folium.LayerControl().add_to(m)  # use folium to add layer control

m  # show map

m.save('activities_map.html')