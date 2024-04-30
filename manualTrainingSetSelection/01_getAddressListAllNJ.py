import numpy as np
import geopandas as gpd

req_cols = ['FULLADDR','POST_CODE','POST_COMM','COUNTY','PLACE_TYPE','PLACEMENT','LONG_', 'LAT']

data = gpd.read_file('../Data/Addr_NG911.gdb', include_fields=req_cols) # 5m 51s for full df

df = data.drop("geometry", axis=1).copy()

df["PLACE_TYPE"] = df["PLACE_TYPE"].mask(~df["PLACE_TYPE"].isin(['Residence', 'Unknown', 'Industrial', 'Outdoors']), "Commercial")
# Sets all other possible Place Types to commercial as it fits that category

df.dropna(inplace=True)
df['COUNTY'].isnull().value_counts()
df["COUNTY"] = df["COUNTY"].astype(np.int64) # need to convert this column into int64

# need to build: '950 Cambridge St, Cambridge, MA 02141' because lat long is too inaccurate
df["ADDRESS"] = df["FULLADDR"] + ", " + df["POST_COMM"] + ", NJ " + df["POST_CODE"]

nj_address_list = df[["PLACE_TYPE","ADDRESS","LONG_","LAT"]]

nj_address_list.to_csv('./csv/nj_address_list.csv', index=False)

print("Done")

# Unfortuntely, we cannot subset the number of addresses here because we have to make sure they are valid addresses,
# therefore, we would need backups if they fail. We shall export entire sets instead.