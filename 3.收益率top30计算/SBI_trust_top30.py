

import csv
import operator
import re
import time

from sqlalchemy import create_engine
import pymysql
import pandas as pd
import os
import datetime
import json

def remove_list(item):
    if item == []:
        item = [""]
        result = item
    else:
        result = item
    return result


def get_notnull_fromlist(list_content):
    result_list = []
    for item in list_content:
        if len(item) !=0:
            result_list.append(item)
    return result_list







def mkdir(path):
    lpath = os.getcwd()
    isExists = os.path.exists(lpath + "/" + path)
    if not isExists:
        os.makedirs(path)


def writeinto_detail(filename,data):
    with open(filename,"a",newline="",encoding="utf-8") as f:
        csv_out = csv.writer(f,delimiter=",")
        csv_out.writerow(data)


def from_db_fetch_last_to30(code):
    engine_Lynne_Mons = create_engine('mysql+pymysql://root:123456@localhost:3306/Trust')

    df_js_f = pd.read_sql_query('select {0} from SBI_trust_daily_dt; '.format(code), engine_Lynne_Mons)
    last_one = df_js_f.values.tolist()[-1][0].split()[0]
    minus30_one = df_js_f.values.tolist()[-9][0].split()[0]
    earning_rate =round((int(last_one)-int(minus30_one))/int(minus30_one),4)
    return earning_rate






def fetch_sql_code(list_content):
    f_list = []
    for item in list_content:
        pattern = re.compile('Param6=(.*?)&int_fd', re.S)
        items = re.findall(pattern, item)
        f_result= ["td{0}".format(x) for x in items if len(x)>1]
        f_list.append(f_result[0])

    return f_list

def readjsonfile(filename):
    with open(filename, 'r', encoding='utf-8') as fw:
        s = json.load(fw)
        return s


# 获取列表的第二个元素
def takeSecond(elem):
    return elem[1]


if __name__== "__main__":
    resultjson = readjsonfile("sbi_trust.json")
    result_url = []
    result_title = []
    result_firm = []
    result_fee = []
    result_last_day = []
    result_R = []
    for item in resultjson:
        result_url.append(item["url"])
        result_title.append(item["title"])
        result_firm.append(item["firm"])
        result_fee.append(item["fee"])
        result_last_day.append(item["last_day"])
    f_sql_code = fetch_sql_code(result_url)
    sbi_trust_code = [x[2:]  for x in f_sql_code]
    for code_item in f_sql_code:
        result_R.append(from_db_fetch_last_to30(code_item))
    all_result = []



    for i1,i2,i3,i4,i5,i6 in zip(sbi_trust_code,result_R,result_title,result_fee,result_last_day,result_firm):
        all_result.append([i1,i2,i3,i4,i5,i6])
    all_result.sort(key=takeSecond,reverse=True)
    filename = datetime.datetime.now().strftime('%Y-%m-%d')
    three_table_title = ["sbi_trust_code", "ER", "title", "fee", "last_day","firm"]
    writeinto_detail("sbi_trust_top50_{0}.csv".format(filename), three_table_title)
    for item in all_result[:50]:
        writeinto_detail("sbi_trust_top50_{0}.csv".format(filename), item)
        print(item)
    print(result_url)


