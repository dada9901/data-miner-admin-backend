from bs4 import BeautifulSoup
import re
import sys
import json
import requests

# http://www.ccgp.gov.cn/cggg/zygg/zbgg/202011/t20201113_15420850.htm
# 概要数据的中文key到英文key的映射
translate_summary = {
    '采购项目名称':'project_name',
    '品目':'project_category',
    '采购单位':'unit_name',
    '行政区域':'region',
    '公告时间':'announcement_time',
    '评审专家名单':'judges',
    '总中标金额':'total_bid_amount',
    '项目联系人':'project_contacts',
    '项目联系电话':'project_phone',
    '采购单位地址':'unit_address',
    '采购单位联系方式':'unit_phone',
    '代理机构名称':'proxy_name',
    '代理机构地址':'proxy_address',
    '代理机构联系方式':'proxy_contacts',
}

# 标的信息的columns key
subject_columns = [
    'no',
    'supplier',
    'name',
    'brand',
    'category',
    'amount',
    'price'
]

# 对公告概要进行解析
def parse_summary(doc, data):
    # 获取公告概要的表格
    summary = doc.find(name = 'div', class_ = 'table')

    # 获取公告概要中所有的数据,并根据数据名填入data中
    table_data = summary.find_all(name='td', class_='title')
    for td in table_data:
        if td.string in translate_summary.keys():
            data[translate_summary[td.string]]=td.next_sibling.string


# 对公告正文进行解析
def parse_body(doc, data):
    body  = doc.find(name = 'div', class_ = 'vF_detail_content')
    node_p = body.find(name = 'p')
    node_p = parse_no(node_p, data)
    node_p = parse_v_bidders(node_p, data)
    node_p = parse_proxy(node_p, data)
    node_p = parse_others(node_p, data)

    parse_subject(body, data)

# 解析项目编号
def parse_no(node, data):
    data['no'] = node.strong.string
    
    return node.next_sibling

# 解析项目的中标信息
def parse_v_bidders(node, data):
    v_bidders=[]
    bidder = node
    while bidder.string==None or re.search('供应商名称',bidder.string)==None:
        bidder = bidder.next_sibling

    while bidder.string!=None and re.search('供应商名称',bidder.string)!=None:
        bidder_dict = {}
        address = bidder.next_sibling
        amount = address.next_sibling

        bidder_dict['name']=bidder.string
        bidder_dict['address']=address.string
        bidder_dict['amount']=amount.string
        v_bidders.append(bidder_dict)

        bidder = amount.next_sibling.next_sibling
    
    data['v_bidders']=v_bidders

    return bidder

# 解析项目的代理服务信息 
def parse_proxy(node, data):
    while node.string==None or re.search('代理费收费标准',node.string)==None:
        node = node.next_sibling
    proxy = {}
    proxy['standard']=node.string
    proxy['amount']=node.next_sibling.next_sibling.string
    data['proxy_service']=proxy

    return node.next_sibling.next_sibling.next_sibling.next_sibling

# 解析项目的公告期限和其他补充事宜
def parse_others(node, data):
    node = node.next_sibling
    data['publicity_time']=node.string
    data['others']=node.next_sibling.next_sibling.string


# 解析项目的主要标的信息
def parse_subject(doc, data):
    subject_list=[]
    table = doc.find(name = 'table').find_all(name = 'tr')
    num=1
    while num < len(table):
        tr = table[num]
        subject = {}
        for i,td in enumerate(tr.find_all(name = 'td')):
            subject[subject_columns[i]]=td.string
        subject_list.append(subject)
        num+=3
    data['subject_info']=subject_list
    return


# 解析项目并且写入到filepath中
def parse_document(doc, filepath):
    soup = BeautifulSoup(doc, features='html.parser')
    detail_document = soup.find(name = 'div',class_='vF_detail_main')
    data = {}
    parse_summary(detail_document, data)
    parse_body(detail_document, data)
    
    f = open('test', mode = 'w', encoding = 'utf-8')
    json.dump(data, f, ensure_ascii=False, indent=4)
    return


def grab(url):
    doc = requests.get(url)
    doc.encoding='utf-8'
    return doc.text


def main(argv):
    doc = grab(argv[1])
    parse_document(doc, argv[2])

if __name__=="__main__":
    main(sys.argv)
