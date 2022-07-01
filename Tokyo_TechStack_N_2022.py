


# -*- coding: utf-8 -*-


import csv
import datetime
import os
import re
import time
import sys
type = sys.getfilesystemencoding()
import pymysql
# import xlrd
import requests
from requests.exceptions import RequestException


def call_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def RemoveDot(item):
    f_l = []
    for it in item:
        f_str = "".join(it.split(","))
        f_l.append(f_str)

    return f_l


def remove_block(items):
    new_items = []
    for it in items:
        f = "".join(it.split())
        new_items.append(f)
    return new_items


def writerDt_csv(headers, rowsdata):
    # rowsdata列表中的数据元组,也可以是字典数据
    with open('tokyoTSN.csv', 'w',newline = '') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rowsdata)


def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='Indeed_J',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:

        f_6 = "%s," *6
        cursor.executemany('insert into Tokyo_TSN ({0}) values ({1})'.format(f_FS_DB,f_6[:-1]), content)
        connection.commit()
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass



if __name__ == '__main__':
    big_list = []
    TS_lang_DB = 'Python,Glang,Echo,Gin,Docker,openstack'
    TS_lang_Web = 'Python,Glang,Echo,Gin,Docker,openstack'
    f_FS_web =TS_lang_Web
    f_FS_DB =TS_lang_DB
    f_tsn_web = f_FS_web.split(",")
    print(len(f_tsn_web))

    for code in f_tsn_web:
        url = 'https://jp.indeed.com/jobs?q={0}&l=%E6%9D%B1%E4%BA%AC%E9%83%BD'.format(code)

        html = call_page(url)
        print(url)
        patt = re.compile('求人検索結果 (.*?) 件中 1 ページ目</div>',re.S)
        items = re.findall(patt, html)
        try:
            if len(items) != 0:
                for it in items:
                    f = "".join(it.split(","))
                    big_list.append(f)
            else:
                big_list.append("0")
        except:
            pass


    ff_l = []
    f_tup = tuple(big_list)
    ff_l.append((f_tup))
    print(ff_l)
    print(len(ff_l[0]))
    insertDB(ff_l)
    print(big_list)






# create table Tokyo_TSN (id int not null primary key auto_increment,
# Python  float,
# Glang  float,
# Echo  float,
# Gin  float,
# Docker  float,
# openstack  float,
# LastTime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP) engine=InnoDB  charset=utf8;
# #
