import pandas as pd
import csv
import os
import shutil
import argparse
import random
import numpy as np

from datasetgenerator.load_and_split_laser_pair import manage_csv_row


def main():
    src_file = "/cs-share/pradalier/lake/pairs/image_pairs.csv"
    base_path = "/cs-share/pradalier/lake/"

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-directory',
                        default='/tmp/data',
                        type=str,
                        dest="output_directory")
    parser.add_argument('-d', '--gps-check-distance',
                        default=1.0,
                        type=float,
                        dest="gps_max_distance")
    parser.add_argument('-p', '--pair-file',
                        default=src_file,
                        type=str,
                        dest="pair_file")
    parser.add_argument('-i', '--input-directory',
                        default=base_path,
                        type=str,
                        dest="input_directory")
    parser.add_argument('-n', '--number-of-groups',
                        default=1,
                        type=int,
                        dest="number_of_groups")
    args = parser.parse_args()

    base_path = args.input_directory
    src_file = args.pair_file

    # create dataset directory (fail if they exist)
    os.makedirs(args.output_directory, exist_ok=True)
    os.makedirs(os.path.join(args.output_directory, "time/left/1"))
    os.makedirs(os.path.join(args.output_directory, "time/right/1"))
    group_list = []

    with open(src_file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        # read header
        survey_dates = csv_reader.__next__()[2:]
        # randomly select the wanted number of rows
        values_array = np.array(list(csv_reader), dtype=np.int64)
        random_row_index = np.random.choice(np.arange(0, values_array.shape[0]),
                                            size=args.number_of_groups,
                                            replace=False)
        random_row = values_array[random_row_index]
        del values_array
        for line in random_row:
            tuple_list = []
            ref_dir = line[0]
            ref_seq = line[1]
            for s, d in zip(line[2:], survey_dates):
                if s != -1:
                    t = manage_csv_row((tuple(map(str, (ref_dir, ref_seq, d, s))), base_path))
                    if t[0] is not None:
                        tuple_list.append(t)
            group_list.append(tuple_list)

    for tuple_list in group_list:
        for (dir1, seq1, x1, y1), (dir2, seq2, x2, y2) in tuple_list:
            if abs(float(x1) - float(x2)) > args.gps_max_distance or abs(float(y1) - float(y2)) > args.gps_max_distance:
                print("GPS check failed, skipping pair")
                continue

            shutil.copyfile(src=os.path.join(base_path, "VBags",
                                             dir1,
                                             "{:0=4d}/{:0=4d}.jpg".format(int('0' + seq1[:-3]), int(seq1[-3:]))),
                            dst=os.path.join(args.output_directory,
                                             "time",
                                             "left/1/{}_{}_{}_{}_{}_{}_{}_{}.jpg".format(dir1, seq1, x1, y1,
                                                                                         dir2, seq2, x2, y2)))
            shutil.copyfile(src=os.path.join(base_path, "VBags",
                                             dir2,
                                             "{:0=4d}/{:0=4d}.jpg".format(int('0' + seq2[:-3]), int(seq2[-3:]))),
                            dst=os.path.join(args.output_directory,
                                             "time",
                                             "right/1/{}_{}_{}_{}_{}_{}_{}_{}.jpg".format(dir1, seq1, x1, y1,
                                                                                          dir2, seq2, x2, y2)))


if __name__ == '__main__':
    main()

