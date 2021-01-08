import time
import requests
import uuid
import json
import re
import os
import pandas as pd
from bs4 import BeautifulSoup

DEFAULT_FORDER = os.path.dirname(__file__)

DATA_FORDER = os.path.join(DEFAULT_FORDER, 'data')
PIC_FORDER = os.path.join(DEFAULT_FORDER, 'pic')


def spider(user_id='',
           urls=[],
           antiminer=False,
           header={},
           miner_param={},
           timing='',
           start_time=''):
    timer(timing, start_time)

    data = {}

    for url in urls:
        doc = html_grab(url['method'], url['url'], antiminer, header)
        result = None
        datalist = {}
        key = url['url']
        for miner_method, miner_rule in miner_param.items():
            if miner_method == 'fuzzy':
                result = fuzzy_search(doc, miner_rule)
            elif miner_method == 'content':
                result = grab_by_content(doc, miner_rule)
            elif miner_method == 'id':
                result = grab_by_id(doc, miner_rule)
            elif miner_method == 'table':
                result = grab_by_table(doc, miner_rule)
            elif miner_method == 'num':
                result = num_search(doc, miner_rule)
            elif miner_method == 'pic':
                result = grab_by_pic(doc, miner_rule, url)
            else:
                log('errorlog: no miner method matched')
            datalist[miner_method] = result
        data[key] = datalist

    return data


def timer(timing='instant', start_time=''):
    log('worklog: start timer')
    if timing != 'instant':
        start_time = time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M"))
        localtime = time.time()
        while localtime < start_time:
            time.sleep(1)
            localtime = time.time()
            log('worklog: timer is waiting for start time')
    log('worklog: end timer')
    return


def html_grab(request_method='', url='', antiminer=False, header={}):
    log('worklog: grab html source file')
    doc = None
    if antiminer == False:
        log('worklog: no antiminer')
        if request_method == 'get':
            log('worklog: take get method')
            doc = requests.get(url)
        elif request_method == 'post':
            log('worklog: take post method')
            doc = requests.post(url)
        else:
            log('errorlog: mistake in request method')
            exit(1)
    else:
        log('worklog: has antiminer')
        if request_method == 'get':
            log('worklog: take get method')
            doc = requests.get(url, headers=header)
        elif request_method == 'post':
            log('worklog: take post method')
            doc = requests.post(url, headers=header)
        else:
            log('errorlog: mistake in request method')
            exit(1)

    log('worklog: get html source file')
    doc.encoding = 'utf-8'
    return doc.text

def num_search(html='', dic={}):
    log('worklog: num searching')
    soup = BeautifulSoup(html, features='lxml')

    result = {}
    res=[]
    for key, word in dic.items():
        reg = re.compile('.*{}.*'.format(word))
        tag = soup.find_all(text=reg)
        print(tag)
        if len(tag) != 0:
            for i in tag:
                print(i)
                print()
                for j in re.findall(r'(([1-9][0-9]*\.?[0-9]*)|(\.[0-9]+))([Ee][+-]?[0-9]+)?', i):
                    res.append(re.findall(r'(([1-9][0-9]*\.?[0-9]*)|(\.[0-9]+))([Ee][+-]?[0-9]+)?', i)[0][0])
            result[key] = res
        else:
            result[key] = []

    return result

def fuzzy_search(html='', dic={}):
    log('worklog: fuzzy searching')
    soup = BeautifulSoup(html, features='lxml')

    result = {}
    for key, word in dic.items():
        reg = re.compile('.*{}.*'.format(word))
        tag = soup.find_all(text=reg)
        if len(tag) != 0:
            result[key] = tag
        else:
            result[key] = []

    return result


def grab_by_content(html='', dic={}):
    log('worklog: run grab_by_content')

    result = {}
    for key, rule in dic.items():
        match = re.findall(rule, html)
        if len(match) != 0:
            result[key] = match
        else:
            result[key] = ''
    return result


def grab_by_id(html='', dic={}):
    log('worklog: run grab_by_id')

    result = {}
    for key, id in dic.items():
        soup = BeautifulSoup(html, features='lxml')
        item = soup.select('#{}'.format(id))
        if len(item) != 0:
            result[key] = str(item[0])
        else:
            result[key] = ''

    return result


def grab_by_table(html='', dic={}):
    log('worklog: run grab_by_table')
    soup = BeautifulSoup(html, 'lxml')
    tables = soup.select('table')
    resultlist = []
    for table in tables:
        singletable = pd.concat(pd.read_html(table.prettify()))
        for i in range(len(singletable)):
            column = []
            for j in range(len(singletable.iloc[i])):
                if singletable.iloc[i][j] not in column:
                    column.append(singletable.iloc[i][j])
            if not (len(column) == 1 and pd.isnull(column[0])) and len(column) > 0:  # 去除异常值
                resultlist.append(column)
    return {'table': resultlist}


def grab_by_pic(html='', dic={}, url=''):
    log('worklog: run grab_by_pic')

    result = {}
    for key, id in dic.items():
        print(key)
        print(id)
        soup = BeautifulSoup(html, features='lxml')
        item = soup.select('#{}'.format(id))
        if item:
            # 存在该标签
            img = item[0]
            # print(img['src'])
            src = str(img['src'])
            if src.startswith('//'):
                # 根路径
                src = 'http:' + src
            if src.startswith('/'):
                src = url + src
                # 相对路径

            r = requests.get(src)
            result[key] = (src, r.content)
            print(result)
    return result


def write_data_file(user_id, data):
    filepath = os.path.join(DATA_FORDER, user_id + '.json')
    file = None
    dic = {}
    t_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    if os.path.exists(filepath):
        file = open(filepath, 'r')
        dic = json.load(file)
        file.close()
        dic[t_time] = data
    else:
        dic[t_time] = data

    file = open(filepath, 'w')
    file.write(json.dumps(dic, ensure_ascii=False))


def read_data_file(user_id):
    filepath = os.path.join(DATA_FORDER, user_id + '.json')
    file = open(filepath, 'r')
    dic = json.load(file)
    return dic[user_id]


def write_pic(user_id, data):
    log('worklog: run write_pic')
    dirpath = os.path.join(PIC_FORDER, user_id)
    os.mkdir(dirpath)
    for i, dic in enumerate(data):
        subdirpath = os.path.join(dirpath, str(i))
        os.mkdir(subdirpath)
        for key, turple in dic.items():
            src = turple[0]
            content = turple[1]

            loc = src.rfind('.')
            suffix = src[loc:]
            filename = str(uuid.uuid1()).replace('-', '') + suffix
            filepath = os.path.join(subdirpath, filename)
            with open(filepath, 'wb') as f:
                f.write(content)


def log(message):
    print(message)


if __name__ == "__main__":
    '''
    write_data_file('1',[{'hello':'data'},{'byebye':'data1'}])
    print(read_data_file('1'))
    exit(0)
    '''

    get = spider(user_id='test1',
                 urls=[{'method': 'get', 'url': 'http://www.ccgp.gov.cn/cggg/zygg/zbgg/202101/t20210104_15746519.htm'},
                       {'method': 'get', 'url': 'http://xinhuanet.com'}],
                 antiminer=False,
                 header={},
                 miner_param={
                     'fuzzy': {'1': '供应商', '2': '马飞', '3': '习近平'},
                     'table': {},
                     'id': {'headline': 'headline'}
                 },
                 timing='instant',
                 start_time='')
    print(get)
    write_data_file('1', get)