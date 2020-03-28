#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 定義變數
account = 100000
stock_price = 30
buy_amount = 1

fee_ratio = 1.425 / 1000
tax_ratio = 3 / 1000


# In[2]:


# 買股票，帳戶的錢變少
stock_value = stock_price * buy_amount * 1000
account = account - stock_value - stock_value * fee_ratio


# In[3]:


# 股價漲
stock_price = stock_price * 1.2


# In[4]:


# 賣股票，帳戶的錢變多
stock_value = stock_price * buy_amount * 1000
account = account + stock_value - stock_value * (fee_ratio + tax_ratio)

print(account)


# In[5]:


"""
回家作業：
  帳戶有100000元
  1. 買1張股價為35的股票
  2. 股價漲了30%
  3. 賣出
  請問帳戶現在有多少錢？
"""

account = 100000
stock_price = 35
buy_amount = 1

fee_ratio = 1.425 / 1000
tax_ratio = 3 / 1000

# 買股票
stock_value = stock_price * buy_amount * 1000
account = account - stock_value * (1 + fee_ratio)

# 股價漲
stock_price = stock_price * 1.3

# 賣股票
stock_value = stock_price * buy_amount * 1000
account = account + stock_value - stock_value * (fee_ratio + tax_ratio)

'答對了' if account == 110248.7875 else '當中有一些小錯誤，再檢查一下吧！'


# In[6]:


# 布林
a = stock_value <= account
print(a)


# In[7]:


a = False
print(a)


# In[8]:


a = 3 < 4
b = 3 < 2 < 0
c = 1 + 2 != 4

answers = [True, False, True]
'答對了' if [a, b, c] == answers else '當中有一些小錯誤，再檢查一下吧！'


# In[9]:


"""
字串
"""
s = 'hello world'
print(s)


# In[10]:


s = "hello world"
print(s)


# In[11]:


s = """hello world"""
print(s)


# In[12]:


s[0]


# In[13]:


s[-1]


# In[14]:


s.count('l')


# In[15]:


s.find('o')


# In[16]:


s + s


# In[19]:


# list
li = [1, 2, 3, 'i am string', True, False]
li[-1]


# In[21]:


# 序號4不會出現
li[1:4]


# In[22]:


li[2] = 4
li


# In[23]:


li.append(100)


# In[24]:


li


# In[25]:


"""
回家作業
型態：字串
計算以下題目，將手寫a跟b依序寫在第16行
雖然我們已經幫您把a跟b寫出來，在第16行，但似乎寫錯了，請糾正，讓程式跑出「答對了！」的字樣
"""

a = 'ABC' + 'DEF'
b = "HI"
b = b.replace('I', 'A')

"""
手寫出 a、b ，將答案依序寫在第16行，讓程式跑出「答對了！」的字樣
"""

answers = ['ABCDEF', 'HA']

'答對了' if [a, b] == answers else '當中有一些小錯誤，再檢查一下吧！'


# In[26]:


"""
回家功課
請閱讀以下的code，並修改第14、25、33、40行，讓四題都全對
"""

# 你前五個月的薪水，依時間順序，由遠到近為
income = [2, 2, 2, 3, 3]

# 最近五個月的花費為
outcome = [1.3, 2.4, 1.8, 1.9, 1.2]

"""
第一題
  最近你的薪水又下來了，因為認真工作，這個月變成4萬！如何修改income list呢？
"""
income.append(4)

"""
第二題
  這半年薪水平均為多少（用程式計算）
  請用sum()、跟len()完成！
""" 

average_income = sum(income) / len(income)

"""
第三題
  半年花費總共多少（用程式計算）
"""

total_outcome = sum(outcome)

"""
第四題
  這半年共累積多少資產？
"""
balance = sum(income) - sum(outcome)


# In[28]:


# dictionary
score = {'小民':90, '大雄':80}
score['KEVEN'] = 95
print(score)


# In[29]:


len(score)


# In[30]:


score.keys()


# In[31]:


score.values()


# In[32]:


position = {
    '1526': 2,
    '台泥': 1,
    '1102': 3,
    '2330': 2,
    '帳戶餘額+交割金額': 40000,
}

a = position['1526']
b = position['1102']


# In[33]:


"""
課堂練習：寫一個減法的函數，並使用看看
"""
def sub(x, y):
    ret = x - y
    return ret

a = 1
b = 3

sub(1,3)


# In[34]:


"""
設計一個函數，叫做calculate_earning
這個函數讀入買入價格、賣出價格、持有數量，並計算並返傳獲利。
（不用考慮手續費）
大家只需要修改以下第9行，讓程式跑出「答對了！」的字樣
"""

def calculate_earning(buy_price, sell_price, amount=1):
    ret = (sell_price * amount * 1000) - (buy_price * amount * 1000)
    return ret

value = calculate_earning(30, 40, 2)

"""
按下執行(Run)，檢查你有沒有答對！
以下的code用來檢查用的，可以忽略～
"""
'答對了！' if value == 20000 else '當中有一些小錯誤，再檢查一下吧！'


# In[35]:


"""
課堂練習：顯示現在幾點
"""
import datetime
datetime.datetime(1991,1,1)
datetime.datetime.now()


# In[36]:


"""
顯示究竟是否獲利?
"""

buy_price = 30
sell_price = 25

if sell_price > buy_price:
    print('ya! win')
elif sell_price == buy_price:
    print('even')
else:
    print('oh no! loss')


# In[37]:


"""
For 迴圈：分別印出1、2、3、4...、1000
"""

for i in [1,2,3,4]:
    print(i)


# In[39]:


# 不會印出4
for i in range(0, 4):
    print(i)


# In[40]:


i = 0
while i < 8:
    print(i)
    i = i + 1
