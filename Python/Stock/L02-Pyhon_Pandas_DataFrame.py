#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd

date = pd.date_range('20180101', periods=6)

# 建立一組時間序列
s1 = pd.Series([1,2,3,4,5,6], index=date)
s2 = pd.Series([5,6,7,8,9,10], index=date)
s3 = pd.Series([11,12,5,7,8,2], index=date)

dictionary = {
    'c1': s1,
    'c2': s2,
    'c3': s3,
}

df = pd.DataFrame(dictionary)
df


# In[12]:


get_ipython().run_line_magic('matplotlib', 'inline')
df.plot()


# In[13]:


# 選取
# 取出後成為一條Series
df.loc['2018-01-02']


# In[14]:


df.iloc[1]


# In[15]:


# 二維表格選取
df.loc['2018-01-02':'2018-01-05', ['c1', 'c2']]


# In[16]:


df.iloc[1:4, [0,1]]


# In[17]:


df.cumsum()


# In[18]:


df.cumprod()


# In[19]:


df.rolling(2).mean()


# In[20]:


df['c1']


# In[23]:


# 由上往下運算
print(df)
df.cumsum(axis=0)


# In[24]:


# 由左到右運算
print(df)
df.cumsum(axis=1)


# In[32]:


df.drop('c1', axis=1)

