import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from pyproj import CRS

'''
This file simply plots all the verified addresses in New Jersey. It uses a Shapefile of New Jersey from NJGIN.
'''

def geo_plot_lat_lon(df, lat, lon, shapepath, savepath, title=None):
    """
    This functions uses the matplot lib to geo plot (lat,lon) pairs onto a given shapefile.
    Function saves image designated path.
    """
    new_jersey_map = gpd.read_file(shapepath)

    crs = CRS('EPSG:4326')
    geometry = [Point(xy) for xy in zip(lon, lat)]
    geo_df = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)

    fig, ax = plt.subplots(figsize=(20, 10))
    new_jersey_map.to_crs(epsg=4326).plot(ax=ax, color='lightgrey')
    geo_df.plot(ax=ax, markersize=0.5, alpha=1)

    plt.xlabel('Longitude', fontsize=18)
    plt.ylabel('Latitude', fontsize=18)
    ax.set_title(title, fontsize=18)

    plt.savefig(savepath)

'''
Example for use:

morris_cleaned = pd.read_csv("./cleaned_morris_meta_df.csv")

geo_plot_lat_lon(morris_cleaned, morris_cleaned.lat, morris_cleaned.lng, './Shapefiles/MorrisCounty'
                                                                         '/MorrisCountyParcels.shp',
                 './morris_cleaned_18k.png', 'Addresses in Morris County in New Jersey')
'''

if __name__ == '__main__':
    df = pd.read_csv("./csv/cleaned_nj_meta_df.csv")
    geo_plot_lat_lon(df, df.lat, df.lng, '../Data/State_Boundary_of_NJ/State_Boundary_of_NJ.shp',
                     './img/nj_cleaned_1.7k.png',
                     'Geo Plot of Random Addresses in New Jersey')
    print("Done")