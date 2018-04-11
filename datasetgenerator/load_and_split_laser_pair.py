import pandas as pd
import sqlite3


if __name__ == '__main__':
    src_file = "/cs-share/pradalier/lake/pairs/image_pairs.csv"
    out_file = "./pairs"

    laser_pairs = pd.read_csv(src_file, sep=',', header=None, names=['dir1', 'seq1', 'dir2', 'seq2'])



