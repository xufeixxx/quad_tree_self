import pandas as pd
import numpy as np
from overall.setting import Setting
from overall.list import leaf_point_list, non_leaf_point_list

setts = Setting()
np_data = None
g_id = 1


def read_dataSet():  # 读取数据集
    global np_data
    data = pd.read_csv('storage.csv')  # 返回一个DataFrame
    x = data.loc[:, 'X']
    y = data.loc[:, 'Y']
    setts.x1 = min(x)
    setts.x2 = max(x)
    setts.y1 = min(y)
    setts.y2 = max(y)
    np_data = np.array(data)
    return np_data


# def from_xy_get_leaf_point_id(x, y):  # 根据点的坐标确定所处叶子节点的id,没考虑递归实现是错的,一晚上努力白费了--
#     level = setts.quad_tree_level
#     x1 = setts.x1
#     x2 = setts.x2
#     y1 = setts.y1
#     y2 = setts.y2
#     num_cells_each_row = np.power(2, level - 1)
#     num_of_non_leaf_point = 1/3*(np.power(4, level - 1) - 1)
#     cell_num_x = np.linspace(x1, x2, num_cells_each_row + 1)
#     cell_num_y = -np.sort(-np.linspace(y1, y2, num_cells_each_row + 1))
#     # for x_num,i in zip(cell_num_x, range(len(cell_num_x))):
#     x_position = None
#     y_position = None
#     for i in range(len(cell_num_x)):
#         if cell_num_x[i] <= x <= cell_num_x[i+1]:
#             x_position = i + 1
#             break
#     for i in range(len(cell_num_y)):
#         if cell_num_y[i] >= y >= cell_num_y[i+1]:
#             y_position = i + 1
#             break
#     # return (y_position - 1) * num_cells_each_row + x_position + num_of_non_leaf_point
#     k = (y_position - 1)//2 * 2 * num_cells_each_row
#     new_y_position = y_position - (2 * ((y_position - 1)//2))
#     num = None
#     if x_position % 2 == 0:
#         if new_y_position == 1:
#             num = (x_position - 2)/2 * 4 + 2
#         elif new_y_position == 2:
#             num = x_position * 2
#     else:
#         if new_y_position == 1:
#             num = (x_position - 1)/2 * 4 + 1
#         elif new_y_position == 2:
#             num = x_position * 2 + 1
#
#     return num + k + num_of_non_leaf_point


def from_xy_get_leaf_point_id(x, y, x1, x2, y1, y2, h):  # 时间复杂度O(logn), n个点就是O(nlogn),如果两次for循环时O(n^2)
    global g_id
    if h != 1:
        xb = (x2 - x1) / 2
        yb = (y2 - y1) / 2
        if x1 <= x <= x1 + xb and y1 + yb <= y <= y2:
            g_id = g_id * 4 - 2
            from_xy_get_leaf_point_id(x, y, x1, x1 + xb, y1 + yb, y2, h - 1)
        elif x1 + xb <= x <= x2 and y1 + yb <= y <= y2:
            g_id = g_id * 4 - 1
            from_xy_get_leaf_point_id(x, y, x1 + xb, x2, y1 + yb, y2, h - 1)
        elif x1 <= x <= x1 + xb and y1 <= y <= y1 + yb:
            g_id = g_id * 4
            from_xy_get_leaf_point_id(x, y, x1, x1 + xb, y1, y1 + yb, h - 1)
        elif x1 + xb <= x <= x2 and y1 <= y <= y1 + yb:
            g_id = g_id * 4 + 1
            from_xy_get_leaf_point_id(x, y, x1 + xb, x2, y1, y1 + yb, h - 1)


def xy_get_id(x, y, x1, x2, y1, y2, h):  # 返回坐标所在叶节点的id
    global g_id
    from_xy_get_leaf_point_id(x, y, x1, x2, y1, y2, h)
    id = g_id
    g_id = 1
    return id
"""
递归实现查找坐标的叶子节点id，在xy_get_id函数中返回一个全局变量g_id.
"""


def tp_value_set_one(x, y):
    l = []
    tp_id = xy_get_id(x, y, setts.x1, setts.x2, setts.y1, setts.y2, setts.quad_tree_level)
    l.append(tp_id)
    f_id = leaf_point_list[tp_id].father_id
    while f_id != '#':
        l.append(f_id)
        f_id = non_leaf_point_list[f_id].father_id
    return np.sort(np.array(l, dtype=float))


def rand_select_level_and_send_list(one_point_list):
    n_level = np.random.randint(1, setts.quad_tree_level + 1)  # 随机选择第几层
    num_of_point_in_level = np.power(4, n_level - 1)
    num_point_out_of_n_level = 1 / 3 * (np.power(4, n_level - 1) - 1)  # 1到n_level-1所有层次节点的总数
    # num_point_of_n_level = 1/3 * (np.power(4, n_level) - 1)  # n_level层所有节点的总数
    n = one_point_list[n_level - 1]
    k = int(n - num_point_out_of_n_level)
    oz = np.zeros((1, num_of_point_in_level))[0]
    oz[k - 1] = 1
    return oz, n_level


def disturbance(x):
    if x == 1:
        if np.random.uniform(0, 1) <= 1 / 2:
            x = 1
        else:
            x = 0
    elif x == 0:
        if np.random.uniform(0, 1) <= np.exp(setts.epsilon) / (1 + np.exp(setts.epsilon)):
            x = 0
        else:
            x = 1
    return x


def add_noise_list_and_h(one_point_list):
    oz_list, h = rand_select_level_and_send_list(one_point_list)
    new_oz_list = list(map(disturbance, oz_list))
    return new_oz_list, h
