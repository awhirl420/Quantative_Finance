# Quarterly Report
import requests
res = requests.get('https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=1101&SYEAR=2017&SSEASON=3&REPORT_ID=C')
res.encoding = 'big5' #utf-8

from io import StringIO
import pandas as pd

dfs = pd.read_html(StringIO(res.text))

# for sid in ['1101', '2330']:
import time
import os

# if no floder "course 9"
if 'course9' not in os.listdir():
    
    # make one
    os.mkdir('course9')

# stock list
sid = ['1101' , '2330']

for s in sid:
    
    # get data
    res = requests.get('https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=' + s + '&SYEAR=2017&SSEASON=3&REPORT_ID=C')
    res.encoding = 'big5'
    
    # save path
    path = os.path.join('course9', s + '.html')
    
    # save file
    f = open(path, 'w', encoding='utf-8')
    f.write(res.text)
    f.close()
    
    print(s)
    
    # take a break
    time.sleep(20)


dfs = []

for s in sid:
    
    path = os.path.join('course9', s + '.html')
    
    dfs.append(pd.read_html(path, encoding='utf-8'))

dfs[1][1].head(10)
