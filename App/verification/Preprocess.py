import os
import shutil
import tensorflow as tf

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