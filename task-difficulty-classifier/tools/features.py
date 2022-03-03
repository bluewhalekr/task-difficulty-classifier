from itertools import combinations

import numpy as np
from shapely.geometry import Point
from shapely.geometry import Polygon


def get_size_ratio(points:list, pic_size:tuple, ceiling:int=5):
    """Calculate the instance size ratio.
    Limit the ratio at 5% of the picture and reverse the ratio.

    Args:
        points (list): [[x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max]]
        pic_size (tuple): (width, height)
        ceiling (int): limit ratio
        
    Returns:
        size_ratio (float)
    """
    x_min, y_min = points[0][0], points[0][1]
    x_max, y_max = points[2][0], points[2][1]
    instance_size = (x_max - x_min) * (y_max - y_min)
    pic_size = pic_size[0] * pic_size[1]
    size_ratio = np.round(((instance_size / pic_size) * 100), 2)

    if size_ratio > ceiling:
        size_ratio = ceiling

    size_ratio = ceiling - size_ratio
    
    return size_ratio


def get_num_occlusion(points:list):
    """Count occlused instances.

    Args Example:
        [
            [[x1_min, y1_min], [x1_max, y1_min], [x1_max, y1_max], [x1_min, y1_max]],
            [[x2_min, y2_min], [x2_max, y2_min], [x2_max, y2_max], [x2_min, y2_max]],
            ...
            [[xn_min, yn_min], [xn_max, yn_min], [xn_max, yn_max], [xn_min, yn_max]]
        ]

    Returns: (list)
        occlused instance numbers of each instance
    """
    n_points = len(points)

    idx_combination = list(combinations(range(n_points), 2))
    cnt_list = [0 for idx in range(n_points)]
    for idx_1, idx_2 in idx_combination:
        p1, p2 = Polygon(points[idx_1]), Polygon(points[idx_2])
        intersection_area = p1.intersection(p2).area
        if intersection_area > 0:
            cnt_list[idx_1] += 1
            cnt_list[idx_2] += 1
    return cnt_list