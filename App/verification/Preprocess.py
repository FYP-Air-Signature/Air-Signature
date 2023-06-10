import os
import shutil
import cv2
import tensorflow as tf
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


def preprocess(file_path):
    # Load in the image
    img = cv2.imread(file_path, 0)

    img = cv2.resize(img, (int(env_vars["IMG_W"]), int(env_vars["IMG_H"])))

    img = np.array(img, dtype=np.float64)

    img = np.squeeze(img_to_array(img))

    img = threshold_image(img)

    img = img * (1. / 255)

    img = img[..., np.newaxis]

    return img
