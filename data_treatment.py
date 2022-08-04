# This Python file uses the following encoding: utf-8
import math
import pandas as pd
import numpy as np
from copy import deepcopy as dcp
from math import log
from operation_model import Microplastic, Retention

water = pd.read_csv("water.csv").iloc[21::, 1]
wave_arr = np.array(pd.read_csv("water.csv").iloc[21::, 0], dtype=np.double)
water_460 = pd.read_csv("water_460.csv").iloc[21::, 1]
wave_arr_460 = np.array(pd.read_csv("water_460.csv").iloc[21::, 0], dtype=np.double)


class Plastic(object):
    # Unify the class attribute wavelength format to DataFrame
    fic_table = pd.DataFrame(wave_arr)
    fic_table_460 = pd.DataFrame(wave_arr_460)

    @classmethod
    def plastic_data(cls, kind, save=None, path=None):
        """
        :description: 荧光强度-波长正态分布数据
        :param kind: MPs/NPs的改性类型
        :param save: excel数据保存路径
        :param path: 将从荧光仪取得的数据文件(.csv)路径进行按顺序存储进列表path传入
        :return:
        """

        # 防止对类属性进行叠加，对其进行深拷进行使用
        global water
        if kind == "null":
            new_fic_table = dcp(cls.fic_table_460)
            water = water_460
        else:
            new_fic_table = dcp(cls.fic_table)

        # fic用来存储后续差分矩阵得到的新的每一列即每个浓度的新数据
        fic = []

        if path is None:
            plastic = []
        else:
            plastic = path

        # 先将水的荧光强度与每种浓度的荧光强度合并为一个表
        # 对表进行类型转换为矩阵，且数据类型是double
        # 利用差分矩阵直接后者减前者得到新的矩阵数据后再转回DataFrame
        # 将新的DataFrame的数据存入列表fic
        for temp in plastic:
            mini_fic = []
            for i in temp:
                data = pd.concat([water, pd.read_csv(i).iloc[21::, 1]],
                                 axis=1, join="outer", ignore_index=True)
                arr = np.array(data, dtype=np.double)
                new_arr = np.diff(arr)
                table = pd.DataFrame(new_arr)
                mini_fic.append(table)
            fic.append(mini_fic)

        # 波长列与每种浓度的数据列整合为一个大table
        for i in range(len(fic)):
            for j in range(len(fic[i])):
                new_fic_table = pd.concat([new_fic_table, fic[i][j]],
                                          axis=1, join="outer", ignore_index=True)
        if kind:
            if save:
                save_path = "".join(["D:\\ZGJ\\SR_DATA\\", save, "\\%s\\%s.xlsx" % (kind, kind)])
            # 将new_fic_table以excel的形式保存到下列路径中
                new_fic_table.to_excel(save_path)
        # 返回这个table
        return new_fic_table

"""
*****************************************************************************************************************************************************
以下为同一种气凝胶对不同浓度的微纳塑料溶液开始过滤实验
故path的取值与上述不同，是不同浓度的微纳塑料溶液得到的滤液的荧光强度数据
"""

class Filtration(object):
    @classmethod
    def concentration(cls, path:list, kind, emission_wavelength, a, b):
        # 仿照Plastic对path传进来的数据作差分矩阵运算
        # 此时整个data表的行索引依旧是波长，而列索引变成了微纳塑料浓度梯度(由小到大)
        data = Plastic.plastic_data(kind, save=None, path=path)
        wave_length = list(data.iloc[::, 0])
        y = []

        # 以发射波长为准，选取发射波长处的荧光强度
        # 将时间梯度中的每种荧光强度存储进y
        ind = 1
        for val in wave_length:
            if val == emission_wavelength:
                val_index = wave_length.index(val)
                for i in range(len(path)):
                    for j in range(len(path[i])):
                        y.append(data.iloc[val_index, ind])
                        ind += 1
                break
        cnc = []
        # 利用拟合直线y=ax+b算出时间梯度中微纳塑料的每种浓度，并存入cnc列表
        for round in y:
            cnc.append((round - b) / a)
        return cnc

    @classmethod
    def retention_rate(cls, path:list, emission_wavelength, a, b, c0:list, save=None, kind=None):
        cn = cls.concentration(path, kind, emission_wavelength, a, b)
        retention = []
        mini_retention = []
        ind = 0
        for i in range(len(path)):
            for j in range(len(path[i])):
                mini_retention.append((1 - cn[ind] / c0[i]) * 100)
            retention.append(mini_retention)
            mini_retention = []
            ind += 1
            if kind:
                if save:
                    save_path = "".join(["D:\\ZGJ\\SR_DATA\\", save, "\\%d.xlsx" % c0[i]])
                    retention_table = pd.DataFrame(retention)
                    retention_table.to_excel(save_path)

        return retention


if __name__ == "__main__":
    data1 = Plastic.plastic_data("amino", path=[["./amino/1.csv"], ["./amino/2.csv"], ["./amino/5.csv"],
                                      ["./amino/10.csv"], ["./amino/20.csv"], ["./amino/40.csv"],
                                      ["./amino/60.csv"], ["./amino/80.csv"]])
    a1, b1 = Microplastic.plot_fic_lc(data1, 518, 9, [1, 2, 5, 10, 20, 40, 60, 80], "amino", "English", [0, 100], [0, 100])
    c1 = Filtration.retention_rate([["amino_filtration/TEMPO/1.281%/15ppm.csv"]], 518, a1, b1, [15], save=None, kind="amino")
    c1[0].append(60.89)
    # save = "M_1\\2st\\filtration\\20220731\\amino\\", kind = "TEMPO\\1.281%"
    data2 = Plastic.plastic_data("carboxyl", path=[["./carboxyl/1.csv"], ["./carboxyl/2.csv"], ["./carboxyl/5.csv"],
                                      ["./carboxyl/10.csv"], ["./carboxyl/20.csv"], ["./carboxyl/40.csv"],
                                      ["./carboxyl/60.csv"], ["./carboxyl/80.csv"]])
    a2, b2 = Microplastic.plot_fic_lc(data2, 518, 9, [1, 2, 5, 10, 20, 40, 60, 80], "carboxyl", "English", [0, 100], [0, 100])
    c2 = Filtration.retention_rate([["carboxyl_filtration/TEMPO/1.281%/15ppm.csv"]], 518, a2, b2, [15], save=None, kind="carboxyl")
    c2[0].append(12.33)
    data3 = Plastic.plastic_data("null", path=[["./null/1.csv"], ["./null/2.csv"], ["./null/5.csv"],
                                      ["./null/10.csv"], ["./null/20.csv"], ["./null/40.csv"],
                                      ["./null/60.csv"], ["./null/80.csv"]])
    a3, b3 = Microplastic.plot_fic_lc(data3, 518, 9, [1, 2, 5, 10, 20, 40, 60, 80], "null", "English", [0, 100], [0, 100])
    c3 = Filtration.retention_rate([["null_filtration/TEMPO/1.281%/15ppm.csv"]], 518, a3, b3, [15], save=None, kind="null")
    c3[0].append(6.28)
    c = c1 + c2 + c3
    print(c)
    Retention.plastic_kind_plot_retention(["PS(+)", "PS(-)", "PS"], c, "TEMPO", "English", ["PS(+)", "PS(-)", "PS"], save="sss.png")
