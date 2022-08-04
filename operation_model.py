# This Python file uses the following encoding: utf-8
import math
from matplotlib import pyplot as plt, font_manager
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.metrics import r2_score
from time import localtime
from time import strftime
from scipy import optimize as op


class Microplastic(object):
    # 实例化一个线性拟合转换器
    line_model = LinearRegression()
    title_carboxyl_sc = {"English": "The fluorescence intensity/concentration standard curve of PS-COOH",
                   "Chinese": "PS-COOH的荧光强度-浓度标准曲线"}
    title_carboxyl_lc = {"English": "The fluorescence intensity/concentration linearity curve of PS-COOH",
                         "Chinese": "PS-COOH的荧光强度-浓度线性拟合曲线"}
    title_amino_sc = {"English": "The fluorescence intensity/concentration standard curve of PS-NH$_{2}$",
                      "Chinese": "PS-NH$_{2}$的荧光强度-浓度标准曲线"}
    title_amino_lc = {"English": "The fluorescence intensity/concentration linearity curve of PS-NH$_{2}$",
                      "Chinese": "PS-NH$_{2}$的荧光强度-浓度线性拟合曲线"}
    title_null_sc = {"English": "The fluorescence intensity/concentration standard curve of PS",
                      "Chinese": "PS的荧光强度-浓度标准曲线"}
    title_null_lc = {"English": "The fluorescence intensity/concentration linearity curve of PS",
                      "Chinese": "PS的荧光强度-浓度线性拟合曲线"}
    title_list = [title_carboxyl_sc, title_amino_sc, title_carboxyl_lc, title_amino_lc, title_null_sc, title_null_lc]
    x_label_sc = {"English": "Wave length(nm)", "Chinese": "波长(nm)"}
    y_label_sc = {"English": "Fluorescence intensity", "Chinese": "荧光强度(10$^{4}$)"}
    x_label_lc = {"English": "Concentration(mg/L)", "Chinese": "浓度(mg/L)"}
    y_label_lc = {"English": "Fluorescence intensity", "Chinese": "荧光强度(10$^{4}$)"}

    # line_style = ['solid', (0, (5, 10)), (0, (1, 10)), (0, (3, 5, 1, 5)), (0, (3, 5, 1, 5, 1, 5)), 'dashed', 'dotted']

    @classmethod
    def plot_fic_sc(cls, deal_data, line_num, kind, key, legend_labels, y_limit, save=None):
        print(strftime("start --> %Y-%m-%d %H:%M:%S", localtime()))
        with plt.style.context(['science', 'nature', 'no-latex']):
            fig = plt.figure(figsize=(12, 10), dpi=180)
            x = deal_data.iloc[::, 0]
            _x = [i for i in range(len(x))]
            line_list = []

            i = 0
            while i < line_num:
                if i == 0:
                    i += 1
                    continue
                y = deal_data.iloc[::, i]
                # if i < len(cls.line_style) + 1:
                #     line = plt.plot(_x, y / 10000, ls=cls.line_style[i - 1])
                # else:
                line = plt.plot(_x, y / 10000)

                line_list.append(line)
                i += 1

            _xtick_labels = [i for i in range(int(x[0]), int(x[len(x) - 1]) + 1)]
            intervals = (x[len(x) - 1] - x[0]) / 10
            plt.xticks(_x[::int(intervals)], _xtick_labels[::int(intervals)])
            if kind == "amino":
                plt.title(cls.title_list[1][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            elif kind == "carboxyl":
                plt.title(cls.title_list[0][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            elif kind == "null":
                plt.title(cls.title_list[4][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            else:
                print("请输入正确信息！")
                return

            plt.xlabel(cls.x_label_sc[key], fontdict={"family": "Microsoft YaHei"}, size=22)
            plt.ylabel(cls.y_label_sc[key], fontdict={"family": "Microsoft YaHei"}, size=22)

            ax = plt.gca()  # 获得坐标轴的句柄
            ax.xaxis.set_ticks_position('bottom')
            ax.spines['bottom'].set_position(('data', 0))

            ax.spines['bottom'].set_linewidth(1.5)  # 设置底部坐标轴的粗细
            ax.spines['left'].set_linewidth(1.5)  # 设置左边坐标轴的粗细
            ax.spines['right'].set_linewidth(1.5)  # 设置右边坐标轴的粗细
            ax.spines['top'].set_linewidth(1.5)  # 设置上部坐标轴的粗细

            plt.ylim(y_limit[0], y_limit[1])
            plt.minorticks_on()
            plt.tick_params(direction='out', left=False, right=False, width=1, length=6, labelsize=22)
            plt.tick_params(which='minor', direction='out', left=False, right=False, width=1, length=3)
            plt.legend(line_list, labels=legend_labels, loc=0, edgecolor='#000000', prop={'size': 20})

            # 选择是否要保存图片以及格式(jpg/png/svg)
            if save is None:
                pass
            else:
                plt.savefig(save)

            plt.show()
        print(strftime("end --> %Y-%m-%d %H:%M:%S", localtime()))
        print("-------------------------------------------------------------")

    @classmethod
    def plot_fic_lc(cls, deal_data, emission_wavelength, dot_num, xtick, kind, key, x_limit, y_limit, save=None):
        print(strftime("start --> %Y-%m-%d %H:%M:%S", localtime()))
        with plt.style.context(['science', 'nature', 'no-latex']):
            fig = plt.figure(figsize=(12, 10), dpi=180)

            x_dot = xtick
            wave_length = list(deal_data.iloc[::, 0])
            y = []
            y0 = []

            for value in wave_length:
                if value == emission_wavelength:
                    index_value = wave_length.index(value)
                    i = 0
                    while i < dot_num:
                        if i == 0:
                            i += 1
                            continue
                        y.append(deal_data.iloc[index_value, i])
                        y0.append(deal_data.iloc[index_value, i] / 10000)
                        i += 1
                    break

            # 调整将要传入线性转换器中的参数的数据类型
            x_arr = np.array(x_dot).reshape(len(x_dot), 1)
            y_arr = np.array(y).reshape(len(y), 1)
            y0_arr = np.array(y0).reshape(len(y0), 1)

            # 进行线性拟合并将拟合曲线条件下的y值求出
            cls.line_model.fit(x_arr, y_arr)
            y_predict = cls.line_model.predict(x_arr)
            a1 = cls.line_model.coef_[0][0]
            b = cls.line_model.intercept_[0]

            cls.line_model.fit(x_arr, y0_arr)
            y0_predict = cls.line_model.predict(x_arr)

            function_str = ""
            if b < 0:
                function_str = "y = %.4fx - %.4f" % (a1, -b)
            elif b > 0:
                function_str = "y = %.4fx + %.4f" % (a1, b)

            R_square = r2_score(y_arr, y_predict)
            r2_str = "R$^{2}$ = %.4f" % (R_square)

            plt.scatter(x_dot, y0, marker='s', s=80, facecolor='none', edgecolor='#0000FF')

            y_function = plt.plot(x_arr, y0_predict, c="#FF7F50")
            y_r2 = plt.plot(0, 0, c="white")

            if kind == "amino":
                plt.title(cls.title_list[3][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            elif kind == "carboxyl":
                plt.title(cls.title_list[2][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            elif kind == "null":
                plt.title(cls.title_list[5][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            else:
                print("请输入正确信息！")
                return

            _x_ticks = [i for i in x_dot]
            plt.xticks(_x_ticks)

            plt.ylabel(cls.y_label_lc[key], fontdict={"family": "Microsoft YaHei", "size": 22})
            plt.xlabel(cls.x_label_lc[key], fontdict={"family": "Microsoft YaHei"}, size=22)
            ax = plt.gca()  # 获得坐标轴的句柄
            ax.xaxis.set_ticks_position('bottom')
            ax.yaxis.set_ticks_position('left')
            ax.spines['bottom'].set_position(('data', y_limit[0]))
            ax.spines['left'].set_position(('data', x_limit[0]))

            ax.spines['bottom'].set_linewidth(1.5)  # 设置底部坐标轴的粗细
            ax.spines['left'].set_linewidth(1.5)  # 设置左边坐标轴的粗细
            ax.spines['right'].set_linewidth(1.5)  # 设置右边坐标轴的粗细
            ax.spines['top'].set_linewidth(1.5)  # 设置上部坐标轴的粗细

            plt.xlim(x_limit[0], x_limit[1])
            plt.ylim(y_limit[0], y_limit[1])
            plt.minorticks_on()
            plt.tick_params(direction='in', left=False, right=False, width=1, length=6, labelsize=22)
            plt.tick_params(which='minor', direction='out', bottom=False, left=False, right=False, width=1, length=3)
            # 设置图例标签labels
            plt.legend([y_function, y_r2], labels=[function_str, r2_str],
                       loc=0, edgecolor='black', prop={'size': 20})

            # 选择是否要保存图片以及格式(jpg/png/svg)
            if save is None:
                pass
            else:
                plt.savefig(save)

            plt.show()
        print(strftime("end --> %Y-%m-%d %H:%M:%S", localtime()))
        print("-------------------------------------------------------------")
        return a1, b


class Retention(object):
    title_PS_COOH_TEMPO = {"English": "Retention(%) of TO-CNF-AG for different concentrations of PS(-)",
                        "Chinese": "TO-CNF-AG对不同浓度PS(-)的保留率"}
    title_PS_NH2_TEMPO = {"English": "Retention(%) of TO-CNF-AG for different concentrations of PS(+)",
                    "Chinese": "TO-CNF-AG对不同浓度PS(+)的保留率"}
    title_PS_TEMPO = {"English": "Retention(%) of TO-CNF-AG for different concentrations of PS",
                "Chinese": "TO-CNF-AG对不同浓度PS的保留率"}
    title_PS_COOH_QAS = {"English": "Retention(%) of QAS-CNF-AG for different concentrations of PS(-)",
                           "Chinese": "QAS-CNF-AG对不同浓度PS(-)的保留率"}
    title_PS_NH2_QAS = {"English": "Retention(%) of QAS-CNF-AG for different concentrations of PS(+)",
                          "Chinese": "QAS-CNF-AG对不同浓度PS(+)的保留率"}
    title_PS_QAS = {"English": "Retention(%) of QAS-CNF-AG for different concentrations of PS",
                      "Chinese": "QAS-CNF-AG对不同浓度PS的保留率"}
    title_TEMPO = {"English": "PS/PS(-)/PS(+) were captured by TO-CNF-AG filtration",
                          "Chinese": "通过TO-CNF-AG过滤捕获PS/PS(-)/PS(+)"}
    title_QAS = {"English": "PS/PS(-)/PS(+) were captured by QAS-CNF-AG filtration",
                        "Chinese": "通过QAS-CNF-AG过滤捕获PS/PS(-)/PS(+)"}
    title_TEMPO_PS_COOH = {"English": "Retention(%) of PS(-) by TO-CNF-AG at different concentrations",
                        "Chinese": "不同浓度TO-CNF-AG对PS(-)的保留率"}
    title_TEMPO_PS_NH2 = {"English": "Retention(%) of PS(+) by TO-CNF-AG at different concentrations",
                    "Chinese": "不同浓度TO-CNF-AG对PS(+)的保留率"}
    title_TEMPO_PS = {"English": "Retention(%) of PS by TO-CNF-AG at different concentrations",
                "Chinese": "不同浓度TO-CNF-AG对PS的保留率"}
    title_QAS_PS_COOH = {"English": "Retention(%) of PS(-) by QAS-CNF-AG at different concentrations",
                         "Chinese": "不同浓度QAS-CNF-AG对PS(-)的保留率"}
    title_QAS_PS_NH2 = {"English": "Retention(%) of PS(+) by QAS-CNF-AG at different concentrations",
                        "Chinese": "不同浓度QAS-CNF-AG对PS(+)的保留率"}
    title_QAS_PS = {"English": "Retention(%) of PS by QAS-CNF-AG at different concentrations",
                    "Chinese": "不同浓度QAS-CNF-AG对PS的保留率"}
    title_PS = {"English": "PS were captured by TO/QAS-CNF-AG filtration",
                   "Chinese": "通过TO/QAS-CNF-AG过滤捕获PS"}
    title_PS_COOH = {"English": "PS(-) were captured by TO/QAS-CNF-AG filtration",
                 "Chinese": "通过TO/QAS-CNF-AG过滤捕获PS(-)"}
    title_PS_NH2 = {"English": "PS(+) were captured by TO/QAS-CNF-AG filtration",
                   "Chinese": "通过TO/QAS-CNF-AG过滤捕获PS(+)"}

    title_list = [title_PS_TEMPO, title_PS_COOH_TEMPO, title_PS_NH2_TEMPO,
                  title_PS_QAS, title_PS_COOH_QAS, title_PS_NH2_QAS,
                  title_TEMPO, title_QAS,
                  title_TEMPO_PS, title_TEMPO_PS_COOH, title_TEMPO_PS_NH2,
                  title_QAS_PS, title_QAS_PS_COOH, title_QAS_PS_NH2,
                  title_PS, title_PS_COOH, title_PS_NH2]
    err_attr = {"elinewidth": 2, "capsize": 6}

    @classmethod
    def plot_retention(cls, retention:list, kind, key, labels:list, save=None):
        with plt.style.context(['science', 'nature', 'no-latex']):
            fig = plt.figure(figsize=(12, 10), dpi=180)
            bar_line = []
            for i in range(len(retention)):
                mini_retention = sorted(retention[i], reverse=True)
                y_err = np.std(mini_retention, ddof=1)
                line = plt.bar(i, mini_retention[len(mini_retention) - 1], yerr=y_err, error_kw=cls.err_attr, width=0.2)
                bar_line.append(line)

            plt.xticks([i for i in range(len(labels))], [(i + 1) for i in range(len(labels))])
            if kind == "null-TEMPO":
                plt.title(cls.title_list[0][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            elif kind == "carboxyl-TEMPO":
                plt.title(cls.title_list[1][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            elif kind == "amino-TEMPO":
                plt.title(cls.title_list[2][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            elif kind == "null-QAS":
                plt.title(cls.title_list[3][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            elif kind == "carboxyl-QAS":
                plt.title(cls.title_list[4][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            elif kind == "amino-QAS":
                plt.title(cls.title_list[5][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            elif kind == "TEMPO":
                plt.title(cls.title_list[6][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            elif kind == "QAS":
                plt.title(cls.title_list[7][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            elif kind == "TEMPO-null":
                plt.title(cls.title_list[8][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            elif kind == "TEMPO-carboxyl":
                plt.title(cls.title_list[9][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            elif kind == "TEMPO-amino":
                plt.title(cls.title_list[10][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            elif kind == "QAS-null":
                plt.title(cls.title_list[11][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            elif kind == "QAS-carboxyl":
                plt.title(cls.title_list[12][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            elif kind == "QAS-amino":
                plt.title(cls.title_list[13][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            elif kind == "null":
                plt.title(cls.title_list[14][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            elif kind == "carboxyl":
                plt.title(cls.title_list[15][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            elif kind == "amino":
                plt.title(cls.title_list[16][key], fontdict={"family": "Microsoft YaHei", "size": 22})
            else:
                print("请输入正确信息！")
                return

            plt.ylabel("Retention rate(%)", size=22)

            ax = plt.gca()  # 获得坐标轴的句柄
            ax.xaxis.set_ticks_position('bottom')
            ax.spines['bottom'].set_position(('data', 0))
            ax.spines['bottom'].set_linewidth(1.5)  # 设置底部坐标轴的粗细
            ax.spines['left'].set_linewidth(1.5)  # 设置左边坐标轴的粗细
            ax.spines['right'].set_linewidth(1.5)  # 设置右边坐标轴的粗细
            ax.spines['top'].set_linewidth(1.5)  #
            plt.minorticks_on()
            plt.tick_params(which='minor', direction='in', bottom=False, left=False, right=False, width=1, length=3)
            plt.tick_params(direction='out', bottom=False, right=False, left=False, width=1, length=6, labelsize=22)
            plt.ylim(0, 100)
            plt.legend(bar_line, labels=labels, loc=0, edgecolor='#000000', prop={'size': 22})
            if save:
                plt.savefig(save)
            plt.show()