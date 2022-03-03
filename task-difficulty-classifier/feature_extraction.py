import json
from collections import Counter

import numpy as np
import pandas as pd
import ray

from tools.features import get_size_ratio
from tools.features import get_num_occlusion


@ray.remote
def get_feature_values(json_path:str, task_size:tuple):
    """Read json and get feature values from the file."""
    with open(json_path) as json_file:
        json_data = json.load(json_file)
        parent_path = json_data['parent_path']
        file_name = json_data['filename']
        annotations = json_data['annotations']

        n_instance = len(annotations)

        if not annotations:
            avg_size_ratio = 0
            avg_n_occlusion = 0
            labels = ['no_instance']

        else:
            size_list = []
            points_list = []
            labels = []
            for instance in annotations:
                points = instance['points']
                label = instance['label']
                size_ratio = get_size_ratio(points, task_size)
                points_list.append(points)
                size_list.append(size_ratio)
                labels.append(label)

            n_occlusion_list = get_num_occlusion(points_list)

            avg_size_ratio = np.round(np.array(size_list).mean(), 2)
            avg_n_occlusion = np.round(np.array(n_occlusion_list).mean(), 2)

    df_values = pd.DataFrame(
        {
            'folder': parent_path,
            'file_name': file_name,
            'n_instance': n_instance,
            'avg_size_ratio': avg_size_ratio,
            'avg_n_occlusion': avg_n_occlusion,
            'labels': [labels]
        }, index=[0]
    )

    return df_values