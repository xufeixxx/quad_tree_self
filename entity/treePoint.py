class TreePoint:
    def __init__(self, tp_id, region, level, f_id):
        self.tp_id = tp_id
        self.tp_value = 0  # 四叉树重构的时候使用
        self.region = region
        self.tp_level = level  # 此节点所在的层
        self.father_id = f_id
        self.tp_value_1 = 0
        self.tp_value_2 = 0
        """
        tp_value_1 and to_value_2 是树的后置化处理后的两个变量，区域查询将使用tp_value_2来进行。
        """