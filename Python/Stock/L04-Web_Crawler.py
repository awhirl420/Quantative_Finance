# requests
# if fail, use selenium

# HTML - Table: Pandas.read_html
# HTML - Element: beautifulsoap
# CSV - Pandas.read_csv
# JSON - Json.dumps

import requests
req = requests.get('http://www.wibibi.com/info.php?tid=116')

req.encoding = 'utf-8' # 'big5'; Traditional Chinese Unicode
req.text

# retrive table form the text and put it into DataFrame
## Step1: save as html
## Step2: use pandas to read html

# Save as html
f = open('text.html', 'w', encoding='utf-8') # write
f.write(req.text)
f.close()

# Translate into DataFrame
import pandas as pd
dfs = pd.read_html('text.html')

# No need to save html
from io import StringIO
dfs = pd.read_html(StringIO(req.text))

######## TW stock market data
## get data
import requests
response = requests.get('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=20200103&type=ALLBUT0999&_=1578128790352')
response.text[:1000]
## confirm data columns
lines = response.text.split('\n')
lines[100]
#for loop
newlines = []

for line in lines:
  if len(line.split('",')) == 17:
    newlines.append(line)

print('lines:'+ str(len(lines)))
print('newlines:'+ str(len(newlines)))

import pandas as pd
from io import StringIO
## Create dataframe
c = '\n'
s = c.join(newlines)
s = s.replace('=', '')
df = pd.read_csv(StringIO(s))
df.head()

# save as string
df = df.astype(str)

# delete ','
df = df.apply(lambda s: s.replace(',', ''))

## second method to delete ','
def func(s):
    return s.str.replace(',','')

df = df.apply(func)

# take 證券代號 as index
df = df.set_index('證券代號')

# translate from str into values
df = df.apply(lambda s: pd.to_numeric(s, errors='coerce')) # set error as NaN

# drop columns with all NaN
df.dropna(axis=1, how='all', inplace=True)
# axis=1, examine each column
# how='all', take all as the condition

## second method to drop columns with all NaN
df = df[df.columns[df.isnull().sum() != len(df)]]

df.head()

## calculate red bar
close_open = df['收盤價'] / df['開盤價']
close_open.head(5)

## select stock
df[close_open > 1.05]

# save csv
df.to_csv('daily_price.csv', encoding='utf_8_sig')

# read csv
df = pd.read_csv('daily_price.csv', index_col=['證券代號'])

df.head()

# save into sqllite3
import sqlite3
conn = sqlite3.connect('test.sqlite3')

df.to_sql('daily_price', conn, if_exists='replace')

# read dataset in the database
df = pd.read_sql('select * from daily_price', conn, index_col=['證券代號'])
df.head()


