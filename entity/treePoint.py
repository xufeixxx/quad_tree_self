class TreePoint:
    def __init__(self, tp_id, region, level, f_id):
        self.tp_id = tp_id
        self.tp_value = 0  # 四叉树重构的时候使用
        self.region = region
        self.tp_level = level  # 此节点所在的层
        self.father_id = f_id
