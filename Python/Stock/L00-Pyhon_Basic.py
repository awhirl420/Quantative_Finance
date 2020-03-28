# Jupyter Notebook
# Ctrl + Enter
# Shift + Enter
# X: Cut
# V: Paste
# A: Insert Up
# B: Insert Below
# D + D
# M: Markdown
# Y: Code

# Variable Type
x = 5
type(x)
float(x)
str(x)
x1 = True

# Show dynamic lines
# 數字y要轉換成string
y = 10
print (str(y) + " Dollars")

# ", ' , /的使用
"I'm fine"
'I\'m fine'
print('Red' + ' car')
print ('Red', 'car')
print (3, 5)
print (3, 5, 6.9, 7.0, 'car')

# 兩數相除的商數
16//3

# 餘數
12%10

# retrive d
"Friday"[3]

# 縮徑
def five(x):
    x = 5
    return x

print (five(3))

10 != 15
5 is not 6

False or True
not False
True and not True
# not最重要、and比or優先
False or not True and True
True and not True or True

# 條件語句
if 5 == 15 / 3:
    print ("Hooray!")
  
def compare_to_five(y):
    if y > 5:
        return "Greater"
    elif y < 5:
        return "Less"
    else:
        return "Equal"

# 函數
def simple():
    print ("My first function")

def plus_ten(a):
    return a + 10

def plus_ten(a):
    result = a + 10
    print ("Outcome:")
    return result

# 函數中的函數
def wage(w_hours):
    return w_hours * 25

def with_bonus(w_hours):
    return wage(w_hours) + 50

# 函數內if
def add_10(m):
    if m >= 100:
        m = m + 10
        return m
    else:
        return "Save more!"
    

# max(), min(), abs(), sum()
max(10, 20, 30)

# 陣列加總
list_1 = [1,2,3,4]
sum(list_1)

# 四捨六入五成雙(若進位的數字是偶數，則不進位)
round(3.555,2)
round(2.3)
round(2.5)

# 次方
pow(2,10)
2 ** 10

# 字數
len('Mathematics')

# 亂數產生
import random
random.random()
random.randint(0, 99)

# 在範圍內，隨機產生2的倍數
random.randrange(0, 101, 2)

# 取得小於等於的最大整數
import math
math.floor(4.56)
math.floor(-3.44)

# 取得大於等於的最小整數
math.ceil(4.3)
math.ceil(-3.2)

# 開根號
math.sqrt(16)

# 函數
math.exp(2)
math.log(7)
math.sin(10)
math.cos(10)
math.tan(10)

# 列表 Lists
Participants = ['John', 'Leila', 'Gregory', 'Cate']
Participants

# 第一個
print (Participants[0])

# 最後一個
Participants[-1]

# 刪除特定一個
del Participants[2]

# 增加
Participants.append("Dwayne")
Participants

Participants.extend(['George', 'Catherine'])
Participants

# List是字串
print ('The first participant is ' + Participants[0] + '.')

# List內單位數目
len(Participants)

# slicing
Participants
# ['John', 'Leila', 'Maria', 'Dwayne', 'George', 'Catherine']
Participants[1:3]
# ['Leila', 'Maria']，不含最後一個
Participants[:2]
# ['John', 'Leila']
Participants[4:]
# ['George', 'Catherine']
Participants[-2]
# 'George'
Participants[-2:]
['George', 'Catherine']

Participants.index("George")

Newcomers = ['Joshua','Brittany']
Newcomers

#　將兩個列表放在一個列表中
Bigger_List = [Participants, Newcomers]
Bigger_List

#　排序
Participants.sort()
Participants.sort(reverse=True)

# Tuples(元組) are immutable.
(age, years_of_school) = "30,17".split(',')
print (age)
print (years_of_school)

# Dictionary
dict = {'k1': "cat", 'k2': "dog", 'k3' : "mouse", 'k4' : "fish"}
dict['k5'] = 'parrot'
dict

dict['k1']
dict["k3"]

dep_workers = {'dep_1':'Peter', 'dep_2':['Jennifer','Michael','Tommy']}
dep_workers['dep_2']

Team = {}
Team['Point Guard'] = 'Dirk'
Team['Shooting Guard'] = 'Al'
Team['Small Forward'] = 'Sean'
Team['Power Forward'] = 'Alexander'
Team['Center'] = 'Hector'

print (Team)
print (Team['Center'])
print (Team.get('Small Forward'))
print (Team.get('coach'))

x = [1, 2, 3]
x

# 變數移除
del x
x

# 顯示變數
dir()

# 顯示廣域變數
globals()

# 顯示區域變數
locals()

# tuple定義後，不允許更動內部值
x = (1, 2, 3)
x[2] = 4

# tuple

# 一行中定義多個變數
x, y = (1,2,3),(3,4,5)
x
y

# 2維
x = ((1,2),(3,4),(5,6))
x
x[0]
x[0][0]

# tuple計算
x=(1,2,3)
y=(7,8,9)
x+y
# (1, 2, 3, 7, 8, 9)
x*3
(1, 2, 3, 1, 2, 3, 1, 2, 3)

#由第一個值來比較
x>y
#False

3 in x
#True

# 可以直接用來迴圈計算
for i in x:
    print(i)
    
#tuple函數應用
#max(x), min(x)

#lsit函數應用
x = [45, 72, 65, 21, 87]
x

x.append(100)
x.count(5)
x.extend([44,45])
x.index(65)
x.remove(72)
x.reverse()
x.sort()
x.sort(reverse=True)
5 in x

sum=0
for i in x:
    sum+=i
    
sum

# dictionary
x = {'one':123, 'two':345, 'three':567}
x

x['one']

x[0]
# 錯誤

# list函數應用
len(x)
x.copy()

# 轉換成list
x.items()

# 取出所有key
x.keys()

x.clear()
x

# list comprehenion 列表推導式
# 讀取檔案、進行資料篩選
x=[1,2,3,4,5]
[i+1 for i in x]

[i**2 for i in x]

[i**2 for i in x if i!=3]

# 二維陣列
y = [[i, i**2] for i in x if i!=3]
y

# 取值
[i[0] for i in y]
