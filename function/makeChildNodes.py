import numpy as np
from entity.treePoint import TreePoint
from overall.setting import Setting
from overall.list import leaf_point_list, non_leaf_point_list

setts = Setting()


def make_child_nodes(treePoint):
    if treePoint.tp_level != setts.quad_tree_level:  # 非叶子节点
        f_id = treePoint.tp_id
        f_region = treePoint.region
        f_level = treePoint.tp_level
        x1 = f_region[0]
        x2 = f_region[1]
        y1 = f_region[2]
        y2 = f_region[3]
        x = (x2 - x1) / 2
        y = (y2 - y1) / 2
        for i in range(-2, 2, 1):
            s_id = f_id * 4 + i
            level = f_level + 1
            if i == -2:
                region = np.array([x1, x1 + x, y1 + y, y2], dtype=float)
            elif i == -1:
                region = np.array([x1 + x, x2, y1 + y, y2], dtype=float)
            elif i == 0:
                region = np.array([x1, x1 + x, y1, y1 + y], dtype=float)
            else:
                region = np.array([x1 + x, x2, y1, y1 + y], dtype=float)
            if level == setts.quad_tree_level:
                tp = TreePoint(s_id, region, level, f_id)
                leaf_point_list[s_id] = tp
            else:
                tp = TreePoint(s_id, region, level, f_id)
                non_leaf_point_list[s_id] = tp
                make_child_nodes(tp)
