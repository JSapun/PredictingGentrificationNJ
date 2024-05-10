import pandas as pd
import requests
from tqdm import tqdm


'''
This file uses the Google Streetview api to verify each address contains a good
 streetview perspective. It returns a list of cleaned and valid New Jersey addresses.
'''

nj_data = pd.read_csv("./csv/nj_address_list.csv")

# Check metadata for all addresses and print status

meta_base = 'https://maps.googleapis.com/maps/api/streetview/metadata?'
pic_base = 'https://maps.googleapis.com/maps/api/streetview?'
api_key = open("../MapsAPI_Key.txt", "r").read()

nj_df = nj_data.copy().sample(2000)

nj_add_df = nj_df["ADDRESS"]
df_meta_response = [requests.get(meta_base, params={'key': api_key, 'location': x}) for x in tqdm(nj_add_df)]
# 30000 entries = 40 mins
# we will do 2000 entries for now

meta_resp_decoded = [x.json() for x in df_meta_response]
meta_resp_status = [x.get('status') for x in meta_resp_decoded]
meta_resp_id = [x.get('pano_id') for x in meta_resp_decoded]
meta_resp_lat = [x.get('location', {'lat': None})['lat'] for x in meta_resp_decoded]
meta_resp_lng = [x.get('location', {'lng': None})['lng'] for x in meta_resp_decoded]

meta_df = pd.DataFrame({'pano_id': meta_resp_id,'status': meta_resp_status, 'lat':meta_resp_lat, 'lng':meta_resp_lng, 'address':nj_add_df})
cleaned_meta_df = meta_df[meta_df["pano_id"].notnull()].reset_index(drop=True).drop_duplicates()
# drop bad status AND duplicates to reduce error in finding good addresses

cleaned_meta_df.to_csv("./csv/cleaned_nj_meta_df.csv", index=False)

print("Done")