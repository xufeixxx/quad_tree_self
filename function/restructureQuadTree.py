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
                sv1, sv2, sv3, sv4 = from_f_id_get_s_point_v1(i, leaf_point_list)
            else:
                sv1, sv2, sv3, sv4 = from_f_id_get_s_point_v1(i, non_leaf_point_list)
            point.tp_value_1 = ((np.power(4, i) - np.power(4, i - 1)) / (np.power(4, i) - 1)) * point.tp_value \
                               + ((sv4 + sv1 + sv3 + sv2) * ((np.power(4, i - 1) - 1) / (np.power(4, i) - 1)))
        h -= 1


def tree_mean_consistency():
    h = 1
    while h != tree_level:
        num_of_point_top_h = int(1 / 3 * (np.power(4, h - 1) - 1))
        num_of_point_in_level = np.power(4, h - 1)
        if h == 1:
            point = non_leaf_point_list[h]
            sv1, sv2, sv3, sv4 = from_f_id_get_s_point_v1(h, non_leaf_point_list)
            point.tp_value_2 = point.tp_value_1 + 1 / 4 * (-(sv1 + sv2 + sv3 + sv4))
            h += 1
        else:
            for i in range(num_of_point_top_h + 1, num_of_point_in_level + num_of_point_top_h + 1):
                point = non_leaf_point_list[i]
                if h == tree_level - 1:
                    sv1, sv2, sv3, sv4 = from_f_id_get_s_point_v1(i, leaf_point_list)
                else:
                    sv1, sv2, sv3, sv4 = from_f_id_get_s_point_v1(i, non_leaf_point_list)
                point.tp_value_2 = point.tp_value_1 + \
                                   1 / 4 * (non_leaf_point_list[point.father_id].tp_value_2 - (sv1 + sv2 + sv3 + sv4))
            h += 1


def from_f_id_get_s_point_v1(f_id, l_list):
    sv1 = l_list[4 * f_id - 2].tp_value_1
    sv2 = l_list[4 * f_id - 1].tp_value_1
    sv3 = l_list[4 * f_id].tp_value_1
    sv4 = l_list[4 * f_id + 1].tp_value_1
    return sv1, sv2, sv3, sv4
