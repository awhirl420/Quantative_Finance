#!/usr/bin/env python
# coding: utf-8

# In[1]:


# KD的意義
# 大家考太爛，重新分布成績
# 新成績 = (分數-最低)/(最高-最低)*100


# In[2]:


# RSV = (股價-n1天內最低)/(n1天內最高-n1天內最低)*100
# K:RSV平滑(n2天平均)
# D:K平滑(n3天平均)

# 黃金交叉:前一天，K<D，隔一天K>D


# In[3]:


from finlab.data import Data
data = Data()


# In[5]:


data.get('收盤價', 200)


# In[6]:


close = data.get('收盤價', 2000)
high = data.get('最高價', 2000)
low = data.get('最低價' ,2000)


# In[11]:


import talib
import pandas as pd


# In[12]:


# 前一次值成為後一次值 ffill()
kd = talib.STOCH(high['0050'].ffill().values,
                 low['0050'].ffill().values,
                 close['0050'].ffill().values,
                 fastk_period=9, slowk_period=3
                 , slowd_period=3, slowk_matype=1, slowd_matype=1)

k = pd.Series(kd[0], index=close['0050'].index)
d = pd.Series(kd[1], index=close['0050'].index)
print(k, d)


# In[16]:


# shift 昨日
buy = (k > d) & (k.shift() < d.shift()) & (k < 30)

k['2015'].plot()
d['2015'].plot()

# 把boolean轉換成數值
buy['2015'].astype(int).plot(secondary_y=True)


# In[18]:


close['0050']['2015'].plot()
buy['2015'].astype(int).plot(secondary_y=True)


# In[22]:


# 明天收盤價 close['0050'].shift(-1)
# 後天收盤價 close['0050'].shift(-2)

arr = [30]
for v, p in zip(buy[1:], close['0050'].shift(-2)/close['0050'].shift(-1)):
    arr.append(arr[-1]*p + v)
    
get_ipython().run_line_magic('matplotlib', 'inline')
close['0050'].plot(secondary_y=True, color='gray')
pd.Series(arr, index=close['0050'].index).plot()
buy.astype(int).plot()
(buy.astype(int).cumsum() + 30).plot()


