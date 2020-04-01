#!/usr/bin/env python
# coding: utf-8

# In[2]:


# requet可以用於80%以上的網站
# 若碰到javacript，改用selenium
# HTML-->Pandas.read_html
# CSV-->Pandas.read_csv
# JSON-->Json.dumps
# HTML中的某個元素-->beautifulsoup


# In[7]:


import requests
req = requests.get('http://www.wibibi.com/info.php?tid=116')


# In[9]:


# 取得網頁原始碼
req.text


# In[10]:


# 轉碼
req.encoding = 'utf-8' # 'big5'
req.text


# In[13]:


# 2步驟
# 1. 存成html檔
# 2. 用pandas讀取html檔

# 存檔
f = open('test.html', 'w', encoding='utf-8')
f.write(req.text)
f.close()


# In[14]:


# 讀檔並轉成DataFrame
import pandas as pd
dfs = pd.read_html('test.html')


# In[16]:


# 瀏覽
dfs[1]


# In[18]:


# 不存檔直接轉成DataFrame
# StringIO(req.text) --> 將字串存成一個檔案
from io import StringIO
dfs = pd.read_html(StringIO(req.text))
dfs[1]
