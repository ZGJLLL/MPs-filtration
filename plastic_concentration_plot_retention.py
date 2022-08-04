# This Python file uses the following encoding: utf-8
from data_treatment import Plastic, Filtration
from operation_model import Microplastic, Retention

if __name__ == "__main__":
    grade = "M_1/2st"
    t = "amino"
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
    c = [5, 15, 25]
    c_num = 1  # 每种微纳塑料做了一组实验为1，做了两组实验为2
    c_label = ["5ppm", "15ppm", "25ppm"]
    AG_kind = "TEMPO"
    AG_concentration = "/1.281%/"
    # retention_data_save = "".join([grade, "\\filtration\\20220731\\", t, "\\", AG_kind, AG_concentration])
    retention_data_save = None
    path = []
    for i in c:
        mini_path = []
        for j in range(c_num):
            mini_path.append("".join([t, "_filtration/", AG_kind, AG_concentration, str(i), "ppm/", str(j + 1), ".csv"]))
        path.append(mini_path)
    r = Filtration.retention_rate(path, emission_wavelength, a, b, c, save=retention_data_save, kind=t)
    print(r)
    Retention.plastic_concentration_plot_retention(c, r, t, "English", c_label)