import geopandas as gpd
import fiona

'''
This file subsets the initial Green space data retrieved from Trust from for Public Land by Morris County.
As the dataset is extremely large, a smaller version is desired for repeated exploration
'''

def save_new_files(county: str):
    """
    This function simply opens the main source file and outputs a smaller version
    * File opens as GeoDatabase but saves as GeoPackage
    """
    GDB_Path = '../Data/greenSpace.gdb'
    #fiona.listlayers(GDB_Path)
    # Need to see which layer to open --> We want ParkServe_Parks_05152023

    df_main = gpd.read_file(GDB_Path, driver='FileGDB', layer='ParkServe_Parks_05152023')
    df_main_nj = df_main.copy()[df_main["Park_State"] == "New Jersey"]
    df_main_nj_morris = df_main_nj[df_main_nj["Park_County"] == county]

    df_main_nj_morris.to_file(county.split(' ')[0] + '_subset.gpkg', driver="GPKG")


if __name__ == '__main__':
    save_new_files("./Morris County")