# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import time
from bs4 import BeautifulSoup as BS
import requests
from time import sleep

# 构造获取广东省各单位（大学）列表的函数，参数传递页码。该请求为post请求
def get_univer(x):
    # s = requests.Session()
    headers = {
        'Accept':'application/xml, text/xml, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Host':'isisn.nsfc.gov.cn',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Referer':'https://isisn.nsfc.gov.cn/egrantindex/funcindex/get-orginfo?include=true&',
        'X-Requested-With':'XMLHttpRequest'
    }
    post_data = { #post_data内容直接复制F12大法里面的data
        '_search':'false',
        'nd':'1507443704974',
        'rows':'60', # 设置一页显示60行
        'page':x,
        'sidx':'orgId',
        'sord':'asc',
        'searchString':'nature^:A[tear]province^:%E5%B9%BF%E4%B8%9C'
    }
    url_path = r"https://isisn.nsfc.gov.cn/egrantindex/funcindex/get-orginfo?type=search"
    respo = requests.post(url_path, data = post_data, headers = headers)
    return respo.text

# 构造获取广东省各单位（医院）列表的函数。同上，参数传递页码，该请求为post请求
def get_hosp(x):
    # s = requests.Session()
    headers = {
        'Accept':'application/xml, text/xml, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Host':'isisn.nsfc.gov.cn',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Referer':'https://isisn.nsfc.gov.cn/egrantindex/funcindex/get-orginfo?include=true&',
        'X-Requested-With':'XMLHttpRequest'
    }
    post_data = {
        '_search':'false',
        'nd':'1507447046530',
        'rows':'60',
        'page':x,
        'sidx':'orgId',
        'sord':'asc',
        'searchString':'nature^:C[tear]province^:%E5%B9%BF%E4%B8%9C'
    }
    url_path = r"https://isisn.nsfc.gov.cn/egrantindex/funcindex/get-orginfo?type=search"
    respo = requests.post(url_path, data = post_data, headers = headers)
    return respo.text

# 解析上面的网页，收集单位列表
def get_list():
    soup1 = BS(get_univer(1),'lxml')
    soup2 = BS(get_hosp(1),'lxml')
    units = []
    for a in soup1.find_all('row'):
        units.append(a.find_all('cell')[1].text)
    for a in soup2.find_all('row'):
        units.append(a.find_all('cell')[1].text)
    return units

# 请求国自然项目的搜索结果，letpub网站接受get请求，参数传递param_data里面的参数，第一个是时间，第二个是页码
def get_fundings(x,y):
    # s = requests.Session()
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Host':'www.letpub.com.cn',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Referer':'http://www.letpub.com.cn/?page=grant&name=&person=%E7%8E%8B%E9%92%9F%E5%85%B4&no=&company=&addcomment_s1=0&addcomment_s2=0&addcomment_s3=0&money1=&money2=&startTime=2016&endTime=2016&subcategory=&searchsubmit=true&submit.x=37&submit.y=21&submit=advSearch'
    }
    param_data = {
        'page':'grant',
        'name':'',
        'person':'',
        'no':'817', #817代表17年医学科学部的所有项目
        'company':'',
        'addcomment_s1':'0',
        'addcomment_s2':'0',
        'addcomment_s3':'0',
        'money1':'',
        'money2':'',
        'startTime':x,
        'endTime':x,
        'subcategory':'',
        'currentpage':y
    }
    url_path = r"http://www.letpub.com.cn/"
    respo = requests.get(url_path, params = param_data, headers = headers)
    return respo.text

# 解析请求到的网页，收集所需数据，这里构造了一个含有列表的列表（矩阵），其实直接做成字符串的列表就可以了，增加了循环，拖延了时间
def get_table(x):
    soup = BS(x,'lxml')
    primlist = []
    for i in range(0,20):
        seclist = []
        i += 1
        s1 = 3*i-1
        for col in soup.find_all('table')[2].contents[s1]:
            seclist.append(col.text)
        s2 = 3*i
        for col in soup.find_all('table')[2].contents[s2]:
            seclist.append(col.text)
        s3 = 3*i+1
        for col in soup.find_all('table')[2].contents[s3]:
            seclist.append(col.text)
        if seclist[1] in get_list() and seclist[3][0:3] == '817': #进一步限定条件，出现在单位列表中的才收集，并在屏幕上打印"matched"
            print "matched"
            primlist.append(seclist)
    return primlist

# 将数据写成文件
def write_table(x):
    table_file = open("output.txt",'w')
    for line in x:
        line_txt = '\t'.join(line)
        table_file.write(line_txt+'\n')
    table_file.close
if __name__ == '__main__':
    total_table = []
    for i in range(0,496):
        try:
            total_table.extend(get_table(get_fundings(2017,i+1)))
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
        print str(i)+'/496 completed' #及时汇报进度
    write_table(total_table)
