#!/usr/bin/env python
__author__ = "lrtao2010"
'''
Excel文件转csv文件脚本
需要将该脚本直接放到要转换的Excel文件同级目录下
支持xlsx 和 xls 格式
在同级目录下生成名为excel_to_csv.csv 的文件，采用UTF-8编码
'''
import xlrd
import csv
import os


# 生成的csv文件名


def get_excel_list():
    # 获取Excel文件列表
    excel_file_list = []
    file_list = os.listdir(os.getcwd())
    for file_name in file_list:
        if file_name.endswith('.csv'):
            excel_file_list.append(file_name)
    return excel_file_list


def read_csv(file_name):
    with open(file_name, "rb") as f:
        items = f.readlines()
        return items


def get_excel_header(excel_name_for_header):
    # 获取表头，并将表头全部变为小写
    workbook = xlrd.open_workbook(excel_name_for_header)
    table = workbook.sheet_by_index(0)
    # row_value = table.row_values(0)
    row_value = [i.lower() for i in table.row_values(0)]
    return row_value


def xlsx_to_csv(csv_file_name, row_value):
    # 生成csv文件
    with open(csv_file_name, 'a', encoding='utf-8', newline='') as f:  # newline=''不加会多空行
        write = csv.writer(f)
        write.writerow(row_value)


def writeToCsv(csv_file_name, row_value):
    with open(csv_file_name, "a", encoding='utf-8') as f:
        f.write(row_value)

        # if type(row_value) == str:
        #     f.write(row_value + "\n")
        # else:
        #     f.write(",".join(row_value) + "\n")


finalName = "csv/A级纳税人.csv"
if __name__ == '__main__':
    # 获取Excel列表
    excel_list = get_excel_list()
    # 获取Excel表头并生成csv文件标题
    # 生成csv数据内容
    obj = {"云南": [3, 1, 2],
           "内蒙古": [1, -1, 0],
           "北京": [1, -1, 2],
           "江西": [1, -1, 0],
           "辽宁": [2, -1, 1],
           "黑龙江": [2, -1, 1],

           "上海": [2, 1, -1],
           "吉林四平": [2, 1, -1],
           "吉林白城": [2, 1, 0],
           "四川": [1, -1, 0],
           "天津": [1, -1, 0],
           "宁夏": [2, 1, -1],
           "安徽省": [0, -1, 1],
           "山东": [2, 1, -1],
           "广东": [4, 3, 2],
           "广西": [1, 0, 0],
           "新疆": [2, 1, -1],
           "江苏南京": [3, 2, 1],
           "河北": [3, 2, 1],
           "河南": [1, -1, 0],
           "浙江省": [2, -1, 1],
           "海南": [2, -1, 1],
           "湖北": [2, -1, 1],
           "甘肃": [2, -1, 1],
           "福建省": [0, -1, 1],
           "西藏": [2, -1, 1],
           "贵州": [3, 1, 2],
           "重庆": [1, -1, 0],
           "陕西": [1, -1, -1]
           }
    writeToCsv(finalName, "评价结果,评价年度,纳税人名称,统一社会信用码,纳税人识别号" + "\n")

    for excel_name in excel_list:
        print(excel_name)
        # writeToCsv('csv/' + excel_name, "评价结果,评价年度,纳税人名称,统一社会信用码,纳税人识别号")
        key = excel_name.split(".")[0]
        items = read_csv(excel_name)[1:]
        # print(len(items))
        i = 1
        num = len(items)
        for item in items:
            i += 1
            print(key, num, i)
            # row_value = item.decode("utf-8").replace("\r", "").replace("\n", "").replace("\t", "").replace("\x7f",
            #                                                                                                "").split(
            #     ",")
            # newValue = []
            # newValue.append("A")
            # newValue.append("2018")
            # for lie in obj[key]:
            #     if lie == -1:
            #         newValue.append(str(0))
            #         continue
            #     newValue.append(row_value[lie])
            # writeToCsv(finalName, newValue)
            writeToCsv(finalName, item.decode("utf-8").replace("\r", ""))
            # break
        # break
print('Excel文件转csv文件结束 ')
