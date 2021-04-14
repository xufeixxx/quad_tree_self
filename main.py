import datetime
import profile
import numpy as np
from function.makeQuadTree import make_quad_tree
from overall.list import leaf_point_list, non_leaf_point_list
from function.quadTreeDisturbance import read_dataSet, add_noise_list_and_h
from function.quadTreeDisturbance import tp_value_set_one
from function.restructureQuadTree import restructure_quad_tree
from overall.setting import Setting

setts = Setting()


def main():
    start_time = datetime.datetime.now()

    make_quad_tree(setts.x1, setts.x2, setts.y1, setts.y2)

    # id_list = tp_value_set_one(6.200492036111823, 10.672587231353166)

    kk = np.random.uniform([0, 0], [16, 16], (5, 2))

    for i in range(5):
        id_list = tp_value_set_one(kk[i][0], kk[i][1])
        oz, h = add_noise_list_and_h(id_list)
        restructure_quad_tree(oz, h)
    print("HelloWorld!!")
    #
    # print("用时：", datetime.datetime.now() - start_time)


if __name__ == '__main__':
    profile.run('main()')