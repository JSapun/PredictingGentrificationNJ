
'''
Process So far
1.) Get addresses in NJ
2.) Get metadata for all addresses in NJ, and clean the data based on Streetview API response
3.) Using the metadata lat and long (in this file), we are able to retrieve the oldest and newest snapshot of one location
    Should also output csv that stores img number with dates and addresses/lat long coordinates
'''

import pandas as pd
from streetview import search_panoramas, get_panorama_meta, get_streetview
from tqdm import tqdm


def save_image_pair(lat, lon, dir, sample):
    panos = search_panoramas(lat=lat, lon=lon)

    cleaned_panos = [panos[i] for i, x in enumerate([x.date for x in panos], 0) if
                     x is not None]  # Only get images with clean dates
    pano_dates = [x.date for x in cleaned_panos]
    pano_ids = [x.pano_id for x in cleaned_panos]

    # Check we have at least 2 panos
    if len(pano_dates) < 2:
        return False,[]

    # We want the first and last dates
    pano_dates_subset = [pano_dates[0], pano_dates[-1]]
    pano_ids_subset = [pano_ids[0], pano_ids[-1]]

    # print(pano_dates_subset)
    # print(pano_ids_subset)

    # meta = [get_panorama_meta(pano_id=x, api_key=api_key) for x in pano_ids_subset]

    # print("\n" + str([x.status for x in meta]))

    images = [get_streetview(pano_id=x, api_key=api_key) for x in pano_ids_subset]  # actually gets image data

    images[0].save(dir +"png/" + sample + "_old.png", "png")
    images[1].save(dir +"png/" + sample + "_new.png", "png")

    images[0].save(dir +"jpg/" + sample + "_old.jpg", "jpeg")
    images[1].save(dir +"jpg/" + sample + "_new.jpg", "jpeg")

    return True,pano_dates_subset


def get_sample_size(df, N, dir):
    check = False
    shuffled_df = df.sample(frac=1).reset_index(drop=True)
    img_index = 0
    save_df = pd.DataFrame(columns=['imgs', 'pano_id', 'lat', 'long', 'address', 'dates'])
    # Some samples will fail
    for i in tqdm(range(N)):
        one_sample = pd.DataFrame()
        dates = []
        while not check:
            if img_index >= len(shuffled_df):
                print("Sample Size too large, too many errors from Streetview!")
                exit()
            one_sample = shuffled_df.iloc[img_index]
            check,dates = save_image_pair(one_sample.lat.item(), one_sample.lng.item(), dir, str(i))
            img_index += 1
        check = False
        row = [i, one_sample.pano_id, one_sample.lat.item(), one_sample.lng.item(), one_sample.address, dates]
        save_df.loc[i] = row
    print(img_index)
    #save_df.to_csv("./csv/cleaned_nj_meta_df.csv", index=False)
    save_df.to_csv("./csv/randomImagePairInfo.csv", index=False) # Save image information



if __name__ == '__main__':
    api_key = open("../MapsAPI_Key.txt", "r").read()
    df = pd.read_csv("./csv/cleaned_nj_meta_df.csv")
    get_sample_size(df, 400, "./streetviewImg/") # 40 mins / 100
    print("Done")