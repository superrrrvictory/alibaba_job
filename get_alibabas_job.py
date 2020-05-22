import requests
import json
import pandas as pd
from tqdm import tqdm
import time
import random
from datetime import datetime

url = 'https://talent.alibaba.com/position/search?'
print("请输入需要查找的起始页码:")
start = input()
print("请输入需要查找的末尾页码：")
end = input()
datas = [{"key":"","pageSize":10,"pageIndex":i,"channel":"group_official_site","_csrf":"263ee632-eb11-4da2-9358-e59eb508e1f8","language":"zh"}
         for i in range(int(start)-1,int(end))]
user_agent = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ','Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1','Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50','Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)']
header = {'user-agent':random.choice(user_agent),
           'content-type': 'application/json;charset=UTF-8'}
# respond = requests.post(url,data=json.dumps(datas[0]),headers=header)
# job_list = json.loads(respond.content)

job_datas = []

for data in tqdm(datas):
    try:
        respond = requests.post(url,data=json.dumps(data),headers=header)
        job_list = json.loads(respond.content)
        job_data = job_list['content']['datas']
        job_datas.extend(job_data)
        time.sleep(random.randint(1,2))
    except Exception as e:
        print(e)
        pass

job_datas1 =job_datas[:]

for i in tqdm(range(len(job_datas1))):
    job_datas1[i]['experience'] = job_datas[i]['experience']['from']
    timestamp = job_datas[i]['publishTime']/1000
    time_local = time.localtime(timestamp)
    job_datas1[i]['publishTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time_local)

job_datas2 = pd.DataFrame(job_datas1)
job_datas2.to_csv('alibaba_jobs.csv',encoding='utf_8_sig')
