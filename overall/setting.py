class Setting:
    def __init__(self):
        self.quad_tree_level = 4  # 四叉树的层数，1024 * 1024应该为11层
        self.x1 = 0
        self.x2 = 16
        self.y1 = 0
        self.y2 = 16
        self.epsilon = 0.5
        # 整个区域的边界
