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

