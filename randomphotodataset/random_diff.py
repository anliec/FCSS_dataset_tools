import os
import glob
import random
import shutil
import argparse

from datasetgenerator.load_and_split_laser_pair import get_gps_coord


def get_random_pair(count: int, dataset_path: str, min_offset: float=1.0):
    print("Listing available pictures in " + dataset_path)
    photo_list = glob.glob(os.path.join(dataset_path, "VBags/[0-9]*/[0-9]*/[0-9]*.jpg"))
    print("Done")
    if len(photo_list) == 0:
        raise RuntimeError("No images available in: {}\n"
                           "are you sure that the path to the 'lake' folder is correct?".format(dataset_path))
    pair_list = []
    print("Generating pairs")
    while len(pair_list) < count:
        path1 = photo_list[random.randint(0, len(photo_list) - 1)]
        path2 = photo_list[random.randint(0, len(photo_list) - 1)]
        splited_path1 = path1.split('/')
        splited_path2 = path2.split('/')
        seq1_int = int(splited_path1[-2]) * 1000 + int(splited_path1[-1][:-4])
        seq2_int = int(splited_path2[-2]) * 1000 + int(splited_path2[-1][:-4])
        try:
            x1, y1 = get_gps_coord(splited_path1[-3], str(seq1_int), dataset_path)
            x2, y2 = get_gps_coord(splited_path2[-3], str(seq2_int), dataset_path)
        except FileNotFoundError as e:
            print("auxiliary file not fund in:",
                  os.path.join(dataset_path, "VBags", splited_path1[-3], "image_auxilliary.csv"),
                  "or",
                  os.path.join(dataset_path, "VBags", splited_path2[-3], "image_auxilliary.csv"))
            continue

        if abs(float(x1) - float(x2)) < min_offset and abs(float(y1) - float(y2)) < min_offset:
            print("Random pair may look at the same place, skip")
            continue

        name = "{}_{}_{}_{}_{}_{}_{}_{}.jpg".format(splited_path1[-3], seq1_int, x1, y1,
                                                    splited_path2[-3], seq2_int, x2, y2)
        pair_list.append((path1, path2, name))
    print("Done")
    return pair_list
        

def generate_random_dataset(count: int, images_path: str, output_path: str, train_test_split: float=0.5):
    train_pair_count = int(count * train_test_split)
    pair_list = get_random_pair(count, images_path)

    # create dataset directory (fail if they exist)
    os.makedirs(output_path, exist_ok=True)
    os.makedirs(os.path.join(output_path, "test/left/-1"))
    os.makedirs(os.path.join(output_path, "test/right/-1"))
    os.makedirs(os.path.join(output_path, "train/left/-1"))
    os.makedirs(os.path.join(output_path, "train/right/-1"))
    print("Writing train dataset")
    for i1, i2, name in pair_list[:train_pair_count]:
        shutil.copyfile(i1, os.path.join(output_path, "train/left/-1/", name))
        shutil.copyfile(i2, os.path.join(output_path, "train/right/-1/", name))
    print("Writing test dataset")
    for i1, i2, name in pair_list[train_pair_count:]:
        shutil.copyfile(i1, os.path.join(output_path, "test/left/-1/", name))
        shutil.copyfile(i2, os.path.join(output_path, "test/right/-1/", name))
    print("Done")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-directory',
                        default='/tmp/data',
                        type=str,
                        dest="output_directory")
    parser.add_argument('-i', '--input-directory',
                        default='/cs-share/pradalier/lake/',
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
