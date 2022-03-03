import argparse
import os

import numpy as np
import pandas as pd
import ray

from tools.jsonfinder import get_json_paths
from tools.difficulty import group_by_num_instances
from tools.difficulty import get_euclidean_distance
from feature_extraction import get_feature_values
from toexcel import cvt_df_to_excel


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--root_path', type=str, required=True)
    parser.add_argument('-s', '--task_size', type=int, nargs='+', required=True)
    parser.add_argument('-n', '--n_cpus', type=int, default=1)

    parser.add_argument('-r', '--extract_ratio', type=float, default=0.20)
    parser.add_argument('-d', '--dst_path', type=str, required=True)
    parser.add_argument('-t', '--title', type=str, default='Project Summary')

    config = parser.parse_args()

    return config


def get_task_difficulty(df, extract_ratio:float=0.20):
    """Get task difficulty based on feature extracted dataframe.
    Tasks will be grouped by number of instances first 
    and adjust the result by euclidean distance.

    Args:
        df (pandas.DataFrame)
            Index:
                RangeIndex
            Columns:
                folder (str): parent path
                file_name (str): file name
                n_instance (int): number of instances
                avg_size_ratio (float): avg_size_ratio,
                avg_n_occlusion (float): avg_n_occlusion,
                labels (list): labels of the instances  # len(labels)=len(instances)
        extract_ratio (float): extracting ratio of difficult & easy group each
    """
    # Calculate number of instances to be extracted from difficult & easy group
    n_extract = int(np.round(len(df) * extract_ratio, 0))
    # Grouping tasks by number of instances in the pictures
    top, mid, bottom = group_by_num_instances(df)
    # Adjust the result within the group by euclidean distance based on avg_size_ratio & n_occlusion
    top = get_euclidean_distance(top, 'difficult').sort_values(by='distance')
    mid = get_euclidean_distance(mid, 'difficult').sort_values(by='distance')
    bottom = get_euclidean_distance(bottom, 'easy').sort_values(by='distance')

    if len(top) > n_extract:
        n_rearange = len(top) - n_extract
        high = top[:-n_rearange]
        intermediate = pd.concat([top[-n_rearange:], mid], axis=0)
    elif len(top) < n_extract:
        n_rearange = n_extract - len(top)
        intermediate = mid[n_rearange:]
        high = pd.concat([top, mid[:n_rearange]], axis=0)
    else:
        high, intermediate = top, mid

    if len(bottom) > n_extract:
        n_rearange = len(bottom) - n_extract
        low = bottom[:-n_rearange]
        intermediate = pd.concat([intermediate, bottom[-n_rearange:]], axis=0)
    elif len(bottom) < n_extract:
        n_rearange = n_extract - len(bottom)
        intermediate = intermediate[:-n_rearange]
        low = pd.concat([intermediate[-n_rearange:], low], axis=0)
    else:
        low = bottom
    
    high = high.assign(distance='high')
    intermediate = intermediate.assign(distance='intermediate')
    low = low.assign(distance='low')

    df_difficulty = pd.concat([high, intermediate, low], axis=0).reset_index(drop=True)
    df_difficulty = df_difficulty.rename(columns={'distance': 'difficulty'})

    n_instance_is_zero = df_difficulty[df_difficulty['n_instance']==0].index
    df_difficulty.loc[n_instance_is_zero, 'difficulty'] = 'low'

    print('STEP 2: CLASSIFYING TASK DIFFICULTY IS COMPLETED')

    return df_difficulty


if __name__ == '__main__':
    config = get_args()
    json_paths = get_json_paths(config.root_path)
    ray.init(num_cpus=config.n_cpus)
    df = ray.get(
        [get_feature_values.remote(j_path, tuple(config.task_size)) for j_path in json_paths]
    )
    df = pd.concat(df, axis=0)

    print('STEP 1: CREATING FILE FEATURES TABLE IS COMPLETED')

    df_classified = get_task_difficulty(df, config.extract_ratio)
    cvt_df_to_excel(df_classified, config.dst_path, config.title)