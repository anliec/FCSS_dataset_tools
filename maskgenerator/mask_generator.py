import cv2
import numpy as np
import sys
import os
import glob
from multiprocessing import Pool
from scipy.signal import convolve2d


filter_size = 7
border_size = 10


def generator_mask(img):
    bound = np.max(img) * 0.5
    mask = (img < bound) * 255
    filter_matrix = np.ones(shape=(filter_size, filter_size), dtype=np.uint8)
    mask = convolve2d(mask, filter_matrix, mode='same')
    mask = (mask > 0) * 255
    mask[:border_size, :] = 0
    mask[-border_size:, :] = 0
    mask[:, -border_size:] = 0
    mask[:, :border_size] = 0
    return mask


def write_mask(img_path, mask_path=None):
    if mask_path is None:
        head, tail = os.path.split(img_path)
        mask_path = head + "/mask" + tail[-5:]
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img = img[:, :, 0]
    mask = generator_mask(img)
    cv2.imwrite(mask_path, mask)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("expected call are:")
        print(sys.argv[0], "source_image destination_mask")
        print(sys.argv[0], "-d directory_to_explore")
        exit(1)

    if sys.argv[1] != "-d":
        write_mask(sys.argv[1], sys.argv[2])
    else:
        path = sys.argv[2]
        if not os.path.isdir(path):
            raise OSError("the given path is not a directory")
        images = glob.glob(path + "/*/*/image[1-2].png")

        pool = Pool()

        pool.imap_unordered(write_mask, images, chunksize=20)

        pool.close()
        pool.join()
