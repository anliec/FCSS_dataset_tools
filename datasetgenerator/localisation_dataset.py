import pandas as pd
import sqlite3
import csv
import os
import shutil
import argparse
import numpy as np
import itertools
from multiprocessing import Pool

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
    os.makedirs(os.path.join(args.output_directory, "localisation/left/1"))
    os.makedirs(os.path.join(args.output_directory, "localisation/right/1"))
    tuple_list = []

    pool = Pool()

    with open(src_file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        xy_it = pool.imap_unordered(manage_csv_row, zip(csv_reader, itertools.repeat(base_path)), chunksize=250)
        for x, y, t in xy_it:
            if x is None:
                continue
            tuple_list.append(t)

    group_generated = 0

    for (dir1, seq1, x1, y1), (dir2, seq2, x2, y2) in tuple_list:
        if abs(float(x1) - float(x2)) > args.gps_max_distance or abs(float(y1) - float(y2)) > args.gps_max_distance:
            print("GPS check failed, skipping pair")
            continue

        if 10 < (int(seq1) % 1000) < 990 and 10 < (int(seq2) % 1000) < 990:
            group_generated += 1
            for offset1 in range(-10, 11):
                file1_name = "{:0=4d}.jpg".format(int(seq1) % 1000 + offset1)
                for offset2 in range(-10, 11):
                    file2_name = "{:0=4d}.jpg".format(int(seq2) % 1000 + offset2)

                    shutil.copyfile(src=os.path.join(base_path, "VBags",
                                                     dir1,
                                                     "{:0=4d}".format(int('0' + seq1[:-3])),
                                                     file1_name),
                                    dst=os.path.join(args.output_directory,
                                                     "localisation",
                                                     "left/1/{}_{}_{}_{}_{}_{}_{}_{}_{}_{}.jpg".format(dir1, seq1, x1,
                                                                                                       y1, offset1,
                                                                                                       dir2, seq2, x2,
                                                                                                       y2, offset2)))
                    shutil.copyfile(src=os.path.join(base_path, "VBags",
                                                     dir2,
                                                     "{:0=4d}".format(int('0' + seq2[:-3])),
                                                     file2_name),
                                    dst=os.path.join(args.output_directory,
                                                     "localisation",
                                                     "right/1/{}_{}_{}_{}_{}_{}_{}_{}_{}_{}.jpg".format(dir1, seq1, x1,
                                                                                                        y1, offset1,
                                                                                                        dir2, seq2, x2,
                                                                                                        y2, offset2)))

        if group_generated == args.number_of_groups:
            break


if __name__ == '__main__':
    main()

