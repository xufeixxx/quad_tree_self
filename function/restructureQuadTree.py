from overall.list import leaf_point_list, non_leaf_point_list
from overall.setting import Setting
import numpy as np
setts = Setting()
tree_level = setts.quad_tree_level


def restructure_quad_tree(oz_list, h):
    if tree_level == h:
        for i, x in zip(leaf_point_list, oz_list):
            leaf_point_list[i].tp_value += x
    else:
        num_of_point_top_h = 1 / 3 * (np.power(4, h - 1) - 1)
        num_of_point_in_level = np.power(4, h - 1)
        for i, x in zip(range(int(num_of_point_top_h + 1), num_of_point_in_level + 1), oz_list):
            non_leaf_point_list[i].tp_value += x

