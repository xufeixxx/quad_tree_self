from entity.treePoint import TreePoint
from function.makeChildNodes import make_child_nodes
from overall.setting import Setting
from overall.list import leaf_point_list, non_leaf_point_list
import numpy as np

setts = Setting()


def make_quad_tree(x1, x2, y1, y2):
    root_tree_point = TreePoint(1, np.array([x1, x2, y1, y2], dtype=float), 1, '#')  # 四叉树根节点没有父节点，标记为'#'
    if root_tree_point.tp_level == setts.quad_tree_level:
        leaf_point_list[root_tree_point.tp_id] = root_tree_point
    else:
        non_leaf_point_list[root_tree_point.tp_id] = root_tree_point
        make_child_nodes(root_tree_point)


"""
此满四叉树根据一定的规律构建的，首先从根节点开始，非根节点从左到右标记，从1开始（根节点为1）。
这些数为节点的id，节点的属性包括节点id，节点代表的区域，父节点id，节点的值（伯努利）以及节点
所在树的层（从上到下，从1开始）。之所以没有将每个节点（叶节点除外）的子节点的id，作为
一个属性的原因是这个属性对此实验的用处不大，即使加上这个属性，找子节点或者父节点的时候
也用不上。因为为了减少时间复杂度会尽量避免遍历四叉树。我们根据公式来判定一个节点的父节点
或者子节点。这样时间复杂度会是O(1)。
公式：
父节点找子结点：
父节点id = f_id, --> 子节点id：f_id*4-2, f_id*4-1, f_id*4, f_id+1。（规律：如果按层标记，父节点的第三个子节点的id一定是
父节点id的四倍，其他的三个节点各异一次推出来）
子节点找父节点：
根据father_id属性可以得到父节点id下面是公式推到：
根据上面的规律可以退出子节点找父节点的规律：
子节点id = s_id。如果s_id可以整除4，那么除4的结果就是父节点的id。如果不是的话，分别进行+1，+2，-1，那个可以整除4，
那么结果就是父节点的id。
------|------
|     |     |
|   1 |   2 |
|-----|-----|
|     |     |
|   3 |   4 |
------|------ 
父节点的四个子节点的区域顺序是上图那样表示的。
"""
