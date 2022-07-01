
#! -*- utf-8 -*-
import copy
import re
import json
import time
from lxml import etree
from selenium import webdriver
import csv
driver = webdriver.Chrome()
def use_selenium_headless_getdt(url):
    driver.get(url)
    time.sleep(1)
    html = driver.page_source
    return html


def list_null(list_content):
    if list_content !=[]:
        result = list_content
    else:
        result = ["null"]
    return result

json_list =[]
url_list= []
url ="https://site0.sbisec.co.jp/marble/fund/detail/achievement.do?s_rflg=1&Param6=203311187&int_fd=fund:psearch:search_result"


html = use_selenium_headless_getdt(url)

selector = etree.HTML(html)
date_of_established = selector.xpath('//*[@id="MAINAREA02_780"]/div[5]/div[1]/table/tbody/tr[39]/td/text()')
pattern = re.compile('<th class="alC">3カ月</th>.*?<td .*?>(.*?)</td>', re.S)
items = re.findall(pattern, html)

yield_since_established = items[0].split()
print(yield_since_established)

title = selector.xpath('//*[@id="MAINAREA02_780"]/div[1]/div[1]/div/h3/text()')
pattern = re.compile('<p class="fl01" style="margin-left:24px;">(.*?)</p>', re.S)
items = re.findall(pattern, html)
firm = items[0].split()[0]

pattern = re.compile("運用方針.*?<td>(.*?)</td>", re.S)
items = re.findall(pattern, html)
strategy = items[0].split()

pattern = re.compile("税込.*?<td>(.*?)</td>", re.S)
items = re.findall(pattern, html)
fee = items[1].split()[0]
last_day = selector.xpath('//*[@id="MAINAREA02_780"]/div[5]/div[1]/table/tbody/tr[41]/td/text()')
pattern = re.compile('<td class="alR">(.*?)</td>', re.S)
items = re.findall(pattern, html)
assert_ = items[0].split()

last_price = selector.xpath(
    '//*[@id="MAINAREA02_780"]/div[2]/div[1]/div/div/div/div/div/div/div/table/tbody/tr[1]/td[2]/div/div[1]/text()')

# bonus = selector.xpath('//*[@id="MAINAREA02_780"]/div[6]/div[2]/div[3]/div[2]/table/tbody/tr[2]/td/text()')
# print(bonus)
# f_bonus = bonus[0].split()[0].split("円")[0]

top_price = selector.xpath('//*[@id="MAINAREA02_780"]/div[2]/div[2]/table/tbody/tr[2]/td/text()')
f_top_price = "".join(top_price[0].split(",")).split("円")[0]

low_price = selector.xpath('//*[@id="MAINAREA02_780"]/div[2]/div[2]/table/tbody/tr[3]/td/text()')
top_price_date = selector.xpath('//*[@id="MAINAREA02_780"]/div[2]/div[2]/table/tbody/tr[2]/td/span/text()')
low_price_date = selector.xpath('//*[@id="MAINAREA02_780"]/div[2]/div[2]/table/tbody/tr[3]/td/span/text()')

f_low_price = "".join(low_price[0].split(",")).split("円")[0]


result = {}

result["title"] = "".join(list_null(title)).split()[0]
result["firm"] = "".join(list_null(firm)).split()[0]
result["strategy"] = "".join(list_null(strategy)).split()[0]
result["last_price"] = "".join(list_null(last_price)).split()[0]
result["date_of_established"] = "".join(list_null(date_of_established)).split()[0]
result["last_day"] = "".join(list_null(last_day)).split()[0]
# result["bonus"] = "".join(list_null([f_bonus])).split()[0]
result["low_price"] = "".join(list_null([f_low_price])).split()[0]
result["top_price"] = "".join(list_null([f_top_price])).split()[0]
result["top_price_date"] = "".join(list_null([top_price_date])).split()[0]
result["low_price_date"] = "".join(list_null([low_price_date])).split()[0]
result["fee"] = "".join(list_null(fee)).split()[0]
result["assert_"] = "".join(list_null(assert_)).split()[0]

json_result = copy.deepcopy(result)
json_list.append(json_result)
json_list_tsv = [json_result["title"], json_result["firm"], json_result["last_price"], json_result["top_price"],
                 json_result["low_price"], json_result["top_price_date"], json_result["low_price_date"],
                 json_result["firm"], json_result["yield_since_established"], json_result["date_of_established"],
                 json_result["last_day"], json_result["fee"], json_result["assert_"], json_result["strategy"],
                 ]
# print(json_list)
#
# <p class="tooltip_before floatL md-l-utl-mt4">直近分配金(税引前)</p>.*?<td>(.*?)円<span
url = "https://site0.sbisec.co.jp/marble/fund/detail/achievement.do?s_rflg=1&Param6=203311187&int_fd=fund:psearch:search_result"
html = use_selenium_headless_getdt(url)

# re.compile("直近分配金(税引前).*?<td>(.*?)</td>", re.S)
# pattern = re.compile('<p class="tooltip_before floatL md-l-utl-mt4">直近分配金(税引前)</p>(.*?)円<span class="fGray01">', re.S)
# items = re.findall(pattern, html)
# selector = etree.HTML(html)
# top_price = selector.xpath('//*[@id="MAINAREA02_780"]/div[2]/div[2]/table/tbody/tr[2]/td/text()')
# f_top_price = "".join(top_price[0].split(",")).split("円")[0]
#
# low_price = selector.xpath('//*[@id="MAINAREA02_780"]/div[2]/div[2]/table/tbody/tr[3]/td/text()')
#
# f_low_price = "".join(low_price[0].split(",")).split("円")[0]


print(items)

# 直近分配金(税引前)

#過去分配金のうち、直近の分配実績と決算日を表示しております。<br></p></div>.*?<td>(.*?)円.*?<span class="fGray01">
# <p class="tooltip_before floatL md-l-utl-mt4">直近分配金(税引前)</p>(.*?)円<span class="fGray01">