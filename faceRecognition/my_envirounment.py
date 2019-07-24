import pandas as pd
import requests  as re
import json
import pinyin
import numpy as np

file_path = 'D:/github/python-master/python-master/areaid.csv'
def city2code(cityname):
    csv_file = pd.read_csv(file_path)
    list_index = [i for i in csv_file.NAMEEN]

    csv_file.index = list_index
    csv_file1 = csv_file.drop(['NAMECN'], axis = 1)
    value = csv_file1.at[cityname, 'AREAID']

    if type(value) is np.int64:
        return value
    else:
        return value[0]


def palceName():
    '''
    csv_file = pd.read_csv(file_path)
    print(type(csv_file))
    list_index = [i for i in csv_file.NAMEEN]
    csv_file.index = list_index
    csv_file1 = csv_file.drop(['NAMEEN'], axis = 1)
    list_P = csv_file1.PROVCN
    list_D = csv_file1.DISTRICTCN

    Shengfen_1 = set(i for i in list_P)
    Shengfen = list(Shengfen_1)

    list1_W = []
    for i in Shengfen:
        csv_file_c = csv_file.copy()
        csv_file_c.index = [i for i in csv_file_c.PROVEN]
        shenfen_py = pinyin.get(i, format="strip", delimiter="")
        csv_file_c_s =  csv_file_c.loc[shenfen_py,'DISTRICTCN']
        set_F = set(csv_file_c_s)
        list_f = [i for i in set_F]
        list1_W.append(list_f)
    # dict_1表示的是省-市
    dict_1 = dict(zip(Shengfen,list1_W))

    Shiqu_1 =  set(i for i in list_D)
    Shiqu = list(i for i in Shiqu_1)
    list1_N = []
    for i in Shiqu:
        csv_file_c_f = csv_file.copy()
        csv_file_c_f.index = [i for i in csv_file.DISTRICTEN]
        shiqu_py = pinyin.get(i, format="strip", delimiter="")
        csv_file_c_s = csv_file_c_f.loc[shiqu_py, 'NAMECN']

        if type(csv_file_c_s) is str:
            str_list = [csv_file_c_s]

            list1_N.append(str_list)
        else:
            set_g = set(csv_file_c_s)

            list_q = [i for i in set_g]

            list1_N.append(list_q)
    # dict_2表示的是市-县
    dict_2 = dict(zip(Shiqu, list1_N))
    '''
    dict_1 = {'信息学院':['信息工程', '通信工程'],'数理学院':['统计学', '信息与计算科学']}
    dict_2 = {'信息工程':['信息151', '信息152', '信息161', '信息162'],'通信工程':['通信151', '通信152', '通信161', '通信162'],
              '统计学':['统计151', '统计152', '统计161', '统计162'], '信息与计算科学':['信计151', '信计152', '信计161', '信计162']}
    return dict_1,dict_2

if __name__ == '__main__':
    name = '信息151'
    Mlist = list(palceName())
    Mdict0 = Mlist[1]
    Mlist1 = Mdict0.values()
    list1 = []
    for i in Mlist1:
        list1 +=i
    csv_file = pd.read_csv(file_path)
    list_B = csv_file.loc[:,['NAMEEN']]
    list2 =[i for i in list_B.NAMEEN]
    for i in range(len(list1)):
        shiqu_py = pinyin.get(list1[i], format="strip", delimiter="")
        try:
            if shiqu_py not in list2:
                print(list1[i],shiqu_py)
        except:
            pass