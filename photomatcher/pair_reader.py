import pandas as pd
from pandas.errors import *
from multiprocessing import Pool


def load_files(file_list):
    pool = Pool()
    results = pool.imap_unordered(file_pair_reader, file_list, chunksize=1000)

    df_list = []
    for df in results:
        if df is not None:
            df_list.append(df)

    pair_df = pd.concat(df_list)
    return pair_df


def file_pair_reader(filename):
    i = filename.rfind('/') + 7
    date_list = filename[i:-4].split('_')
    try:
        df = pd.read_csv(filename,
                         sep=' ',
                         comment='%',
                         header=None,
                         engine='c')
    except (OSError, EmptyDataError):
        print("ERROR: unable to load file", filename)
        return None

    df = df.ix[:, [2, 3, 6, 7]]
    df = df.rename(columns={2: 'dir1', 3: 'file1', 6: 'dir2', 7: 'file2'})
    df = df.assign(date1=pd.Series([date_list[0]] * df.size))
    df = df.assign(date2=pd.Series([date_list[1]] * df.size))
    return df


