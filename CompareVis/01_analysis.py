import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import heapq
import os

'''
This file introduces two methods to comparing two streetview image pairs on their pixel data. 
 After the images have been processed through the semantic segmentation model, we can use the 
 fact that the different colors represent different objects. This file outputs numerical results
 from comparing the image two different ways: 1.) the difference in building pixels, 2.) the 
 difference in all pixels.
'''


def crop_right_image(image):
    """
    Crops image to only the right half (semantic segmentation model)
    """
    height, width, channels = image.shape
    return image[0:height, int(width / 2):]


def load_images_from_folder(folder):
    """
    Loads all image pairs in a directory and stores in images list with sample number at index 1.
    """
    images = []
    samples = []
    for filename1 in os.listdir(folder):
        fl1_sample = filename1.split('_')[0]
        fl1_age = filename1.split('_')[1].rsplit('.', 1)[0]
        if fl1_sample not in samples:
            for filename2 in os.listdir(folder):
                fl2_sample = filename2.split('_')[0]
                fl2_age = filename2.split('_')[1].rsplit('.', 1)[0]
                if (fl2_sample == fl1_sample) and (fl2_age != fl1_age):
                    if fl1_age == "old":
                        img1 = cv2.imread(os.path.join(folder, filename1))
                        img2 = cv2.imread(os.path.join(folder, filename2))
                    else:
                        img2 = cv2.imread(os.path.join(folder, filename1))
                        img1 = cv2.imread(os.path.join(folder, filename2))
                    if (img1 is not None) and (img2 is not None):
                        images.append(list((fl1_sample, img1, img2)))  # img1 will always be old, img will always be new
                    samples.append(fl1_sample)
                    break
    return images


def get_percent_color(image, color):
    """
    Returns percent of specific colored pixels of an image.
    """
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    total_pixels = 409600

    pixels = img.flatten().reshape(total_pixels, 3)

    seta = np.unique(pixels, axis=0)  # get unique values

    dictt = {}
    for x in seta:
        count = 0
        for y in pixels:
            if (x == y).all():
                count += 1
        dictt[str(x)] = count

    a = heapq.nlargest(20, dictt, key=dictt.get)

    for x in dictt:
        if x == color:
            building_percent = (dictt[x] / total_pixels) * 100
            return round(building_percent, 2)
    return 0


# Way 1: Filter out building percent of total image and get difference.
def building_percent_diff(image1, image2):
    """
    This function takes a percent difference of building pixels from 2 images.
    """
    #
    val1 = get_percent_color(image1, "[180 120 120]")  # rgb color for buildings
    val2 = get_percent_color(image2, "[180 120 120]")
    # print(val1)
    # print(val2)
    if val1 == 0:
        return val2  # no buildings were found
    elif val2 == 0:
        return val1
    else:
        return round(abs(val1 - val2), 2)


# Way 2: Overlap images, take percentage of total difference between images.
def overlap_binary_image(image1, image2):
    """
    This function overlaps 2 images into a black and white version representing different pixels.
    """
    img1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    img2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
    h, w, _ = img1.shape  # same shape
    blank_image = np.zeros((h, w, 3), np.uint8)

    a = []
    count = 0
    for x in range(w):
        for y in range(h):
            px1 = img1[y, x]
            px2 = img2[y, x]
            if bool(set(px1).intersection(px2)):  # same color, change to white
                count = count + 1
                blank_image[y][x] = [255, 255, 255]

    return blank_image


def overlap_percent_diff(image1, image2):
    """
    Takes the overall percentage of different pixels in the binary image.
    """
    comb = overlap_binary_image(image1, image2)
    comb_percent_diff = get_percent_color(comb, "[0 0 0]")
    return comb_percent_diff


if __name__ == "__main__":

    images = load_images_from_folder("./morrisInput/")
    building_percent_vals = []
    overlap_percent_vals = []
    sample_list = []

    # Iterate through all image pairs in input folder
    for img in images:
        sample_list.append(int(img[0]))
        print("Sample: " + str(img[0]))

        cropped_old = crop_right_image(img[1])
        cropped_new = crop_right_image(img[2])

        # Way 1
        building_percent_vals.append(building_percent_diff(cropped_old, cropped_new))

        # Way 2
        overlap_percent_vals.append(overlap_percent_diff(cropped_old, cropped_new))

    df = pd.DataFrame(
        data={'img': sample_list, 'building_percent': building_percent_vals, 'overlap_percent': overlap_percent_vals})
    df.to_csv("./files/morrisNumericalAnalysis.csv", index=False)

