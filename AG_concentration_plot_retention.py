# This Python file uses the following encoding: utf-8
from data_treatment import Plastic, Filtration
from operation_model import Microplastic, Retention

if __name__ == "__main__":
    grade = "M_1/2st"
    t = "amino"
    AG = "TEMPO"
    # MPs/NPs
    c = [1, 2, 5, 10, 20, 40, 60, 80]
    c_num = 9
    emission_wavelength = 518
    x_limit = [0, 81]
    y_limit = [0, 125]
    # data_save_path = "M_1\\2st\\PSMPs\\20220718"
    data_save_path = None
    # s1 = "".join([t, "_png/", grade,"/荧光强度-波长正态分布曲线图.png"])
    # s2 = "".join([t, "_png/", grade,"/荧光强度-浓度拟合直线图.png"])
    s1 = None
    s2 = None
    path = []
    c_label = []
    for ind, val in enumerate(c):
        mini_path = []
        mini_path.append("".join([t, "/", str(val), ".csv"]))
        path.append(mini_path)
    for i in c:
        c_label.append("".join([str(i), "mg/L"]))
    a = 0
    b = 0
    try:
        # 导入浓度梯度下的微纳塑料母液荧光强度数据, 并完成差分矩阵运算处理
        data = Plastic.plastic_data(t, data_save_path, path)
        # 8要比绘制的点(条)数多1, 荧光强度-波长正态分布曲线图
        Microplastic.plot_fic_sc(data, c_num, t, "English", c_label, y_limit, s1)
        # 8要比绘制的点(条)数多1, 荧光强度-浓度拟合直线图，返回斜率a和截距b
        a, b = Microplastic.plot_fic_lc(data, emission_wavelength, c_num, c, t, "English", x_limit, y_limit, s2)
    except Exception as result:
        print("请检查微塑料数据！%s" % result)
    """
    ------------------------------------------------------------------------------------------------------------------------
    """
    # Retention
    c = [15]  # 某种浓度下的微纳塑料溶液
    c_num = 1  # 每种微纳塑料做了一组实验为1，做了两组实验为2
    c_label = ["1.281%", "1%", "0.8%"]
    AG_concentration1 = "/1.281%/"
    AG_concentration2 = "/1%/"
    AG_concentration3 = "/0.8%/"
    plastic_concentration = "15ppm/"
    # retention_data_save_1281 = "".join([grade, "\\filtration\\20220731\\", t, "\\", AG, AG_concentration1])
    # retention_data_save_1 = "".join([grade, "\\filtration\\20220731\\", t, "\\", AG, AG_concentration2])
    # retention_data_save_08 = "".join([grade, "\\filtration\\20220731\\", t, "\\", AG, AG_concentration3])
    retention_data_save_1281 = None
    retention_data_save_1 = None
    retention_data_save_08 = None
    path1 = []
    for ind in range(c_num):
        mini_path = []
        mini_path.append(
            "".join([t, "_filtration/", AG, AG_concentration1, plastic_concentration, str(ind + 1), ".csv"]))
        path1.append(mini_path)
    path2 = []
    for ind in range(c_num):
        mini_path = []
        mini_path.append(
            "".join([t, "_filtration/", AG, AG_concentration2, plastic_concentration, str(ind + 1), ".csv"]))
        path2.append(mini_path)
    path3 = []
    for ind in range(c_num):
        mini_path = []
        mini_path.append(
            "".join([t, "_filtration/", AG, AG_concentration3, plastic_concentration, str(ind + 1), ".csv"]))
        path3.append(mini_path)
    r1 = Filtration.retention_rate(path1, emission_wavelength, a, b, c, save=retention_data_save_1281, kind=t)
    r1[0].append(60.89)
    r2 = Filtration.retention_rate(path2, emission_wavelength, a, b, c, save=retention_data_save_1, kind=t)
    r2[0].append(68.28)
    r3 = Filtration.retention_rate(path3, emission_wavelength, a, b, c, save=retention_data_save_08, kind=t)
    r3[0].append(42.33)
    r = r1 + r2 + r3
    print(r)
    Retention.plot_retention(r, "".join([AG, "-", t]), "English", c_label, save="bbb.png")