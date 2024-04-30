'''
This file copies over images to new directory based on csv file made from bestImgPairs
'''

import pandas as pd
from pathlib import Path
import shutil


def saveBestImagePairs(data_dir, image_dir):

    def copy_imgs(data, c):
        new_list_png = []
        new_list_jpg = []
        for num in data:
            new_list_png.append("./streetviewImg/png/" + str(num) + "_old.png")
            new_list_png.append("./streetviewImg/png/" + str(num) + "_new.png")
            new_list_jpg.append("./streetviewImg/jpg/" + str(num) + "_old.jpg")
            new_list_jpg.append("./streetviewImg/jpg/" + str(num) + "_new.jpg")

        # copy over images
        for f in new_list_png:
            shutil.copy(f, image_dir + c + "/png/")
        for f in new_list_jpg:
            shutil.copy(f, image_dir + c + "/jpg/")

    # delete imgs in directory as safety measure (sucks for hard drive)
    for f in Path(image_dir + "png/").rglob('*.png'):
        try:
            f.unlink()
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))
    for f in Path(image_dir + "jpg/").rglob('*.jpg'):
        try:
            f.unlink()
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))

    # copy now
    df = pd.read_csv(data_dir)
    df = df.astype('Int64')
    for name in df:
        copy_imgs(df[name].dropna().values.tolist(), name)



if __name__ == "__main__":
    # Doesn't delete ugh, just manually copy to SemanticSegmentation/Imgs
    saveBestImagePairs("./csv/imgPairsForTraining.csv", "./bestStreetviewImg/")
    print("Done")
