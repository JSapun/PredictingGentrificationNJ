import geopandas as gpd
import fiona

def save_new_files(county: str):
    """
    This function simply opens the main source file and outputs a smaller version
    * File opens as gdb but saves as GeoJson
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