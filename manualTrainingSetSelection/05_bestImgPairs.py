'''
This file uses Tkinter to set up a gui window to allow easier manual image analysis. It gives users the options to
search through different pairs of images, and save the ones where a change is most noticeable. Current limit is 20.
'''

from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import os
import pandas as pd
import math
import numpy as np

def processImages(list_out_dir, img_dir, clear=False):
    df = pd.read_csv(list_out_dir)

    if clear:
        df = pd.DataFrame(columns=df.columns, index=df.index) # Need way to clear data
        df.to_csv(list_out_dir, index=False)
        return None

    data_in = range(len(os.listdir('./streetviewImg/png/'))//2) # list of all images
    img_index = 0   # help rotate through images
    data_out = []
    df = pd.read_csv(list_out_dir)
    data_out_c_nan = df["change"].values.tolist()
    data_out_g_nan = df["good"].values.tolist()
    data_out_b_nan = df["bad"].values.tolist()

    data_out_c = [x for x in data_out_c_nan if not math.isnan(x)] # Remove Nans
    data_out_g = [x for x in data_out_g_nan if not math.isnan(x)]
    data_out_b = [x for x in data_out_b_nan if not math.isnan(x)]

    def next_pair(index: int):
        nonlocal data_in
        if not data_in:
            print("list input is empty")
            exit()

        image1 = Image.open(img_dir + str(data_in[index]) + "_old.png") # Combine 2 image pairs into one for easy canvas use
        image2 = Image.open(img_dir + str(data_in[index]) + "_new.png")
        image1_size = image1.size
        new_image = Image.new('RGB', (2 * image1_size[0], image1_size[1]), (250, 250, 250))
        new_image.paste(image1, (0, 0))
        new_image.paste(image2, (image1_size[0], 0))

        img_comb = ImageTk.PhotoImage(new_image)

        return img_comb

    # Create window
    window = Tk()
    window.title("Best Image Pair Classifier for Training Set")
    window.configure(background="white")
    window.minsize(1280, 640)  # width, height

    canvas = Canvas(window, width=1280, height=640)
    canvas.pack()

    # images
    pair = next_pair(img_index)
    image_container = canvas.create_image(0, 0, anchor="nw", image=pair)

    # Create a label widget to display the text
    text_label = Label(window, text="Please cycle through the images to find the best pair")
    text_label.pack()


    def processInput(string: str):
        nonlocal img_index
        nonlocal pair
        nonlocal data_out_c
        nonlocal data_out_g
        nonlocal data_out_b
        nonlocal data_in
        # update row value for image pair in df_out, remove row from df_in
        if string == "previous":
            if img_index == 0:
                img_index = len(data_in)
            img_index -= 1
            pair = next_pair(img_index)
            lbl.config(text="Image " + str(img_index))
        elif string == "next":
            img_index += 1
            if img_index == len(data_in):
                img_index = 0
            pair = next_pair(img_index)
            lbl.config(text="Image " + str(img_index))
        elif string == "save-c":
            if not (img_index in data_out_c) and (len(data_out_c) < 20):
                data_out_c.append(img_index)
                lbl.config(text="Saved Images " + str(img_index))
            else:
                lbl.config(text="Cant Save " + str(img_index))
        elif string == "save-g":
            if not (img_index in data_out_g) and (len(data_out_g) < 20):
                data_out_g.append(img_index)
                lbl.config(text="Saved Images " + str(img_index))
            else:
                lbl.config(text="Cant Save " + str(img_index))
        elif string == "save-b":
            if not (img_index in data_out_b) and (len(data_out_b) < 20):
                data_out_b.append(img_index)
                lbl.config(text="Saved Images " + str(img_index))
            else:
                lbl.config(text="Cant Save " + str(img_index))
        elif string == "index":
            inp = inputtxt.get(1.0, "end-1c")
            img_index = int(inp)
            pair = next_pair(img_index)

        # process next image
        canvas.imgref = pair
        canvas.itemconfig(image_container, image=pair)


        # Buttons
    A = ttk.Button(window, text="previous", command=lambda: processInput("previous"))
    B = ttk.Button(window, text="next", command=lambda: processInput("next"))
    C = ttk.Button(window, text="save-c", command=lambda: processInput("save-c"))
    D = ttk.Button(window, text="save-g", command=lambda: processInput("save-g"))
    E = ttk.Button(window, text="save-b", command=lambda: processInput("save-b"))
    txtbut = ttk.Button(window, text="index", command=lambda: processInput("index"))
    inputtxt = tk.Text(window, height=1, width=20)
    lbl = tk.Label(window, text="Image " + str(img_index))

    lbl.pack(side='left', anchor='e', expand=True)
    A.pack(side='left', anchor='e')
    B.pack(side='left', anchor='e')
    C.pack(side='left', anchor='e')
    D.pack(side='left', anchor='e')
    inputtxt.pack(side='right', anchor='w', expand=True)
    txtbut.pack(side='right', anchor='w')
    E.pack(side='right', anchor='w')


    window.mainloop()

    df["change"] = data_out_c + np.full((20-len(data_out_c)),np.nan).tolist() # need to buffer with nan
    df["good"] = data_out_g + np.full((20-len(data_out_g)),np.nan).tolist()
    df["bad"] = data_out_b + np.full((20-len(data_out_b)),np.nan).tolist()
    df.to_csv(list_out_dir, index=False)



if __name__ == "__main__":
    processImages("./csv/imgPairsForTraining.csv", "./streetviewImg/png/", False)
    # change - change, good (no change) - good, bad (no change) - bad
    print("Done")