import pandas as pd
import xlrd
from openpyxl import load_workbook

def read_data(file_path):
    data = xlrd.open_workbook(file_path)
    return data

data = read_data(r'C:\Users\Ilian\Desktop\Tatko\Работна Теленор ДП 72.xls')

def read_sheet_data(data, sheet_name):
    return data.sheet_by_name(sheet_name)


def get_dict_from_sheet_data(data, sheet_data):
    dict = {}
    for row in range(1, sheet_data.nrows):
        key = str(sheet_data.cell_value(row,4))
        print(key)
        if key != None and key !='А Номер' and key != '':
            dict[key] = False
    return dict

def algo(data):
    list_of_dicts = {}
    for name in data.sheet_names():
        sheet_data = read_sheet_data(data, name)
        dict_data = get_dict_from_sheet_data(data, sheet_data)
        list_of_dicts[name] = dict_data
    return list_of_dicts

list_of_dicts = algo(data)
names = list(list_of_dicts.keys())
print(list_of_dicts)

def comp(list_of_dicts, dic1, dic2):
    d = {}
    for elt in list_of_dicts[dic1]:
        if elt in list_of_dicts[dic2]:
            d[elt] = [dic1, dic2]
    return d

def compare(list_of_dicts, names):
    d = {}
    for i in range(len(names)):
        for y in range(i+1, len(names)):
            for elt in list_of_dicts[names[i]]:
                if elt in list_of_dicts[names[y]]:
                    if elt not in d:
                        d[elt] = [names[i], names[y]]
                    else:
                        if names[y] not in d[elt]:
                            d[elt].append(names[y])
    return d

final_dict = compare(list_of_dicts, names)
print(final_dict)
with open("Работна Теленор ДП 72 data.txt","w") as f:
    for elt in final_dict:
        f.write(f"{elt} - ")
        for element in final_dict[elt]:
            f.write(f"{element}, ")
        f.write("\n")









