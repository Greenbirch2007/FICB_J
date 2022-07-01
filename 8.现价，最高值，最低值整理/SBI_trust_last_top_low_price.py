#! -*- utf-8 -*-
import copy
import re
import json
import time
from lxml import etree
from selenium import webdriver
import csv
driver = webdriver.Chrome()

pageNum = 20

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



def writeinto_jsonfile(filename,list_data):
    with open(filename, 'w', encoding='utf-8') as fw:
        json.dump(list_data, fw, indent=4, ensure_ascii=False)


def writeintoTSV_file(filename,data):
    with open(filename,'a', newline='\n', encoding="utf-8") as f_output:
        tsv_output = csv.writer(f_output, delimiter='\t')
        tsv_output.writerow(data)

if __name__=="__main__":
    json_list =[]
    url_list= []
    url ="https://site0.sbisec.co.jp/marble/fund/powersearch/fundpsearch.do?"
    html = use_selenium_headless_getdt(url)
    driver.find_element_by_xpath('//*[@id="tab_values_base"]/table/thead/tr/th[4]/a[2]/span').click()

    selector = etree.HTML(html)
    url_code = selector.xpath('//*[@id="tab_values_base"]/table/tbody/tr/td/a/@href')
    f_url = ["https://site0.sbisec.co.jp/{0}".format(x) for x in url_code]
    for item in f_url:
        print(item)
        url_list.append(item)
    # 开始翻页 20页吧

    for onepage in range(1,pageNum):
        driver.find_element_by_xpath('//*[@id="pageHolderLower"]/div/div[2]/p[3]/a').click()
        time.sleep(1)
        html = driver.page_source
        selector = etree.HTML(html)
        url_code = selector.xpath('//*[@id="tab_values_base"]/table/tbody/tr/td/a/@href')
        f_url = ["https://site0.sbisec.co.jp/{0}".format(x) for x in url_code]
        for item in f_url:
            print(item)
            url_list.append(item)

    for oneurl in url_list:
        driver.get(oneurl)
        html = driver.page_source
        time.sleep(1)


        selector = etree.HTML(html)
        try:

            date_of_established = selector.xpath('//*[@id="MAINAREA02_780"]/div[5]/div[1]/table/tbody/tr[39]/td/text()')
            pattern = re.compile('<th class="alC">設定来</th>.*?<td .*?>(.*?)</td>', re.S)
            items = re.findall(pattern, html)

            yield_since_established = items[0].split()
            print(yield_since_established)



            title = selector.xpath('//*[@id="MAINAREA02_780"]/div[1]/div[1]/div/h3/text()')
            pattern = re.compile('<p class="fl01" style="margin-left:24px;">(.*?)</p>', re.S)
            items = re.findall(pattern,html)
            firm = items[0].split()[0]

            pattern = re.compile("運用方針.*?<td>(.*?)</td>", re.S)
            items = re.findall(pattern,html)
            strategy = items[0].split()

            pattern = re.compile("税込.*?<td>(.*?)</td>", re.S)
            items = re.findall(pattern,html)
            fee = items[1].split()[0]
            last_day = selector.xpath('//*[@id="MAINAREA02_780"]/div[5]/div[1]/table/tbody/tr[41]/td/text()')
            pattern = re.compile('<td class="alR">(.*?)</td>', re.S)
            items = re.findall(pattern,html)
            assert_ = items[0].split()

            last_price = selector.xpath(
                '//*[@id="MAINAREA02_780"]/div[2]/div[1]/div/div/div/div/div/div/div/table/tbody/tr[1]/td[2]/div/div[1]/text()')
            last_price = ["".join(last_price[0].split(","))]
            pattern = re.compile('過去分配金のうち、直近の分配実績と決算日を表示しております。<br></p></div>.*?<td>(.*?)円.*?<span class="fGray01">',
                                 re.S)
            bonus = re.findall(pattern, html)
            top_price_date = selector.xpath(
                '//*[@id="MAINAREA02_780"]/div[2]/div[2]/table/tbody/tr[2]/td/span/text()')

            low_price_date = selector.xpath(
                '//*[@id="MAINAREA02_780"]/div[2]/div[2]/table/tbody/tr[3]/td/span/text()')

            top_price = selector.xpath('//*[@id="MAINAREA02_780"]/div[2]/div[2]/table/tbody/tr[2]/td/text()')
            f_top_price= "".join(top_price[0].split(",")).split("円")[0]


            low_price = selector.xpath('//*[@id="MAINAREA02_780"]/div[2]/div[2]/table/tbody/tr[3]/td/text()')

            f_low_price= "".join(low_price[0].split(",")).split("円")[0]

            result = {}

            result["title"] = "".join(list_null(title)).split()[0]
            result["firm"] = "".join(list_null(firm)).split()[0]
            result["strategy"] = "".join(list_null(strategy)).split()[0]
            result["last_price"] = "".join(list_null(last_price)).split()[0]
            result["date_of_established"] = "".join(list_null(date_of_established)).split()[0]
            result["yield_since_established"] = "".join(list_null(yield_since_established)).split()[0]
            result["last_day"] = "".join(list_null(last_day)).split()[0]
            result["bonus"] = "".join(list_null(bonus)).split()[0]
            result["low_price"] = "".join(list_null([f_low_price])).split()[0]
            result["top_price"] = "".join(list_null([f_top_price])).split()[0]
            result["fee"] = "".join(list_null(fee)).split()[0]
            result["top_price_date"] = "".join(list_null(top_price_date)).split()[0]
            result["low_price_date"] = "".join(list_null(low_price_date)).split()[0]
            result["assert_"] = "".join(list_null(assert_)).split()[0]
            result["url"] = oneurl
            json_result = copy.deepcopy(result)
            json_list.append(json_result)
            json_list_tsv =[json_result["title"],json_result["firm"],json_result["last_price"],json_result["top_price"],json_result["low_price"],json_result["top_price_date"],json_result["low_price_date"],json_result["firm"],json_result["yield_since_established"],json_result["date_of_established"],json_result["last_day"],json_result["fee"],json_result["assert_"],json_result["strategy"],json_result["url"]]
            print(json_result)
            writeintoTSV_file("SBI_trust_last_top_low_price.tsv",json_list_tsv)

        except:
            pass

    writeinto_jsonfile("SBI_trust_last_top_low_price.json",json_list)









