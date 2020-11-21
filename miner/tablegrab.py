# coding=utf-8
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

html = '''<div id="songs-list">
<h2 class="title">经典老歌</h2>
<p class="introduction">
经典老歌列表
</p>
<ul id="list" class="list-group">
<li data-view="2">一路上有你</li>
<li data-view="7">
<a href="/2.mp3" singer="任贤齐">沧海一声笑</a>
</li>
<li data-view="4" class="active">
<a href="/3.mp3" singer="齐秦">往事随风</a>
</li>
<li data-view="6"><a href="/4.mp3" singer="beyond">光辉岁月</a></li>
<li data-view="5"><a href="/5.mp3" singer="陈慧琳">记事本</a></li>
<li data-view="5">
<a href="/6.mp3" singer="邓丽君">但愿人长久</a>
</li>
</ul>
</div>'''

# 根据id爬取数据,id唯一
# 返回标签下内容
def get_by_id(html, id):
    soup = BeautifulSoup(html, 'lxml')
    item = soup.select('#{}'.format(id))
    return item[0]

# 测试 get_by_id
# url = 'http://www.njgp.gov.cn/cgxx/cgcjjg/202006/t20200602_129953.html'
# r = requests.get(url)
# r.encoding = r.apparent_encoding
# print(r.text)
# result = get_by_id(r.text, 'siteordoccount')      
# print(result)
result = get_by_id(html, 'list')
print(result)


# 爬取表格标签, 横式表格，多行多列，只用于规则表格(每行列数相同)
# 返回DataFrame
def get_table(html):
    soup = BeautifulSoup(html, 'lxml')

    table = soup.table
    thead = table.thead
    tbody = table.tbody
    trs = tbody.select('tr')
    head = []
    ths = []

    # 有表头
    if thead:
        ths = thead.select('th')
    # 无表头，第一行为表头
    else:
        ths = trs[0].select('td')
        trs.pop(0)
    for th in ths:
        head.append(th.string)
    # print(head)

    df = pd.DataFrame(columns=head)
    index = 0
    for tr in trs:
        tds = tr.select('td')
        col = []
        for td in tds:
            col.append(td.string)
        # print(col)
        df.loc[index] = col
        index += 1
    
    return df

# 测试 get_table
# path = './thead.html'
# html = open(path, 'r', encoding='utf-8')
# html = '<table cellspacing="0" cellpadding="0" style="width: 100%; background-color: white; border: 1px solid rgb(228, 230, 231); text-align: left; border-collapse: collapse; margin: 0px auto;"><thead><tr><th contenteditable="false" style="background-color: white;border: 1px solid #ddd;width:8%;"><span>序号</span></th><th contenteditable="false" style="background-color: white;border: 1px solid #ddd;width:8%;"><span>标项名称</span></th><th contenteditable="false" style="background-color: white;border: 1px solid #ddd;width:8%;"><span>总价(元)</span></th><th contenteditable="false" style="background-color: white;border: 1px solid #ddd;width:18%;"><span>中标供应商名称</span></th><th contenteditable="false" style="background-color: white;border: 1px solid #ddd;width:29%;"><span>中标供应商地址</span></th><th contenteditable="false" style="background-color: white;border: 1px solid #ddd;width:23%;"><span>中标供应商统一社会信用代码</span></th><th contenteditable="false" style="background-color: white;border: 1px solid #ddd;width:7%;"><span>备注</span></th></tr></thead><tbody><tr style="padding:5px;"><td style="border: 1px solid #ddd;"><div>1</div></td><td style="border: 1px solid #ddd;"><div></div></td><td style="border: 1px solid #ddd;"><div>345600.00</div></td><td style="border: 1px solid #ddd"><div>北京广顺锦隆汽车销售服务有限责任公司</div></td><td style="border: 1px solid #ddd"><div>北京北京市朝阳区北京市朝阳区来广营乡新北路甲6号院内</div></td><td style="border: 1px solid #ddd"><div>911101056977082860</div></td><td style="border: 1px solid #ddd"><div></div></td></tr></tbody></table>'
# html_thead = '<table cellspacing="0" cellpadding="0" style="width: 100%;background-color: white;border: solid 1px #e4e6e7;text-align: left;border-collapse: collapse;"><thead><tr><th contenteditable="false" style="background-color: white;border: 1px solid #ddd;width:8%;"><span>序号</span></th><th contenteditable="false" style="background-color: white;border: 1px solid #ddd;width:8%;"><span>标项名称</span></th><th contenteditable="false" style="background-color: white;border: 1px solid #ddd;width:8%;"><span>总价(元)</span></th><th contenteditable="false" style="background-color: white;border: 1px solid #ddd;width:18%;"><span>中标供应商名称</span></th><th contenteditable="false" style="background-color: white;border: 1px solid #ddd;width:29%;"><span>中标供应商地址</span></th><th contenteditable="false" style="background-color: white;border: 1px solid #ddd;width:23%;"><span>中标供应商统一社会信用代码</span></th><th contenteditable="false" style="background-color: white;border: 1px solid #ddd;width:7%;"><span>备注</span></th></tr></thead><tbody><tr style="padding:5px;"><td style="border: 1px solid #ddd;"><div>1</div></td><td style="border: 1px solid #ddd;"><div></div></td><td style="border: 1px solid #ddd;"><div>345600.00</div></td><td style="border: 1px solid #ddd"><div>北京广顺锦隆汽车销售服务有限责任公司</div></td><td style="border: 1px solid #ddd"><div>北京北京市朝阳区北京市朝阳区来广营乡新北路甲6号院内</div></td><td style="border: 1px solid #ddd"><div>911101056977082860</div></td><td style="border: 1px solid #ddd"><div></div></td></tr></tbody></table>'
# result = get_table(html)                # 无thead
# result2 = get_table(html_thead)         # 有thead
# print(result)
# print(result2)


# 爬取表格，全适用，不规则也适用，针对display:none这种暗地传数据
# 返回list，每一项对应一个表格

def get_all_tables(html):
    soup = BeautifulSoup(html, 'lxml')

    tables = soup.select('table')
    result = []

    for table in tables:
        ths = table.select('thead th')
        trs = table.select('tbody tr')
        
        row_list = []
        head = []
        if ths:
            for th in ths:
                head.append(th.string)
            row_list.append(head)
        for tr in trs:
            row = []
            tds = tr.select('td')
            for td in tds:
                row.append(td.string)
            row_list.append(row)
        result.append(row_list)
    return result

# 测试 get_all_tables
# path = './thead.html'
# html = open(path, 'r', encoding='utf-8')
# result = get_all_tables(html.read())
# print(result)


# 正则匹配爬取信息
# 返回匹配内容
def get_by_re(html, rule, mod):
    results = re.findall(rule, html, mod)
    return results

# 测试 get_by_re
# rule = '<li.*?href="(.*?)".*?singer="(.*?)">(.*?)</a>'          # 使用分组，会直接返回分组内容
# results = get_by_re(html, rule, re.S)
# print(results)