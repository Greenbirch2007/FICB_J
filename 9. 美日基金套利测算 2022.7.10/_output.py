# !/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import datetime
import pymysql
import pandas as pd

from sqlalchemy import create_engine
import pymysql
import pandas as pd
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import datetime

engine_Nas_Mons = create_engine('mysql+pymysql://root:123456@localhost:3306/Trust')


sql_Nas_Mons = 'SELECT td29I31115A,td29I312223,td20431820A,td20431720A,Lasttime from sbi_trust_daily_dt; '

ln = os.getcwd()


def savedt():

    df_js225 = pd.read_sql_query(sql_Nas_Mons, engine_Nas_Mons)
    df_js225 = pd.DataFrame([x[0].split()[0] for x in df_js225.values.tolist()])


    excelFile3 = '{0}/{1}.xlsx'.format(ln, "sbi_trust_daily_dt")  # 处理了文件属于当前目录下！
    df_js225.to_excel(excelFile3)





if __name__ == '__main__':
    savedt()