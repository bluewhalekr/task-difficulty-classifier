import numpy as np
import pandas as pd

from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import MinMaxScaler
from scipy.spatial import distance


def group_by_num_instances(df:pd.DataFrame, threshold:float=0.3):
    gmm = GaussianMixture(n_components=3)
    predict = gmm.fit_predict(pd.DataFrame(df['n_instance']))
    df['group'] = predict

    grp_idx_in_order = df.groupby('group').mean().sort_values(by='n_instance').index

    bottom = df[df['group'] == grp_idx_in_order[0]].reset_index(drop=True)
    mid = df[df['group'] == grp_idx_in_order[1]].reset_index(drop=True)
    top = df[df['group'] == grp_idx_in_order[2]].reset_index(drop=True)
    
    del bottom['group']
    del mid['group']
    del top['group']

    return top, mid, bottom


def get_euclidean_distance(df:pd.DataFrame, mode:str):
    if mode == 'easy':
        reference_vector = np.array([0, 0, 0])
    elif mode == 'difficult':
        reference_vector = np.array([1, 1, 1])
    
    scaler = MinMaxScaler()
    scaled_matrix = scaler.fit_transform(
        df[['n_instance', 'avg_size_ratio', 'avg_n_occlusion']]
    )

    distance_list = []
    for file_vector in scaled_matrix:
        try:
            distance_ = distance.euclidean(reference_vector, file_vector)
            distance_list.append(distance_)
        except ValueError:
            # When file_vector is empty
            distance_list.append(None)
            pass
    df['distance'] = distance_list

    return df