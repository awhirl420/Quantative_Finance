# 取用檔案
file = open('123.txt','w+')
file.name
# 查詢是否關閉使用
file.closed
file.mode

# 關閉取用檔案
file.close()
file.name
file.closed

# 覆蓋寫入檔案
file = open('123.txt', 'w+')
file.write("123456789/n")
file.close()

# 讀取檔案
file = open('123.txt', 'r')
file.read()

# 讀取檔案第一行
open('text.txt').readline()

# 讀取檔案所有行，並存成list
open('text.txt').readlines()

# 修改檔案名稱
import os
os.rename('123.txt', '456.txt')

# remove
os.remove('456.txt')

# 字串長度
str = "i am a pig"
len(str)

# 將元素透過特定符號組合
seq="    "
cc=('1','2','3','4')
seq.join(cc)

# 將特定字元從字首字尾中移除
str.strip()
str.strip("i")
str.strip("ig")

# 將特定字元從字首中移除
str = "i am a pig"
str.lstrip("i")
str.lstrip("ig")

# 將特定字元從字尾中移除
str = "i am a pig"
str.rstrip("i")
str.rstrip("ig")

# 轉換大小寫
str = "I am a pig"
str.swapcase()
str.lower()
str.upper()

# 字串中最大值、最小值
max(str)
min(str)

# 將字串透過0填滿至特定寬度
str='TTT'
str.zfill(15)

# 將字串中特定字元取代
str='HJODBJHEYHWKKE'
str.replace('H', " ")

# 將字串依照特定符號進行分割
str="111,333,532,7456,234,122"
str.split(',')

# 安裝套件
pip install pymysql
import pymysql

# Tick時間格式
import time
# 從1970/1/1 00:00至當前的秒數
ticks = time.time()
ticks

time.ctime(ticks)

# TimeTuple時間格式
# 年(4位數)、月、日、時、分、秒、日(周)、日(年)、是否採用DST(日光節約時間)
t = (2009, 2, 17, 17, 3, 38, 1, 48, 0)
t = time.mktime(t)
t

time.gmtime(t)

# 字串轉時間
time.strptime("09:30:20","%H:%M:%S")
time.strptime("2017/09/30 09:30:20","%Y/%m/%d %H:%M:%S")

# 將timetuple轉換成秒數
time.mktime(time.strptime("2017/09/30 09:30:20","%Y/%m/%d %H:%M:%S"))

# 沒有指定日期，沒辦法轉換成tick時間格式
time.mktime(time.strptime("09:30:20","%H:%M:%S"))

# time套件函數
# 取得當前時間秒數
import time
start=time.time()
time.time()-start

# 取得當前時間tuple
import time
time.localtime()
time.localtime()[1]

# 秒數轉為字串
import time
time.ctime()
time0=time.time()
time.ctime(time0)

# tuple轉換成秒數
import time
t = (2017, 2, 17, 17, 3, 38, 1, 48,0)
time.mktime(t)
time.mktime(time.localtime())

# 秒數轉換成tuple
import time
time.gmtime(time.time())

# 練習
t = (2017, 2, 17, 17, 3, 38, 1, 48, 0)
time.mktime(t)
time.gmtime(time.mktime(t))

# 將tuple轉換成特定格式字串
import time
time0 = (2017, 2, 17, 17, 3, 38, 1 ,48, 0)
time0 = time.mktime(time0)
print(time.strftime("%b-%d-%Y %H:%M:%S", time.gmtime(time0)))

# 轉換字串至時間物件
import time
time.strptime("12:30:25","%H:%M:%S")

# 秒數延遲
import time
time.time()
time.sleep(3)
time.time()

# datatime套件函數
import datetime
datetime.datetime.strptime("12:30:30.431234", "%H:%M:%S.%f")

# timedelta 日、秒
x = datetime.datetime.strptime("12:30:30.430000", "%H:%M:%S.%f")
x
x + datetime.timedelta(0,1)
x - datetime.timedelta(0,1)

# 資料的取用
x = [1,2,3,4,5,6,7,8,9]
x[:-2]
# [1, 2, 3, 4, 5, 6, 7]
x[-2:]
# [8, 9]

#取得2的倍數索引的值
x[::2]
# [1, 3, 5, 7, 9]

#透過迴圈簡易切割資料
[i for i in x if i>5]

# 邏輯判斷式
# 等於、不等於
x = 10
y = 9
x == y
x != y

x == 9 and y == 9

# 條件判斷式
if x==10:
    x+=10
else:
    x-=10

# for loop - practice 1
for i in 1,2,3,4 :
    print ("No.", i)
    
# for loop - practice 2
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for i in x:
    print("No.", i)
    
# for loop - practice 3
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for i in x[::2]:
    print("No.", i)
    
# for loop - practice 4
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

for i in x:
    y+=i
    print(y)
    
# for loop - practice 5
# 當i=7時，略過該循環

y = 0

for i in x:
    if i == 7:
        continue
    y+=i
    print(y)

# while loop - practice 1
x = 0
while x <= 7:
    print(x)
    x+=1
    
# while loop - practice 2
# 無窮迴圈的簡單寫法
x = 0
while 1:
    print(x)
    x+=1
    
# while loop - practice 3
x = 1
y = 0

while x <= 10:
    y+=x
    x+=1

y

# while loop - practice 4
# 用break, continue來強制改變while的循環型態
# pass並沒有實際的作用，都是用來編寫空的迴圈主體
x = 0
while x < 10:
    x+=1
    if x==5:
        continue
    print(x)
    

def cumsum(x):
    y=[]
    sum=0
    for i in x:
        sum+=i
        y.append(sum)
    return y

# file name: function.py
def cumsum(x):
    y=[]
    sum=0
    for i in x:
        sum+=i
        y.append(sum)
    return y

# import function.py
import function
function.cumsum([1, 2, 3, 4, 5, 6, 7, 8])

# 載入特定函數
from function import cumsum
cumsum([1,2,3,4,5,6,7,8])
