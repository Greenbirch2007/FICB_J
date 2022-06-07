import re

url = "https://site0.sbisec.co.jp/marble/fund/detail/achievement.do?s_rflg=1&Param6=204312167&int_fd=fund:psearch:search_result"


import requests
res = requests.get(url)
res.encoding = res.apparent_encoding

# # 增加总资产,投资方法,费率的解析

# +".*?運用方針.*?<td>(.*?)<td>.'?信託報酬&nbsp;(税込)/年.*?<td>(.*?)<td>.'?信託財産留保額"
pattern = re.compile('<td class="alR">(.*?)</td>',re.S)
items = re.findall(pattern,res.text)
print(items[0].split())
#


pattern = re.compile("運用方針.*?<td>(.*?)</td>",re.S)
items = re.findall(pattern,res.text)
print(items[0].split())

pattern = re.compile("税込.*?<td>(.*?)</td>",re.S)
items = re.findall(pattern,res.text)
print(items[1].split()[0])



