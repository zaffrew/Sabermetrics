import pandas as pd
import numpy as np

from pybaseball import pitching_stats


def fan_graphs_stats(range, stats):

    # extracting year from start date
    start_str = range[0]
    start = start_str[:4]

    # extracting year from end date
    end_str = range[1]
    end = end_str[:4]

    # get pitching_stats for specific range given
    pitch_stats = pitching_stats(start, end)
    pitch_stats_df = pd.DataFrame(pitch_stats)
    headersList = pitch_stats_df.columns
    headers = np.asarray(headersList)

    # drop columns that are in the input stats array
    keep_stats = []
    index = []
    count = 0
    for i in stats:
        for j in headers:
            if j == i:
                index.insert(len(index) + 1, count)
                keep_stats.insert(len(keep_stats) + 1, j)
            count = count + 1
        count = 0

    drop_cols = np.delete(headers, index)
    drop = np.asarray(drop_cols)

    # drop the columns from pitching stats with these names
    pitch_stats_df = pitch_stats_df.drop(columns=drop)
    return pitch_stats_df


