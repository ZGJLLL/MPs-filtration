# This Python file uses the following encoding: utf-8
from data_treatment import Plastic, Filtration
from operation_model import Microplastic, Retention

if __name__ == "__main__":
    grade = "M_1\\2st"
    type1 = "amino"
    type2 = "carboxyl"
    type3 = "null"
    # MPs/NPs
    c = [1, 2, 5, 10, 20, 40, 60, 80]
    c_num = 9
    emission_wavelength_amino = 518
    emission_wavelength_carboxyl = 518
    emission_wavelength_null = 518
    x_amino_limit = [0, 81]
    y_amino_limit = [0, 125]
    x_carboxyl_limit = [0, 81]
    y_carboxyl_limit = [0, 125]
    x_null_limit = [0, 81]
    y_null_limit = [0, 125]
    # data_save_path = "M_1\\2st\\PSMPs\\20220718"
    data_save_path = None
    # s1 = "".join([type1, "_png/", grade,"/荧光强度-波长正态分布曲线图.png"])
    # s2 = "".join([type1, "_png/", grade,"/荧光强度-浓度拟合直线图.png"])
    # s3 = "".join([type2, "_png/", grade,"/荧光强度-波长正态分布曲线图.png"])
    # s4 = "".join([type2, "_png/", grade,"/荧光强度-浓度拟合直线图.png"])
    # s5 = "".join([type3, "_png/", grade,"/荧光强度-波长正态分布曲线图.png"])
    # s6 = "".join([type3, "_png/", grade,"/荧光强度-浓度拟合直线图.png"])
    s1 = None
    s2 = None
    s3 = None
    s4 = None
    s5 = None
    s6 = None
    c_label = []
    for i in c:
        c_label.append("".join([str(i), "mg/L"]))
    path1 = []
    for ind, val in enumerate(c):
        mini_path = []
        mini_path.append("".join([type1, "/", str(val), ".csv"]))
        path1.append(mini_path)
    path2 = []
    for ind, val in enumerate(c):
        mini_path = []
        mini_path.append("".join([type2, "/", str(val), ".csv"]))
        path2.append(mini_path)
    path3 = []
    for ind, val in enumerate(c):
        mini_path = []
        mini_path.append("".join([type3, "/", str(val), ".csv"]))
        path3.append(mini_path)
    a1 = 0
    b1 = 0
    a2 = 0
    b2 = 0
    a3 = 0
    b3 = 0

    try:
        # 导入浓度梯度下的微纳塑料母液荧光强度数据, 并完成差分矩阵运算处理
        data1 = Plastic.plastic_data(type1, data_save_path, path1)
        # 8要比绘制的点(条)数多1, 荧光强度-波长正态分布曲线图
        Microplastic.plot_fic_sc(data1, c_num, type1, "English", c_label, y_amino_limit, s1)
        # 8要比绘制的点(条)数多1, 荧光强度-浓度拟合直线图，返回斜率a和截距b
        a1, b1 = Microplastic.plot_fic_lc(data1, emission_wavelength_amino, c_num, c, type1, "English", x_amino_limit, y_amino_limit, s2)
        data2 = Plastic.plastic_data(type2, data_save_path, path2)
        Microplastic.plot_fic_sc(data2, c_num, type2, "English", c_label, y_carboxyl_limit, s3)
        a2, b2 = Microplastic.plot_fic_lc(data2, emission_wavelength_carboxyl, c_num, c, type2, "English", x_carboxyl_limit, y_carboxyl_limit, s4)
        data3 = Plastic.plastic_data(type3, data_save_path, path3)
        Microplastic.plot_fic_sc(data2, c_num, type2, "English", c_label, y_carboxyl_limit, s5)
        a3, b3 = Microplastic.plot_fic_lc(data3, emission_wavelength_carboxyl, c_num, c, type3, "English", x_carboxyl_limit, y_carboxyl_limit, s6)
    except Exception as result:
        print("请检查微塑料数据！%s" % result)

    """
    ------------------------------------------------------------------------------------------------------------------------
    """
    # Retention
    c = [15] # 某种浓度下的微纳塑料溶液
    c_num = 1 # 每种微纳塑料做了一组实验为1，做了两组实验为2
    c_label = ["PS(+)", "PS(-)", "PS"]
    AG = "QAS"
    AG_kind = "QAS/4_1"
    AG_concentration = "/0.819%/"
    plastic_concentration = "15ppm/"
    # retention_data_save_amino = "".join([grade, "\\filtration\\20220731\\", type1, "\\", AG_kind, AG_concentration])
    # retention_data_save_carboxyl = "".join([grade, "\\filtration\\20220731\\", type2, "\\", AG_kind, AG_concentration])
    # retention_data_save_null = "".join([grade, "\\filtration\\20220731\\", type3, "\\", AG_kind, AG_concentration])
    retention_data_save_amino = None
    retention_data_save_carboxyl = None
    retention_data_save_null = None
    path1 = []
    mini_path = []
    for ind in range(c_num):
        mini_path.append("".join([type1, "_filtration/", AG_kind, AG_concentration, plastic_concentration, str(ind + 1), ".csv"]))
    path1.append(mini_path)
    path2 = []
    mini_path = []
    for ind in range(c_num):
        mini_path.append("".join([type2, "_filtration/", AG_kind, AG_concentration, plastic_concentration, str(ind + 1), ".csv"]))
    path2.append(mini_path)
    path3 = []
    mini_path = []
    for ind in range(c_num):
        mini_path.append("".join([type3, "_filtration/", AG_kind, AG_concentration, plastic_concentration, str(ind + 1), ".csv"]))
    path3.append(mini_path)
    r1 = Filtration.retention_rate(path1, emission_wavelength_amino, a1, b1, c, save=retention_data_save_amino, kind=type1)
    r2 = Filtration.retention_rate(path2, emission_wavelength_carboxyl, a2, b2, c, save=retention_data_save_carboxyl, kind=type2)
    r3 = Filtration.retention_rate(path3, emission_wavelength_null, a3, b3, c, save=retention_data_save_null, kind=type3)
    r = r1 + r2 + r3
    print(r)
    Retention.plot_retention_bar(r, AG, "English", c_label, save="xxx.png")