import pandas


def load_files(file_list):
    pair_df = pandas.DataFrame()
    for file in file_list:
        df = file_pair_reader(file)
        pair_df = pair_df.append(df)
    return pair_df


def file_pair_reader(filename):
    df = pandas.read_csv(filename,
                         sep=' ',
                         comment='%',
                         header=None)
    df = df.ix[:, [2, 3, 6, 7]]
    df = df.rename(columns={2: 'dir1', 3: 'file1', 6: 'dir2', 7: 'file2'})
    return df


