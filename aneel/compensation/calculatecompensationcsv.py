import csv
import json
import datetime

"""
Criação de módulo que calcula as compensações de continuidade à consumidores informado em um padrão de CSV estabelecido.
"""


class CalculateCompensationCSV:
    __csv_path_file = ""
    __content_file = []
    __data_base = []
    __calculator = CompensationContinuityConsumer()

    def set_csv_path_file(self, csv_path_file):
        self.__csv_path_file = csv_path_file
        with open(self.__csv_path_file, "rt") as temp:
            self.__content_file = list(csv.reader(temp, delimiter=";", quotechar="\""))
        self.__ajust_data()
        self.__execute_calculations()

    def __ajust_data(self):
        for i, value in enumerate(self.__content_file):
            if i > 0:
                temp = [value[0], int(value[1]), value[2], value[3], value[4], int(value[5]),
                        [float(j) for j in value[6:18]], [float(j) for j in value[18:30]],
                        [float(j) for j in value[30:42]], [float(j) for j in value[42:54]]]
                self.__data_base.append(temp)

    def __execute_calculations(self):
        for i, value in enumerate(self.__data_base):
            self.__calculator.set_features(value[0], value[1], value[2], value[3], value[4], value[5], value[6],
                                           value[7], value[8], value[9])

    def write_result(self):
        temp01 = self.__csv_path_file
        temp02 = datetime.datetime.now().__str__().replace(" ", "-").replace(":", "-").replace(".", "-")
        with open(temp01.replace(".csv", "{}.csv".format(temp02)), "wt") as csv_file:
            temp03 = csv.writer(csv_file, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
            for linha in self.__data_base:
                temp03.writerow(linha[:6] + linha[6][:] + linha[7][:] + linha[8][:] + linha[9][:])

    def print_data(self):
        for linha in self.__data_base:
            # for linha in self.__data_base:
            print(linha)
            # for coluna in linha:
            # print("{}".format(coluna))


if __name__ == "__main__":
    print(datetime.datetime.now().__str__().replace(" ", "-").replace(":", "-").replace(".", "-"))
    my_file = CalculateCompensationCSV()
    my_file.set_csv_path_file("dados.csv")
    my_file.write_result()
    my_file.print_data()
    print(datetime.datetime.now().__str__().replace(" ", "-").replace(":", "-").replace(".", "-"))
