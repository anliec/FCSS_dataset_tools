import pandas as pd
import sqlite3
import csv
import os
import shutil
import argparse

src_file = "/cs-share/pradalier/lake/pairs/image_pairs.csv"
base_path = "/cs-share/pradalier/lake/VBags"


def register_directory(d):
    df = pd.read_csv(os.path.join(base_path, d, "image_auxilliary.csv"), sep=',', header=0)
    df = df[['seq', 'x', 'y']]
    df = df.assign(dir=[d] * df.shape[0])
    df.to_sql('aux', con, if_exists='append')


def get_gps_coord(d, seq):
    try:
        query = con.execute("SELECT count(*) FROM aux WHERE dir = ?;", (d,))
        if int(query.fetchone()[0]) == 0:
            register_directory(d)
    except sqlite3.OperationalError:
        register_directory(d)

    query = con.execute("SELECT x, y FROM aux WHERE dir = ? AND seq = ?;", (d, seq + ".000000"))
    return query.fetchone()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-directory',
                        default='/tmp/data',
                        type=str,
                        dest="output_directory")
    args = parser.parse_args()

    # create dataset directory (fail if they exist)
    os.makedirs(args.output_directory)
    os.makedirs(os.path.join(args.output_directory, "test/left/1"))
    os.makedirs(os.path.join(args.output_directory, "test/right/1"))
    os.makedirs(os.path.join(args.output_directory, "train/left/1"))
    os.makedirs(os.path.join(args.output_directory, "train/right/1"))

    con = sqlite3.connect(":memory:")

    tuple_list = []
    x_sum = 0.0
    x_count = 0
    y_sum = 0.0
    y_count = 0

    with open(src_file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            dir1, seq1, dir2, seq2 = row
            x1, y1 = get_gps_coord(dir1, seq1)
            x2, y2 = get_gps_coord(dir2, seq2)
            tuple_list.append(((dir1, seq1, x1, y1), (dir2, seq2, x2, y2)))
            x_sum += float(x1) + float(x2)
            x_count += 2
            y_sum += float(y1) + float(y2)
            x_count += 2

    x_avg = x_sum / x_count
    y_avg = y_sum / y_count

    for (dir1, seq1, x1, y1), (dir2, seq2, x2, y2) in tuple_list:
        if x1 < x_avg:
            dataset = "train"
        else:
            dataset = "test"

        shutil.copyfile(src=os.path.join(base_path,
                                         dir1,
                                         "{:0=4d}/{:0=4d}.png".format(seq1[:-3], seq1[-3:])),
                        dst=os.path.join(args.output_directory,
                                         dataset,
                                         "left/1/{}_{}_{}_{}.png".format(dir1, seq1, x1, y1)))
        shutil.copyfile(src=os.path.join(base_path,
                                         dir2,
                                         "{:0=4d}/{:0=4d}.png".format(seq2[:-3], seq2[-3:])),
                        dst=os.path.join(args.output_directory,
                                         dataset,
                                         "left/1/{}_{}_{}_{}.png".format(dir2, seq2, x2, y2)))



