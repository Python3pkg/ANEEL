import csv
import json


class CompensationContinuityConsumer:
    __code_consumer = ""
    __year = 0
    __type_tension = "BT"
    __type_area = "URB"
    __type_system = "INT"
    __code_conjunt = 0
    __dic_monthly_h = [0.0] * 12
    __dic_quartely_h = [0.0] * 4
    __proportion_dic_quartely = [0.0] * 4
    __paid_monthly_dic_quartely_rs = [0.0] * 4
    __dic_yearly_h = [0.0] * 1
    __proportion_dic_yearly = [0.0] * 1
    __paid_monthly_dic_yearly_rs = [0.0] * 1
    __fic_monthly = [0.0] * 12
    __fic_quartely = [0.0] * 4
    __proportion_fic_quartely = [0.0] * 4
    __paid_monthly_fic_quartely_rs = [0.0] * 4
    __fic_yearly = [0.0] * 1
    __proportion_fic_yearly = [0.0] * 1
    __paid_monthly_fic_yearly_rs = [0.0] * 1
    __dmic_monthly_h = [0.0] * 12
    __eusd_monthly_rs = [0.0] * 12
    __eusd_quartely_rs = [0.0] * 4
    __eusd_yearly_rs = [0.0] * 1
    __kei = 0
    __limit_dec_yearly_h = 0
    __limit_fec_yearly = 0
    __limit_dic_monthly_h = 0
    __limit_fic_monthly = 0
    __limit_dmic_monthly_h = 0
    __limit_dic_quartely_h = 0
    __limit_fic_quartely = 0
    __limit_dic_yearly_h = 0
    __limit_fic_yearly = 0
    __monthly_value_compensation = [0.0] * 12
    __monthly_indicator_compensation = ["NA"] * 12
    __quartely_value_compensation = [0.0] * 4
    __quartely_indicator_compensation = ["NA"] * 4
    __yearly_value_compensation = [0.0] * 1
    __yearly_indicator_compensation = ["NA"] * 1

    def __init__(self, code_consumer, year, type_tension, type_area, type_system, code_conjunt, dic_h, fic, dmic_h,
                 eusd_rs):
        self.__code_consumer = code_consumer
        self.__year = year
        self.__type_tension = type_tension
        self.__type_area = type_area
        self.__type_system = type_system
        self.__code_conjunt = code_conjunt
        self.__dic_monthly_h = dic_h
        self.__fic_monthly = fic
        self.__dmic_monthly_h = dmic_h
        self.__eusd_monthly_rs = eusd_rs
        self.calculate_compensation()

    @classmethod
    def get_kei(cls, type_tension):
        if type_tension == "BT":
            return 15
        elif type_tension == "MT":
            return 20
        elif type_tension == "AT":
            return 27

    def __set_kei(self):
        self.__kei = CompensationContinuityConsumer.get_kei(self.__type_tension)

    @classmethod
    def get_dec_fec_limits(cls, code_conjunt, year):
        dec_fec_limits = [0.0] * 2
        # Each register must follow the pattern
        # [year1, [[codeConjunt1, yearlyDech, yearlyFec], [codeConjunt2, yearlyDech, yearlyFec]]]
        limits_table_dech_fec = [
            [2016, [[1111, 12, 6], [2222, 5, 2]]],
            [2017, [[1111, 6, 3], [2222, 2, 1]]],
        ]
        for years_table in limits_table_dech_fec:
            if years_table[0] == year:
                for code_conjunts_table in years_table[1]:
                    if code_conjunts_table[0] == code_conjunt:
                        dec_fec_limits = code_conjunts_table[1:]
                        return dec_fec_limits

    def __set_dec_fec_limits(self):
        temp = CompensationContinuityConsumer.get_dec_fec_limits(self.__code_conjunt, self.__year)
        self.__limit_dec_yearly_h = temp[0]
        self.__limit_fec_yearly = temp[1]

    @classmethod
    def get_table(cls, type_tension, type_area, type_system):
        table = 0
        if type_tension == "AT":
            table = 1
        elif type_tension == "MT" and type_area == "URB" and type_system == "INT":
            table = 2
        elif (type_tension == "MT" and type_area == "NRB") or type_system == "ISO":
            table = 3
        elif type_tension == "BT" and type_area == "URB" and type_system == "INT":
            table = 4
        elif type_tension == "BT" and type_area == "NRB" and type_system == "INT":
            table = 5
        return table

    @classmethod
    def get_index_table(cls, limit, type_tension, type_area, type_system):
        index = 0
        lanes = [
            [0, 1, 0],
            [1, 2, 1],
            [2, 3, 2],
            [3, 4, 3],
            [4, 5, 4],
            [5, 6, 5],
            [6, 7, 6],
            [7, 8, 7],
            [8, 9, 8],
            [9, 10, 9],
            [10, 11, 10],
            [11, 12, 11],
            [12, 13, 12],
            [13, 14, 13],
            [14, 15, 14],
            [15, 16, 15],
            [16, 17, 16],
            [17, 18, 17],
            [18, 19, 18],
            [19, 20, 19],
            [20, 22, 20],
            [22, 24, 21],
            [24, 26, 22],
            [26, 28, 23],
            [28, 30, 24],
            [30, 32, 25],
            [32, 34, 26],
            [34, 36, 27],
            [36, 38, 28],
            [38, 40, 29],
            [40, 45, 30],
            [45, 50, 31],
            [50, 55, 32],
            [55, 60, 33],
            [60, 65, 34],
            [65, 70, 35],
            [70, 80, 36],
            [80, 90, 37],
            [90, 100, 38],
            [100, 110, 39],
            [110, 120, 40],
            [120, 9999, 41],
        ]
        table = cls.get_table(type_tension, type_area, type_system)
        if table == 1:
            if type_system == "INT":
                index = 0
            else:
                index = 1
        else:
            for lane in lanes:
                if limit > lane[0] and limit <= lane[1]:
                    index = lane[2]
                    break
        return index

    @classmethod
    def get_dic_fic_dmic_limits(cls, code_conjunt, year, type_tension, type_area, type_system):
        dic_fic_dmic_limits = [0.0] * 7
        # Each register must follow the pattern
        # [table, index, yearlyDich, quartlyDich, monthlyDich, yearlyFic, quartlyFic, monthlyFic, monthlyDmich]
        limits_table_dich_fic_dmich = [
            [1, 0, 5.00, 3.00, 2.00, 5.00, 3.00, 2.00, 1.50],
            [1, 1, 6.00, 4.00, 3.00, 6.00, 4.00, 3.00, 2.50],
            [2, 0, 11.25, 5.62, 2.81, 6.48, 3.24, 1.62, 2.36],
            [2, 1, 11.68, 5.84, 2.92, 6.93, 3.46, 1.73, 2.39],
            [2, 2, 12.12, 6.06, 3.03, 7.37, 3.68, 1.84, 2.41],
            [2, 3, 12.55, 6.27, 3.13, 7.82, 3.91, 1.95, 2.44],
            [2, 4, 12.99, 6.49, 3.24, 8.27, 4.13, 2.06, 2.46],
            [2, 5, 13.43, 6.71, 3.35, 8.71, 4.35, 2.17, 2.49],
            [2, 6, 13.86, 6.93, 3.46, 9.16, 4.58, 2.29, 2.52],
            [2, 7, 14.3, 7.15, 3.57, 9.61, 4.8, 2.4, 2.54],
            [2, 8, 14.73, 7.36, 3.68, 10.05, 5.02, 2.51, 2.57],
            [2, 9, 15.17, 7.58, 3.79, 10.5, 5.25, 2.62, 2.6],
            [2, 10, 15.61, 7.8, 3.9, 10.95, 5.47, 2.73, 2.62],
            [2, 11, 16.04, 8.02, 4.01, 11.4, 5.7, 2.85, 2.65],
            [2, 12, 16.48, 8.24, 4.12, 11.84, 5.92, 2.96, 2.68],
            [2, 13, 16.91, 8.45, 4.22, 12.29, 6.14, 3.07, 2.71],
            [2, 14, 17.35, 8.67, 4.33, 12.74, 6.37, 3.18, 2.74],
            [2, 15, 17.79, 8.89, 4.44, 13.18, 6.59, 3.29, 2.76],
            [2, 16, 18.22, 9.11, 4.55, 13.63, 6.81, 3.4, 2.79],
            [2, 17, 18.66, 9.33, 4.66, 14.08, 7.04, 3.52, 2.82],
            [2, 18, 19.09, 9.54, 4.77, 14.52, 7.26, 3.63, 2.85],
            [2, 19, 19.53, 9.76, 4.88, 14.97, 7.48, 3.74, 2.88],
            [2, 20, 19.97, 9.98, 4.99, 15.42, 7.71, 3.85, 2.91],
            [2, 21, 20.84, 10.42, 5.21, 16.31, 8.15, 4.07, 2.98],
            [2, 22, 21.71, 10.85, 5.42, 17.2, 8.6, 4.3, 3.04],
            [2, 23, 22.58, 11.29, 5.64, 18.1, 9.05, 4.52, 3.1],
            [2, 24, 23.45, 11.72, 5.86, 18.99, 9.49, 4.74, 3.17],
            [2, 25, 24.33, 12.16, 6.08, 19.88, 9.94, 4.97, 3.24],
            [2, 26, 25.2, 12.6, 6.3, 20.78, 10.39, 5.19, 3.31],
            [2, 27, 26.07, 13.03, 6.51, 21.67, 10.83, 5.41, 3.38],
            [2, 28, 26.94, 13.47, 6.73, 22.57, 11.28, 5.64, 3.45],
            [2, 29, 27.81, 13.9, 6.95, 23.46, 11.73, 5.86, 3.52],
            [2, 30, 29.34, 14.67, 7.33, 25.02, 12.51, 6.25, 3.55],
            [2, 31, 31.52, 15.76, 7.88, 27.26, 13.63, 6.81, 3.8],
            [2, 32, 33.7, 16.85, 8.42, 29.49, 14.74, 7.37, 4.06],
            [2, 33, 35.88, 17.94, 8.97, 31.72, 15.86, 7.93, 4.34],
            [2, 34, 38.06, 19.03, 9.51, 33.96, 16.98, 8.49, 4.64],
            [2, 35, 40.24, 20.12, 10.06, 36.19, 18.09, 9.04, 4.96],
            [2, 36, 43.51, 21.75, 10.87, 39.54, 19.77, 9.88, 5.47],
            [2, 37, 47.87, 23.93, 11.96, 44.01, 22, 11, 6.23],
            [2, 38, 52.23, 26.11, 13.05, 48.48, 24.24, 12.12, 7.1],
            [2, 39, 56.59, 28.29, 14.14, 52.95, 26.47, 13.23, 8.07],
            [2, 40, 60.95, 30.47, 15.23, 57.42, 28.71, 14.35, 9.17],
            [2, 41, 63.13, 31.56, 15.78, 59.65, 29.82, 14.91, 9.77],
            [3, 0, 31.98, 15.99, 7.99, 15.49, 7.74, 3.87, 4.32],
            [3, 1, 32.62, 16.31, 8.15, 15.96, 7.98, 3.99, 4.39],
            [3, 2, 33.26, 16.63, 8.31, 16.43, 8.21, 4.1, 4.46],
            [3, 3, 33.9, 16.95, 8.47, 16.9, 8.45, 4.22, 4.53],
            [3, 4, 34.54, 17.27, 8.63, 17.37, 8.68, 4.34, 4.6],
            [3, 5, 35.18, 17.59, 8.79, 17.84, 8.92, 4.46, 4.67],
            [3, 6, 35.82, 17.91, 8.95, 18.31, 9.15, 4.57, 4.74],
            [3, 7, 36.46, 18.23, 9.11, 18.78, 9.39, 4.69, 4.81],
            [3, 8, 37.1, 18.55, 9.27, 19.25, 9.62, 4.81, 4.88],
            [3, 9, 37.74, 18.87, 9.43, 19.72, 9.86, 4.93, 4.95],
            [3, 10, 38.38, 19.19, 9.59, 20.19, 10.09, 5.04, 5.02],
            [3, 11, 39.02, 19.51, 9.75, 20.66, 10.33, 5.16, 5.09],
            [3, 12, 39.66, 19.83, 9.91, 21.13, 10.56, 5.28, 5.16],
            [3, 13, 40.3, 20.15, 10.07, 21.6, 10.8, 5.4, 5.24],
            [3, 14, 40.94, 20.47, 10.23, 22.07, 11.03, 5.51, 5.31],
            [3, 15, 41.58, 20.79, 10.39, 22.54, 11.27, 5.63, 5.38],
            [3, 16, 42.22, 21.11, 10.55, 23.01, 11.5, 5.75, 5.45],
            [3, 17, 42.86, 21.43, 10.71, 23.48, 11.74, 5.87, 5.52],
            [3, 18, 43.5, 21.75, 10.87, 23.95, 11.97, 5.98, 5.59],
            [3, 19, 44.14, 22.07, 11.03, 24.42, 12.21, 6.1, 5.66],
            [3, 20, 44.78, 22.39, 11.19, 24.9, 12.45, 6.22, 5.73],
            [3, 21, 46.06, 23.03, 11.51, 25.84, 12.92, 6.46, 5.87],
            [3, 22, 47.34, 23.67, 11.83, 26.78, 13.39, 6.69, 6.01],
            [3, 23, 48.61, 24.3, 12.15, 27.72, 13.86, 6.93, 6.15],
            [3, 24, 49.89, 24.94, 12.47, 28.66, 14.33, 7.16, 6.29],
            [3, 25, 51.17, 25.58, 12.79, 29.6, 14.8, 7.4, 6.43],
            [3, 26, 52.45, 26.22, 13.11, 30.54, 15.27, 7.63, 6.57],
            [3, 27, 53.73, 26.86, 13.43, 31.48, 15.74, 7.87, 6.72],
            [3, 28, 55.01, 27.5, 13.75, 32.42, 16.21, 8.1, 6.86],
            [3, 29, 56.29, 28.14, 14.07, 33.36, 16.68, 8.34, 7],
            [3, 30, 58.53, 29.26, 14.63, 35.01, 17.5, 8.75, 7.24],
            [3, 31, 61.73, 30.86, 15.43, 37.36, 18.68, 9.34, 7.6],
            [3, 32, 64.92, 32.46, 16.23, 39.71, 19.85, 9.92, 7.95],
            [3, 33, 68.12, 34.06, 17.03, 42.06, 21.03, 10.51, 8.3],
            [3, 34, 71.32, 35.66, 17.83, 44.42, 22.21, 11.1, 8.65],
            [3, 35, 74.52, 37.26, 18.63, 46.77, 23.38, 11.69, 9.01],
            [3, 36, 79.32, 39.66, 19.83, 50.3, 25.15, 12.57, 9.54],
            [3, 37, 85.71, 42.85, 21.42, 55, 27.5, 13.75, 10.24],
            [3, 38, 92.11, 46.05, 23.02, 59.7, 29.85, 14.92, 10.95],
            [3, 39, 98.5, 49.25, 24.62, 64.41, 32.2, 16.1, 11.65],
            [3, 40, 104.9, 52.45, 26.22, 69.11, 34.55, 17.27, 12.36],
            [3, 41, 108.1, 54.05, 27.02, 71.46, 35.73, 17.86, 12.71],
            [4, 0, 16, 8, 4, 11.2, 5.6, 2.8, 2.09],
            [4, 1, 16.47, 8.23, 4.11, 11.45, 5.72, 2.86, 2.18],
            [4, 2, 16.95, 8.47, 4.23, 11.7, 5.85, 2.92, 2.26],
            [4, 3, 17.43, 8.71, 4.35, 11.95, 5.97, 2.98, 2.35],
            [4, 4, 17.91, 8.95, 4.47, 12.2, 6.1, 3.05, 2.43],
            [4, 5, 18.38, 9.19, 4.59, 12.45, 6.22, 3.11, 2.52],
            [4, 6, 18.86, 9.43, 4.71, 12.7, 6.35, 3.17, 2.6],
            [4, 7, 19.34, 9.67, 4.83, 12.95, 6.47, 3.23, 2.69],
            [4, 8, 19.82, 9.91, 4.95, 13.2, 6.6, 3.3, 2.77],
            [4, 9, 20.3, 10.15, 5.07, 13.45, 6.72, 3.36, 2.86],
            [4, 10, 20.77, 10.38, 5.19, 13.7, 6.85, 3.42, 2.94],
            [4, 11, 21.25, 10.62, 5.31, 13.95, 6.97, 3.48, 3.03],
            [4, 12, 21.73, 10.86, 5.43, 14.2, 7.1, 3.55, 3.11],
            [4, 13, 22.21, 11.1, 5.55, 14.45, 7.22, 3.61, 3.2],
            [4, 14, 22.69, 11.34, 5.67, 14.7, 7.35, 3.67, 3.29],
            [4, 15, 23.16, 11.58, 5.79, 14.95, 7.47, 3.73, 3.37],
            [4, 16, 23.64, 11.82, 5.91, 15.2, 7.6, 3.8, 3.46],
            [4, 17, 24.12, 12.06, 6.03, 15.45, 7.72, 3.86, 3.54],
            [4, 18, 24.6, 12.3, 6.15, 15.7, 7.85, 3.92, 3.63],
            [4, 19, 25.08, 12.54, 6.27, 15.96, 7.98, 3.99, 3.71],
            [4, 20, 25.89, 12.94, 6.47, 16.47, 8.23, 4.11, 3.8],
            [4, 21, 27.48, 13.74, 6.87, 17.42, 8.71, 4.35, 3.97],
            [4, 22, 29.06, 14.53, 7.26, 18.37, 9.18, 4.59, 4.14],
            [4, 23, 30.65, 15.32, 7.66, 19.32, 9.66, 4.83, 4.31],
            [4, 24, 32.23, 16.11, 8.05, 20.28, 10.14, 5.07, 4.48],
            [4, 25, 33.82, 16.91, 8.45, 21.23, 10.61, 5.3, 4.65],
            [4, 26, 35.4, 17.7, 8.85, 22.18, 11.09, 5.54, 4.82],
            [4, 27, 36.99, 18.49, 9.24, 23.13, 11.56, 5.78, 4.99],
            [4, 28, 38.57, 19.28, 9.64, 24.08, 12.04, 6.02, 5.16],
            [4, 29, 40.16, 20.08, 10.04, 25.04, 12.52, 6.26, 5.33],
            [4, 30, 42.93, 21.46, 10.73, 26.7, 13.35, 6.67, 5.63],
            [4, 31, 46.89, 23.44, 11.72, 29.08, 14.54, 7.27, 6.05],
            [4, 32, 50.86, 25.43, 12.71, 31.46, 15.73, 7.86, 6.48],
            [4, 33, 54.82, 27.41, 13.7, 33.84, 16.92, 8.46, 6.9],
            [4, 34, 58.78, 29.39, 14.69, 36.22, 18.11, 9.05, 7.33],
            [4, 35, 62.74, 31.37, 15.68, 38.6, 19.3, 9.65, 7.75],
            [4, 36, 68.68, 34.34, 17.17, 42.17, 21.08, 10.54, 8.39],
            [4, 37, 76.61, 38.3, 19.15, 46.93, 23.46, 11.73, 9.24],
            [4, 38, 84.53, 42.26, 21.13, 51.69, 25.84, 12.92, 10.09],
            [4, 39, 92.46, 46.23, 23.11, 56.45, 28.22, 14.11, 10.94],
            [4, 40, 100.38, 50.19, 25.09, 61.21, 30.6, 15.3, 11.8],
            [4, 41, 104.34, 52.17, 26.08, 63.59, 31.79, 15.89, 12.22],
            [5, 0, 36, 18, 9, 28, 14, 7, 4.57],
            [5, 1, 36.57, 18.28, 9.14, 28.29, 14.14, 7.07, 4.67],
            [5, 2, 37.15, 18.57, 9.28, 28.59, 14.29, 7.14, 4.77],
            [5, 3, 37.73, 18.86, 9.43, 28.89, 14.44, 7.22, 4.87],
            [5, 4, 38.3, 19.15, 9.57, 29.19, 14.59, 7.29, 4.97],
            [5, 5, 38.88, 19.44, 9.72, 29.49, 14.74, 7.37, 5.07],
            [5, 6, 39.46, 19.73, 9.86, 29.79, 14.89, 7.44, 5.17],
            [5, 7, 40.03, 20.01, 10, 30.09, 15.04, 7.52, 5.28],
            [5, 8, 40.61, 20.3, 10.15, 30.39, 15.19, 7.59, 5.38],
            [5, 9, 41.19, 20.59, 10.29, 30.69, 15.34, 7.67, 5.48],
            [5, 10, 41.76, 20.88, 10.44, 30.98, 15.49, 7.74, 5.58],
            [5, 11, 42.34, 21.17, 10.58, 31.28, 15.64, 7.82, 5.68],
            [5, 12, 42.92, 21.46, 10.73, 31.58, 15.79, 7.89, 5.78],
            [5, 13, 43.49, 21.74, 10.87, 31.88, 15.94, 7.97, 5.88],
            [5, 14, 44.07, 22.03, 11.01, 32.18, 16.09, 8.04, 5.98],
            [5, 15, 44.65, 22.32, 11.16, 32.48, 16.24, 8.12, 6.08],
            [5, 16, 45.22, 22.61, 11.3, 32.78, 16.39, 8.19, 6.19],
            [5, 17, 45.8, 22.9, 11.45, 33.08, 16.54, 8.27, 6.29],
            [5, 18, 46.38, 23.19, 11.59, 33.38, 16.69, 8.34, 6.39],
            [5, 19, 46.96, 23.48, 11.74, 33.68, 16.84, 8.42, 6.49],
            [5, 20, 47.79, 23.89, 11.94, 34.16, 17.08, 8.54, 6.59],
            [5, 21, 49.42, 24.71, 12.35, 35.1, 17.55, 8.77, 6.79],
            [5, 22, 51.05, 25.52, 12.76, 36.04, 18.02, 9.01, 6.99],
            [5, 23, 52.68, 26.34, 13.17, 36.98, 18.49, 9.24, 7.2],
            [5, 24, 54.31, 27.15, 13.57, 37.92, 18.96, 9.48, 7.4],
            [5, 25, 55.94, 27.97, 13.98, 38.86, 19.43, 9.71, 7.6],
            [5, 26, 57.57, 28.78, 14.39, 39.8, 19.9, 9.95, 7.8],
            [5, 27, 59.2, 29.6, 14.8, 40.74, 20.37, 10.18, 8.01],
            [5, 28, 60.83, 30.41, 15.2, 41.69, 20.84, 10.42, 8.21],
            [5, 29, 62.45, 31.22, 15.61, 42.63, 21.31, 10.65, 8.41],
            [5, 30, 65.3, 32.65, 16.32, 44.27, 22.13, 11.06, 8.76],
            [5, 31, 69.38, 34.69, 17.34, 46.62, 23.31, 11.65, 9.27],
            [5, 32, 73.45, 36.72, 18.36, 48.98, 24.49, 12.24, 9.77],
            [5, 33, 77.52, 38.76, 19.38, 51.33, 25.66, 12.83, 10.28],
            [5, 34, 81.59, 40.79, 20.39, 53.68, 26.84, 13.42, 10.79],
            [5, 35, 85.66, 42.83, 21.41, 56.03, 28.01, 14, 11.29],
            [5, 36, 91.77, 45.88, 22.94, 59.56, 29.78, 14.89, 12.05],
            [5, 37, 99.92, 49.96, 24.98, 64.26, 32.13, 16.06, 13.06],
            [5, 38, 108.06, 54.03, 27.01, 68.97, 34.48, 17.24, 14.07],
            [5, 39, 116.2, 58.1, 29.05, 73.67, 36.83, 18.41, 15.08],
            [5, 40, 124.35, 62.17, 31.08, 78.38, 39.19, 19.59, 16.09],
            [5, 41, 128.42, 64.21, 32.1, 80.73, 40.36, 20.18, 16.6],
        ]
        table = cls.get_table(type_tension, type_area, type_system)
        dec_fec_limits = cls.get_dec_fec_limits(code_conjunt, year)
        index_dec = cls.get_index_table(dec_fec_limits[0], type_tension, type_area, type_system)
        index_fec = cls.get_index_table(dec_fec_limits[1], type_tension, type_area, type_system)
        for register in limits_table_dich_fic_dmich:
            if register[0] == table and register[1] == index_dec:
                dic_fic_dmic_limits[0] = register[2]
                dic_fic_dmic_limits[1] = register[3]
                dic_fic_dmic_limits[2] = register[4]
                dic_fic_dmic_limits[6] = register[8]
            if register[0] == table and register[1] == index_fec:
                dic_fic_dmic_limits[3] = register[5]
                dic_fic_dmic_limits[4] = register[6]
                dic_fic_dmic_limits[5] = register[7]
        return dic_fic_dmic_limits

    def __set_dic_fic_dmic_limits(self):
        temp = CompensationContinuityConsumer.get_dic_fic_dmic_limits(self.__code_conjunt, self.__year, self.__type_tension,
                                                                      self.__type_area, self.__type_system)
        self.__limit_dic_yearly_h = temp[0]
        self.__limit_dic_quartely_h = temp[1]
        self.__limit_dic_monthly_h = temp[2]
        self.__limit_fic_yearly = temp[3]
        self.__limit_fic_quartely = temp[4]
        self.__limit_fic_monthly = temp[5]
        self.__limit_dmic_monthly_h = temp[6]

    def __set_time_variables(self):
        self.__dic_quartely_h = [0.0] * 4
        self.__fic_quartely = [0.0] * 4
        self.__eusd_quartely_rs = [0.0] * 4
        self.__proportion_dic_quartely = [0.0] * 4
        self.__proportion_fic_quartely = [0.0] * 4
        self.__dic_yearly_h = [0.0] * 1
        self.__fic_yearly = [0.0] * 1
        self.__eusd_yearly_rs = [0.0] * 1
        self.__proportion_dic_yearly = [0.0] * 1
        self.__proportion_fic_yearly = [0.0] * 1
        for i, value in enumerate(self.__dic_monthly_h):
            self.__dic_quartely_h[i // 3] += self.__dic_monthly_h[i]
            self.__fic_quartely[i // 3] += self.__fic_monthly[i]
            self.__eusd_quartely_rs[i // 3] += self.__eusd_monthly_rs[i] / 3
            self.__dic_yearly_h[i // 12] += self.__dic_monthly_h[i]
            self.__fic_yearly[i // 12] += self.__fic_monthly[i]
            self.__eusd_yearly_rs[i // 12] += self.__eusd_monthly_rs[i] / 12
        for i, value in enumerate(self.__dic_monthly_h):
            if self.__dic_monthly_h[i] <= self.__limit_dic_monthly_h:
                self.__proportion_dic_quartely[i // 3] += self.__dic_monthly_h[i] / self.__dic_quartely_h[i // 3]
                self.__proportion_dic_yearly[i // 12] += self.__dic_monthly_h[i] / self.__dic_yearly_h[i // 12]
            if self.__fic_monthly[i] <= self.__limit_fic_monthly:
                self.__proportion_fic_quartely[i // 3] += self.__fic_monthly[i] / self.__fic_quartely[i // 3]
                self.__proportion_fic_yearly[i // 12] += self.__fic_monthly[i] / self.__fic_yearly[i // 12]

    def __calculate_compensation_monthly(self):
        self.__monthly_value_compensation = [0.0] * 12
        self.__monthly_indicator_compensation = ["NA"] * 12
        gross_compensation_dic_rs = [0] * 12
        gross_compensation_fic_rs = [0] * 12
        gross_compensation_dmic_rs = [0] * 12
        for i, value in enumerate(self.__dic_monthly_h):
            if self.__dic_monthly_h[i] > self.__limit_dic_monthly_h:
                gross_compensation_dic_rs[i] = (self.__dic_monthly_h[
                                                    i] / self.__limit_dic_monthly_h - 1) * self.__limit_dic_monthly_h * \
                                               self.__eusd_monthly_rs[i] * self.__kei / 730
            if self.__dmic_monthly_h[i] > self.__limit_dmic_monthly_h:
                gross_compensation_dmic_rs[i] = (self.__dmic_monthly_h[
                                                     i] / self.__limit_dmic_monthly_h - 1) * self.__limit_dmic_monthly_h * \
                                                self.__eusd_monthly_rs[i] * self.__kei / 730
            if self.__fic_monthly[i] > self.__limit_fic_monthly:
                gross_compensation_fic_rs[i] = (self.__fic_monthly[
                                                    i] / self.__limit_fic_monthly - 1) * self.__limit_dic_monthly_h * \
                                               self.__eusd_monthly_rs[i] * self.__kei / 730
            if gross_compensation_dic_rs[i] > 0 and gross_compensation_dic_rs[i] >= gross_compensation_fic_rs[i] and \
                            gross_compensation_dic_rs[i] >= gross_compensation_dmic_rs[i]:
                self.__monthly_value_compensation[i] = gross_compensation_dic_rs[i]
                self.__monthly_indicator_compensation[i] = "DIC"
            elif gross_compensation_fic_rs[i] > 0 and gross_compensation_fic_rs[i] > gross_compensation_dic_rs[i] and \
                            gross_compensation_fic_rs[i] > gross_compensation_dmic_rs[i]:
                self.__monthly_value_compensation[i] = gross_compensation_fic_rs[i]
                self.__monthly_indicator_compensation[i] = "FIC"
            elif gross_compensation_dmic_rs[i] > 0 and gross_compensation_dmic_rs[i] > gross_compensation_dic_rs[i] and \
                            gross_compensation_dmic_rs[i] > gross_compensation_fic_rs[i]:
                self.__monthly_value_compensation[i] = gross_compensation_dmic_rs[i]
                self.__monthly_indicator_compensation[i] = "DMIC"
            else:
                self.__monthly_value_compensation[i] = 0
                self.__monthly_indicator_compensation[i] = "NA"

    def __calculate_paid_compensation_monthly(self):
        self.__paid_monthly_dic_quartely_rs = [0.0] * 4
        self.__paid_monthly_dic_yearly_rs = [0.0] * 1
        self.__paid_monthly_fic_quartely_rs = [0.0] * 4
        self.__paid_monthly_fic_yearly_rs = [0.0] * 1
        for i, value in enumerate(self.__monthly_value_compensation):
            if self.__monthly_indicator_compensation[i] == "DIC":
                self.__paid_monthly_dic_quartely_rs[i // 3] += self.__monthly_value_compensation[i]
                self.__paid_monthly_dic_yearly_rs[i // 12] += self.__monthly_value_compensation[i]
            if self.__monthly_indicator_compensation[i] == "FIC":
                self.__paid_monthly_fic_quartely_rs[i // 3] += self.__monthly_value_compensation[i]
                self.__paid_monthly_fic_yearly_rs[i // 12] += self.__monthly_value_compensation[i]

    def __calculate_compensation_quartely(self):
        self.__quartely_value_compensation = [0.0] * 4
        self.__quartely_indicator_compensation = ["NA"] * 4
        gross_compensation_dic_rs = [0] * 4
        gross_compensation_fic_rs = [0] * 4
        for i, value in enumerate(self.__dic_quartely_h):
            if self.__dic_quartely_h[i] > self.__limit_dic_quartely_h:
                gross_compensation_dic_rs[i] = (
                                                   self.__dic_quartely_h[
                                                       i] / self.__limit_dic_quartely_h - 1) * self.__limit_dic_quartely_h * \
                                               self.__eusd_quartely_rs[i] * self.__kei / 730
            if self.__fic_quartely[i] > self.__limit_fic_quartely:
                gross_compensation_fic_rs[i] = (self.__fic_quartely[
                                                    i] / self.__limit_fic_quartely - 1) * self.__limit_dic_quartely_h * \
                                               self.__eusd_quartely_rs[i] * self.__kei / 730
            if self.__proportion_dic_quartely[i] != 0:
                gross_compensation_dic_rs[i] *= self.__proportion_dic_quartely[i]
            else:
                gross_compensation_dic_rs[i] -= self.__paid_monthly_dic_quartely_rs[i]
            if self.__proportion_fic_quartely[i] != 0:
                gross_compensation_fic_rs[i] *= self.__proportion_fic_quartely[i]
            else:
                gross_compensation_fic_rs[i] -= self.__paid_monthly_fic_quartely_rs[i]
            if gross_compensation_dic_rs[i] > 0 and gross_compensation_dic_rs[i] >= gross_compensation_fic_rs[i]:
                self.__quartely_value_compensation[i] = gross_compensation_dic_rs[i]
                self.__quartely_indicator_compensation[i] = "DIC"
            elif gross_compensation_fic_rs[i] > 0 and gross_compensation_fic_rs[i] > gross_compensation_dic_rs[i]:
                self.__quartely_value_compensation[i] = gross_compensation_fic_rs[i]
                self.__quartely_indicator_compensation[i] = "FIC"
            else:
                self.__quartely_value_compensation[i] = 0
                self.__quartely_indicator_compensation[i] = "NA"

    def __calculate_compensation_yearly(self):
        self.__yearly_value_compensation = [0.0] * 1
        self.__yearly_indicator_compensation = ["NA"] * 1
        gross_compensation_dic_rs = [0] * 1
        gross_compensation_fic_rs = [0] * 1
        for i, value in enumerate(self.__dic_yearly_h):
            if self.__dic_yearly_h[i] > self.__limit_dic_yearly_h:
                gross_compensation_dic_rs[i] = (
                                                   self.__dic_yearly_h[
                                                       i] / self.__limit_dic_yearly_h - 1) * self.__limit_dic_yearly_h * \
                                               self.__eusd_yearly_rs[i] * self.__kei / 730
            if self.__fic_yearly[i] > self.__limit_fic_yearly:
                gross_compensation_fic_rs[i] = (self.__fic_yearly[
                                                    i] / self.__limit_fic_yearly - 1) * self.__limit_dic_yearly_h * \
                                               self.__eusd_yearly_rs[i] * self.__kei / 730
            if self.__proportion_dic_yearly[i] != 0:
                gross_compensation_dic_rs[i] *= self.__proportion_dic_yearly[i]
            else:
                gross_compensation_dic_rs[i] -= self.__paid_monthly_dic_yearly_rs[i]
            if self.__proportion_fic_yearly[i] != 0:
                gross_compensation_fic_rs[i] *= self.__proportion_fic_yearly[i]
            else:
                gross_compensation_fic_rs[i] -= self.__paid_monthly_fic_yearly_rs[i]
            if gross_compensation_dic_rs[i] > 0 and gross_compensation_dic_rs[i] >= gross_compensation_fic_rs[i]:
                self.__yearly_value_compensation[i] = gross_compensation_dic_rs[i]
                self.__yearly_indicator_compensation[i] = "DIC"
            elif gross_compensation_fic_rs[i] > 0 and gross_compensation_fic_rs[i] > gross_compensation_dic_rs[i]:
                self.__yearly_value_compensation[i] = gross_compensation_fic_rs[i]
                self.__yearly_indicator_compensation[i] = "FIC"
            else:
                self.__yearly_value_compensation[i] = 0
                self.__yearly_indicator_compensation[i] = "NA"

    def calculate_compensation(self):
        self.__set_kei()
        self.__set_dec_fec_limits()
        self.__set_dic_fic_dmic_limits()
        self.__set_time_variables()
        self.__calculate_compensation_monthly()
        self.__calculate_paid_compensation_monthly()
        self.__calculate_compensation_quartely()
        self.__calculate_compensation_yearly()

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __repr__(self):
        return json.dumps(self.__dict__, sort_keys=True, indent=2)


class calculateCompensation:
    database = []

    def __init__(self, csvpathfile):
        with open(csvpathfile, "rt") as csvpathfile:
            self.database = list(csv.reader(csvpathfile, delimiter=";", quotechar="\""))

    def printData(self):
        for linha in self.database:
            for coluna in linha:
                print("{}".format(coluna))


if __name__ == "__main__":
    mycal = CompensationContinuityConsumer("abc", 2016, "BT", "URB", "INT", 1111, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                           [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                           [40, 42, 43, 44, 45, 56, 47, 38, 49, 40, 51, 62])
    print(mycal)
    print(CompensationContinuityConsumer.get_dec_fec_limits(1111, 2016))
    print(CompensationContinuityConsumer.get_kei("BT"))
    print(CompensationContinuityConsumer.get_table("BT", "URB", "INT"))
    print(CompensationContinuityConsumer.get_dic_fic_dmic_limits(1111, 2016, "BT", "URB", "INT"))
