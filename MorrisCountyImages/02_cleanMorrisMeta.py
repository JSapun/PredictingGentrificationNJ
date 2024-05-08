import pandas as pd
import requests
from tqdm import tqdm


# Check metadata for all addresses and print status


def validate(df):
    meta_base = 'https://maps.googleapis.com/maps/api/streetview/metadata?'
    api_key = open("../MapsAPI_Key.txt", "r").read()
    morris_df = df.copy().sample(300)  # 300 samples per town

    add_df = morris_df["ADDRESS"]
    town_df = morris_df["POST_COMM"]
    df_meta_response = [requests.get(meta_base, params={'key': api_key, 'location': x}) for x in add_df]
    # 30000 entries = 40 mins

    meta_resp_decoded = [x.json() for x in df_meta_response]
    meta_resp_status = [x.get('status') for x in meta_resp_decoded]
    meta_resp_id = [x.get('pano_id') for x in meta_resp_decoded]
    meta_resp_lat = [x.get('location', {'lat': None})['lat'] for x in meta_resp_decoded]
    meta_resp_lng = [x.get('location', {'lng': None})['lng'] for x in meta_resp_decoded]

    meta_df = pd.DataFrame({'pano_id': meta_resp_id, 'status': meta_resp_status, 'town': town_df, 'lat': meta_resp_lat,
                            'lng': meta_resp_lng, 'address': add_df})
    cleaned_meta_df = meta_df[meta_df["pano_id"].notnull()].reset_index(drop=True).drop_duplicates()
    return cleaned_meta_df


def iterate_towns(df):
    comb = pd.DataFrame()
    for town in tqdm(towns):
        ret = validate(df[df["POST_COMM"] == town])
        comb = pd.concat([comb, ret], ignore_index=True)
    return comb


if __name__ == '__main__':
    morris = pd.read_csv("./csv/morris_address.csv")
    towns = list(pd.read_csv("./csv/morris_towns.csv").towns)

    cleaned_morris_df = iterate_towns(morris)
    cleaned_morris_df.to_csv("./csv/cleaned_morris_address.csv", index=False)
