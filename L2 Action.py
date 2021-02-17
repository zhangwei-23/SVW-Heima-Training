# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 21:29:07 2021

@author: zhangwei23
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd


# 得到页面的内容
def get_page_content(request_url):
    print(request_url)
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html=requests.get(request_url,headers=headers,timeout=20)
    content = html.text
    soup = BeautifulSoup(content,'html.parser')
    return soup

#分析当前页面投诉信息
def analysis(soup):
    df = pd.DataFrame(columns=['id','brand','car_model','type','desc','problem','datetime','status'])
    temp = soup.find('div',class_ = 'tslb_b')
    tr_list = temp.find_all('tr')
    for tr in tr_list:
        td_list = tr.find_all('td')
        if len(td_list)>0:
            id,brand,car_model,type,desc,problem,datetime,status = \
                td_list[0].text,td_list[1].text,td_list[2].text,td_list[3].text,\
                td_list[4].text,td_list[5].text,td_list[6].text,td_list[7].text
            
            #print(id,brand,car_model,type,desc,problem,datetime,status)
            temp = {}
            temp['id']= id
            temp['brand']= brand
            temp['car_modul']= car_model
            temp['type']= type
            temp['desc']= desc
            temp['problem']= problem
            temp['datetime']= datetime
            temp['status']= status
            df = df.append(temp,ignore_index = True)
        return df
    
result = pd.DataFrame(columns=['id','brand','car_model','type','desc','problem','datetime','status'])
                     
# 请求URL           
base_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-'     
page_num = 20
for i in range(page_num):
    request_url = base_url + str(i+1) + '.shtml' #当前页面url
    soup = get_page_content(request_url)         #得到soup解析
    df = analysis(soup)                          #通过soup解析，得到当前页面的dataframe
    result = result.append(df)

print(result)
result.to_csv('car_complain.csv',index=False)
result.to_excel('car_complain.xlsx',index=False)