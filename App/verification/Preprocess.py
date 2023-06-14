import os
import shutil
import cv2
import itertools
import tensorflow as tf
from sklearn.utils import shuffle
from PIL import Image
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from dotenv import dotenv_values
from skimage.filters import threshold_otsu

# Load environment variables from .env file
env_vars = dotenv_values()


# Make Directories
def makeDirectoryDeleteAndCreate(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)


def deleteDirectory(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def preprocessAndResizeV1(file_path):
    # Read in image from file path
    byte_img = tf.io.read_file(file_path)
    # Load in the image
    img = tf.io.decode_jpeg(byte_img)

    # Preprocessing steps - resizing the image to be 100x100x3
    img = tf.image.resize(img, (100, 150))
    # Scale image to be between 0 and 1
    img = img / 255.0

    # Return image
    return img


def threshold_image(img_arr):
    thresh = threshold_otsu(img_arr)
    return np.where(img_arr > thresh, 255, 0)


def convertImage(path):
    im = Image.open(path)

    fill_color = (255, 255, 255)  # your new background color

    im = im.convert("RGBA")  # it had mode P after DL it from OP
    if im.mode in ('RGBA', 'LA'):
        background = Image.new(im.mode[:-1], im.size, fill_color)
        background.paste(im, im.split()[-1])  # omit transparency
        im = background

    return im.convert("RGB")


def create_batch(pos_groups, inp_groups, user, batch_size=1):
    for person in pos_groups:
        for path in person:
            img = convertImage(path)
            img.save(path)

    for person in inp_groups:
        for path in person:
            img = convertImage(os.path.join('verification', 'application_data', user, 'new_sign', 'tempSign.png'))
            img.save(path)

    while True:
        all_pairs = []

        for pos, inp in zip(pos_groups, inp_groups):
            for i in range(len(inp)):
                all_pairs.extend(list(itertools.product(pos, inp)))

        all_pairs = shuffle(all_pairs)

        img_w = int(env_vars["IMG_W"])
        img_h = int(env_vars["IMG_H"])

        k = 0
        pairs = [np.zeros((batch_size, img_h, img_w, 1)) for i in range(2)]
        for ix, pair in enumerate(all_pairs):
            img1 = cv2.imread(pair[0], 0)
            img2 = cv2.imread(pair[1], 0)
            img1 = cv2.resize(img1, (img_w, img_h))
            img2 = cv2.resize(img2, (img_w, img_h))
            img1 = np.array(img1, dtype=np.float64)
            img2 = np.array(img2, dtype=np.float64)
            img1 = np.squeeze(img_to_array(img1))
            img2 = np.squeeze(img_to_array(img2))
            img1 = threshold_image(img1)
            img2 = threshold_image(img2)
            img1 = img1 * (1. / 255)
            img2 = img2 * (1. / 255)
            img1 = img1[..., np.newaxis]
            img2 = img2[..., np.newaxis]
            pairs[0][k, :, :, :] = img1
            pairs[1][k, :, :, :] = img2
            k += 1
            if k == batch_size:
                yield pairs
                k = 0
                pairs = [np.zeros((batch_size, img_h, img_w, 1)) for i in range(2)]
