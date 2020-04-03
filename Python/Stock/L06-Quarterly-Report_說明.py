#!/usr/bin/env python
# coding: utf-8

# In[3]:


# 財報可以用來理解公司如何收集資金、進行投資、提高利潤
import requests

res = requests.get('https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=1101&SYEAR=2017&SSEASON=3&REPORT_ID=C')


# In[8]:


from io import StringIO
import pandas as pd

res.encoding = 'big5'
dfs = pd.read_html(StringIO(res.text))


# In[21]:


# for sid in ['1101', '2330']
import os
import time

sid = ['1101', '2330']

for s in sid:
    res = requests.get('https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID='+ s +'&SYEAR=2017&SSEASON=3&REPORT_ID=C')
    res.encoding = 'big5'
    
    # 根據作業系統，選擇斜線 windows/，windows\
    path = os.path.join('course9', s + '.html')
    print(path)
    
    f = open(path, 'w')
    f.write(res.text)
    f.close()
    
    time.sleep(10)


# In[30]:


dfs = []
for s in sid:
    path = os.path.join('course9', s + '.html')
    dfs.append(pd.read_html(path))


# In[31]:


dfs[0]


# In[32]:


# REPORT_ID: 個別財報(A) 個體財報(B) 合併報表(C)
# C -> B

import requests
res = requests.get('https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=1101&SYEAR=2017&SSEASON=3&REPORT_ID=C')
res.encoding = 'big5' #也可以試 utf-8


# In[33]:


from io import StringIO
import pandas as pd

# 將 res.text 用 StringIO 轉成 檔案 再用 pd.read_html 將 html文字檔轉成 dateframe
dfs = pd.read_html(StringIO(res.text))


# In[36]:


dfs[1]


# In[38]:


# for sid in ['1101', '2330']
import time
import os

# 假如沒有 course9 這個資料夾
if 'course9' not in os.listdir():

    # 就創建一個
    os.mkdir('course9')
    
# 想要爬的股票代號
sid = ['1101', '2330']

# 對於每一筆股票代號
for s in sid:
    
    # 抓取它的html檔
    res = requests.get('https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=1101&SYEAR=2017&SSEASON=3&REPORT_ID=C')
    res.encoding = 'big5'
    
    # 設定存檔的路徑 ex: course9\1101.html
    path = os.path.join('course9', s + '.html')
    
    # 將檔案打開，寫入html，然後關閉
    f = open(path, 'w', encoding='utf-8')
    f.write(res.text)
    f.close()
    
    print(s)
    
    # 休息20秒，再跑下一支股票
    time.sleep(20)


# In[39]:


dfs = []

# 對於每一支股票
for s in sid:
    
    # 將檔案 ex: course9\1101.html拿出來
    path = os.path.join('course9', s + '.html')
    
    # 存在dfs中
    dfs.append(pd.read_html(path, encoding='utf-8'))


# In[41]:


# 抓取2330的第一張dataFrame前10個row

dfs[1][1].head(10)

