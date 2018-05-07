import os
import glob
import random
import shutil
import argparse

from datasetgenerator.load_and_split_laser_pair import get_gps_coord


def get_random_pair(count: int, dataset_path: str, min_offset: float=1.0):
    photo_list = glob.glob(os.path.join(dataset_path, "VBags/*/*/*.jpg"))
    if len(photo_list) == 0:
        raise RuntimeError("No images available in: {}\n"
                           "are you sure that the path to the 'lake' folder is correct?".format(dataset_path))
    pair_list = []
    while len(pair_list) < count:
        path1 = photo_list[random.randint(0, len(photo_list) - 1)]
        path2 = photo_list[random.randint(0, len(photo_list) - 1)]
        splited_path1 = path1.split('/')
        splited_path2 = path2.split('/')
        seq1_int = int(splited_path1[-2]) * 1000 + int(splited_path1[-1][:-4])
        seq2_int = int(splited_path2[-2]) * 1000 + int(splited_path2[-1][:-4])
        x1, y1 = get_gps_coord(splited_path1[-3], str(seq1_int))
        x2, y2 = get_gps_coord(splited_path2[-3], str(seq2_int))

        if abs(float(x1) - float(x2)) < min_offset and abs(float(y1) - float(y2)) < min_offset:
            print("Random pair may look at the same place, skip")
            continue

        name = "{}_{}_{}_{}_{}_{}_{}_{}.jpg".format(splited_path1[-3], seq1_int, x1, y1,
                                                    splited_path2[-3], seq2_int, x2, y2)
        pair_list.append((path1, path2, name))

    return pair_list
        

def generate_random_dataset(count: int, images_path: str, output_path: str, train_test_split: float=0.5):
    train_pair_count = int(count * train_test_split)
    pair_list = get_random_pair(train_pair_count, images_path)
    for i1, i2, name in pair_list:
        shutil.copyfile(i1, os.path.join(output_path, "train/left/-1/", name))
        shutil.copyfile(i2, os.path.join(output_path, "train/right/-1/", name))
    pair_list = get_random_pair(count - train_pair_count, images_path)
    for i1, i2, name in pair_list:
        shutil.copyfile(i1, os.path.join(output_path, "test/left/-1/", name))
        shutil.copyfile(i2, os.path.join(output_path, "test/right/-1/", name))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-directory',
                        default='/tmp/data',
                        type=str,
                        dest="output_directory")
    parser.add_argument('-i', '--input-directory',
                        default='/cs-share/pradalier/lake/VBags',
                        type=str,
                        dest="input_directory")
    parser.add_argument('-n', '--number-of-pair',
                        default=6000,
                        type=int,
                        dest="count")
    parser.add_argument('-s', '--train-percentage',
                        default=0.5,
                        type=float,
                        dest="train_percentage")
    args = parser.parse_args()

    generate_random_dataset(args.count, args.input_directory, args.output_directory, args.train_percentage)


if __name__ == '__main__':
    main()
