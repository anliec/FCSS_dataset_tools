import pandas as pd
import sqlite3
import csv
import os
import shutil
import argparse
import numpy as np
from multiprocessing import Pool

src_file = "/cs-share/pradalier/lake/pairs/image_pairs.csv"
base_path = "/cs-share/pradalier/lake/"


def get_gps_coord(d, seq, dataset_path=base_path):
    with open(os.path.join(dataset_path, "VBags", d, "image_auxilliary.csv"), mode='r') as d_file:
        reader = csv.reader(d_file)
        for line in reader:
            if line[1] == seq + ".000000":
                return line[2], line[3]
        raise ValueError("{} not fund in {}".format(seq, d))


def manage_csv_row(row):
    dir1, seq1, dir2, seq2 = row
    try:
        x1, y1 = get_gps_coord(dir1, seq1)
        x2, y2 = get_gps_coord(dir2, seq2)
        return float(x1) + float(x2), float(y1) + float(y2), ((dir1, seq1, x1, y1), (dir2, seq2, x2, y2))
    except ValueError as e:
        print(str(e))
        return None, None, None


def main():
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
    args = parser.parse_args()

    global base_path, src_file
    base_path = args.input_directory
    src_file = args.pair_file

    # create dataset directory (fail if they exist)
    os.makedirs(args.output_directory, exist_ok=True)
    os.makedirs(os.path.join(args.output_directory, "test/left/1"))
    os.makedirs(os.path.join(args.output_directory, "test/right/1"))
    os.makedirs(os.path.join(args.output_directory, "train/left/1"))
    os.makedirs(os.path.join(args.output_directory, "train/right/1"))
    tuple_list = []
    x_sum = 0.0
    x_count = 0
    y_sum = 0.0
    y_count = 0

    pool = Pool()

    with open(src_file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        xy_it = pool.imap_unordered(manage_csv_row, csv_reader, chunksize=250)
        for x, y, t in xy_it:
            if x is None:
                continue
            x_sum += x
            y_sum += y
            x_count += 2
            y_count += 2
            tuple_list.append(t)

    x_avg = x_sum / x_count
    y_avg = y_sum / y_count

    for (dir1, seq1, x1, y1), (dir2, seq2, x2, y2) in tuple_list:
        if float(x1) < x_avg:
            dataset = "train"
        else:
            dataset = "test"

        if abs(float(x1) - float(x2)) > args.gps_max_distance or abs(float(y1) - float(y2)) > args.gps_max_distance:
            print("GPS check failed, skipping pair")
            continue

        shutil.copyfile(src=os.path.join(base_path,
                                         dir1,
                                         "{:0=4d}/{:0=4d}.jpg".format(int('0' + seq1[:-3]), int(seq1[-3:]))),
                        dst=os.path.join(args.output_directory,
                                         dataset,
                                         "left/1/{}_{}_{}_{}_{}_{}_{}_{}.jpg".format(dir1, seq1, x1, y1,
                                                                                     dir2, seq2, x2, y2)))
        shutil.copyfile(src=os.path.join(base_path,
                                         dir2,
                                         "{:0=4d}/{:0=4d}.jpg".format(int('0' + seq2[:-3]), int(seq2[-3:]))),
                        dst=os.path.join(args.output_directory,
                                         dataset,
                                         "right/1/{}_{}_{}_{}_{}_{}_{}_{}.jpg".format(dir1, seq1, x1, y1,
                                                                                      dir2, seq2, x2, y2)))


if __name__ == '__main__':
    main()

