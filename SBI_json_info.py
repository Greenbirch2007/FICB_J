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
    for onepage in range(21):
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

            community_code = selector.xpath('//*[@id="MAINAREA02_780"]/div[5]/div[1]/table/tbody/tr[7]/td/text()')
            pattern = re.compile("税込.*?<td>(.*?)</td>", re.S)
            items = re.findall(pattern,html)
            fee = items[1].split()[0]
            last_day = selector.xpath('//*[@id="MAINAREA02_780"]/div[5]/div[1]/table/tbody/tr[41]/td/text()')
            pattern = re.compile('<td class="alR">(.*?)</td>', re.S)
            items = re.findall(pattern,html)
            assert_ = items[0].split()
            result = {}


            result["title"] = "".join(list_null(title)).split()[0]
            result["firm"] = "".join(list_null(firm)).split()[0]
            result["strategy"] = "".join(list_null(strategy)).split()[0]
            result["yield_since_established"] = "".join(list_null(yield_since_established)).split()[0]
            result["date_of_established"] = "".join(list_null(date_of_established)).split()[0]
            result["last_day"] = "".join(list_null(last_day)).split()[0]
            result["community_code"] = "".join(list_null(community_code)).split()[0]
            result["fee"] = "".join(list_null(fee)).split()[0]
            result["assert_"] = "".join(list_null(assert_)).split()[0]
            result["url"] = oneurl
            print(result)
            json_result = copy.deepcopy(result)
            json_list.append(json_result)
            json_list_tsv =[json_result["title"],json_result["firm"],json_result["yield_since_established"],json_result["date_of_established"],json_result["last_day"],json_result["fee"],json_result["assert_"],json_result["strategy"],json_result["url"]]
            print(json_list)
            writeintoTSV_file("sbi_trust.tsv",json_list_tsv)

        except:
            pass

    writeinto_jsonfile("sbi_trust.json",json_list)








