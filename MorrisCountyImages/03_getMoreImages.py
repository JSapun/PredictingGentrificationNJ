import pandas as pd
import numpy as np
from streetview import search_panoramas, get_streetview
from tqdm import tqdm

'''
This file uses the metadata lat and long (in this file) from the previous script, to retrieve the 
 oldest and newest snapshot of one location. This file generates a given sample (20) of valid image 
 pairs for each town in Morris County.
'''

# Get image pairs, a sample of 20 per each town in Morris County
def save_image_pair(lat, lon, dir, sample):
    """
    This function obtain streetview images by coordinate request and save it to a
    specific directory location. It will save as both a PNG and JPEG.
    """
    panos = search_panoramas(lat=lat, lon=lon)

    cleaned_panos = [panos[i] for i, x in enumerate([x.date for x in panos], 0) if
                     x is not None]  # Only get images with clean dates
    pano_dates = [x.date for x in cleaned_panos]
    pano_ids = [x.pano_id for x in cleaned_panos]

    # Check we have at least 2 panos
    if len(pano_dates) < 2:
        return False, []

    # We want the first and last dates
    pano_dates_subset = [pano_dates[0], pano_dates[-1]]
    pano_ids_subset = [pano_ids[0], pano_ids[-1]]

    # print(pano_dates_subset)
    # print(pano_ids_subset)

    # meta = [get_panorama_meta(pano_id=x, api_key=api_key) for x in pano_ids_subset]

    # print("\n" + str([x.status for x in meta]))

    images = [get_streetview(pano_id=x, api_key=api_key) for x in pano_ids_subset]  # actually gets image data

    images[0].save(dir + "png/" + sample + "_old.png", "png")
    images[1].save(dir + "png/" + sample + "_new.png", "png")

    images[0].save(dir + "jpg/" + sample + "_old.jpg", "jpeg")
    images[1].save(dir + "jpg/" + sample + "_new.jpg", "jpeg")

    return True, pano_dates_subset


def get_sample_size(df, towns, N, dir):
    """
    This function will iterate through town subsets to save a given sample (20) of image pairs
    using the previous function. It will also save a CSV containing image pair information.
    """
    save_df = pd.DataFrame(columns=['imgs', 'pano_id', 'town', 'lat', 'long', 'address', 'dates'])
    running_sum = 0
    running_img_index = 0

    for town in tqdm(towns):  # iterate through towns until desired amount received
        shuffled_df = df[df.town == town].sample(frac=1).reset_index(drop=True)  # Sort and shuffle
        check = False  # Some samples will fail
        img_index = 0
        i = 0
        while i < N:  # Stop once sample is reached for each town
            one_sample = pd.DataFrame()
            dates = []
            while not check:
                if img_index >= len(shuffled_df):  # Huge problem
                    print("\nSample Size too large, too many errors from Streetview!")
                    print(town)
                    print(img_index)
                    print(i)
                    exit()
                one_sample = shuffled_df.iloc[img_index]
                check, dates = save_image_pair(one_sample.lat.item(), one_sample.lng.item(), dir, str(running_img_index))
                img_index += 1
            row = [running_img_index, one_sample.pano_id, one_sample.town, one_sample.lat.item(), one_sample.lng.item(),
                   one_sample.address, dates]
            save_df.loc[running_img_index] = np.asarray(row, dtype="object")
            running_img_index += 1
            check = False
            i += 1
        running_sum += img_index

    print("Iterated through: " + str(running_sum) + " images")
    save_df.to_csv("./csv/randomImagePairInfo.csv", index=False)  # Save image information


if __name__ == '__main__':
    api_key = open("../MapsAPI_Key.txt", "r").read()
    df = pd.read_csv("./csv/cleaned_morris_address.csv")
    towns = list(pd.read_csv("./csv/morris_towns.csv").towns)
    get_sample_size(df, towns, 20, "./streetviewImg/")  # 40 mins / 100, needed 106 for 39
    print("Done")
