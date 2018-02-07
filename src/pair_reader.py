import pandas as pd


def load_files(file_list):
    pair_df = pd.DataFrame()
    for i, file in enumerate(file_list):
        print("loading file", i, "of", len(file_list))
        df = file_pair_reader(file)
        pair_df = pair_df.append(df)
    return pair_df


def file_pair_reader(filename):
    i = filename.rfind('/') + 7
    date_list = filename[i:-4].split('_')
    df = pd.read_csv(filename,
                     sep=' ',
                     comment='%',
                     header=None)
    df = df.ix[:, [2, 3, 6, 7]]
    df = df.rename(columns={2: 'dir1', 3: 'file1', 6: 'dir2', 7: 'file2'})
    df = df.assign(date1=pd.Series([date_list[0]] * df.size))
    df = df.assign(date2=pd.Series([date_list[1]] * df.size))
    return df


