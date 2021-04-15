from overall.list import leaf_point_list, non_leaf_point_list
from overall.setting import Setting
import numpy as np
setts = Setting()
tree_level = setts.quad_tree_level


def restructure_quad_tree(oz_list, h):
    if tree_level == h:
        for i, x in zip(leaf_point_list, oz_list):
            leaf_point_list[i].tp_value += x
            leaf_point_list[i].tp_value_1 = leaf_point_list[i].tp_value
            leaf_point_list[i].tp_value_2 = leaf_point_list[i].tp_value
    else:
        num_of_point_top_h = int(1 / 3 * (np.power(4, h - 1) - 1))
        num_of_point_in_level = np.power(4, h - 1)
        for i, x in zip(range(num_of_point_top_h + 1, num_of_point_in_level + num_of_point_top_h + 1), oz_list):
            non_leaf_point_list[i].tp_value += x


def tree_average_treatment():  # tp_value_1
    h = tree_level - 1
    while h != 0:
        num_of_point_top_h = int(1 / 3 * (np.power(4, h - 1) - 1))
        num_of_point_in_level = np.power(4, h - 1)
        for i in range(num_of_point_top_h + 1, num_of_point_in_level + num_of_point_top_h + 1):
            point = non_leaf_point_list[i]
            if h == tree_level - 1:
                sv1 = leaf_point_list[4 * i - 2].tp_value_1
                sv2 = leaf_point_list[4 * i - 1].tp_value_1
                sv3 = leaf_point_list[4 * i].tp_value_1
                sv4 = leaf_point_list[4 * i + 1].tp_value_1
            else:
                sv1 = non_leaf_point_list[4 * i - 2].tp_value_1
                sv2 = non_leaf_point_list[4 * i - 1].tp_value_1
                sv3 = non_leaf_point_list[4 * i].tp_value_1
                sv4 = non_leaf_point_list[4 * i + 1].tp_value_1
            point.tp_value_1 = ((np.power(4, i) - np.power(4, i - 1)) / (np.power(4, i) - 1)) * point.tp_value \
                               + ((sv4 + sv1 + sv3 + sv2) * ((np.power(4, i - 1) - 1) / (np.power(4, i) - 1)))
        h -= 1


