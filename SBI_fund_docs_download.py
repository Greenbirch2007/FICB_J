#! -*- utf-8 -*-
import copy
import re
import json
import time
from lxml import etree
from selenium import webdriver
import csv



import requests
def getFile(url,filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:  # 切片之后优化了命名
            f.write(response.content)
            f.close()
    else:
        pass

def use_selenium_redirect_url(url):


    driver.get(url)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="MAINAREA02_780"]/div[1]/div[2]/div[3]/div[2]/div/p/a').click()

    time.sleep(1)
    # 跳转到最新页面
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(3)
    # driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr/td/table/tbody/tr[3]/td[3]/a/img").click()
    driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr/td/table/tbody/tr[4]/td[2]/a/img").click()

    driver.switch_to.window(driver.window_handles[-1])


    currentUrl = driver.current_url
    return currentUrl


def readjsonfile(filename):
    with open(filename, 'r', encoding='utf-8') as fw:
        s = json.load(fw)
        return s







if __name__=="__main__":
    driver = webdriver.Chrome()
    resultjson = readjsonfile("top30_sbi_trust.json")
    result_url = []
    result_title = []
    for item in resultjson:
        currentUrl = use_selenium_redirect_url(item["url"])
        filename = "C:\sbi_fund_docs_top30\{0}2.pdf".format(item["title"])
        getFile(currentUrl,filename)












