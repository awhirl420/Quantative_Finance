#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Series一條序列由index跟數值組成


# In[2]:


# DateFrame N條Series共用同一個index


# In[5]:


# 創建一條序列
import pandas as pd
s = pd.Series([1,2,3,4])
print(s)


# In[15]:


# 時間序列
date = pd.date_range('20180101', periods=6)
s = pd.Series([1,2,3,4,5,6], index=date)
print(s)


# In[13]:


s = pd.Series(0, index=date)
print(s)


# In[16]:


# 查找
s.loc['20180104']


# In[17]:


# 用index找
# 會秀出最後一筆資料
s.loc['20180102':'2018-01-04']


# In[18]:


# 第1個
s.iloc[0]


# In[20]:


# 不會秀出第4個
s.iloc[1:3]


# In[22]:


# 修改前
s = pd.Series([1,2,3,4,5,6], index=pd.date_range('20180101', periods=6))
print(s)


# In[59]:


# 修改後
l = [1,2,3,4,5,6]
date_index = pd.date_range('20180101', periods=6)

s = pd.Series(l, index=date_index)
print(s)


# In[28]:


s.max()
s.min()
s.mean()
s.std()


# In[29]:


# Series進階方法
s.cumsum()


# In[30]:


s.cumprod()


# In[32]:


# 移動窗格
print(s)
s.rolling(2).sum()


# In[36]:


s.rolling(2).max()
s.rolling(2).min()
s.rolling(2).mean()
s.rolling(2).std()


# In[43]:


print(s)
s + 1
s - 1
s * 2
s / 2
s > 3
s < 3


# In[44]:


# 繪圖
# 把圖畫在jupyter notebook上
get_ipython().run_line_magic('matplotlib', 'inline')
s.plot()


# In[47]:


# 綜合應用
s.loc[s > 3]


# In[48]:


# 其他寫法
larger_than_3 = s > 3
s.loc[larger_than_3]


# In[49]:


s.loc[s > 3] = s.loc[s > 3] + 1
s


# In[58]:


# 練習拆解
print(s)
(s.rolling(2).sum().cumsum() + 1).max()


# In[67]:


# 練習拆解 2
print(s)
((s + 2).cumprod() + 4).min()


# In[78]:


# 2018/1/1為60kg，2018/1/3吃太多，隔天起床變重5kg
weight = pd.Series(60, index=pd.date_range('2018-01-01', periods=10))
# 到這個序列最後一個值
weight.loc['2018-01-04':] += 5
weight
