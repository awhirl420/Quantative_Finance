# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.ptt.cc/bbs/movie/M.1586525586.A.891.html'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

div_tag = soup.find('div', {'id':'main-content'})

date_string = soup.find_all('span', {'class': 'article-meta-value'})[-1].text

result = str(div_tag).split('※ 發信站: 批踢踢實業坊(ptt.cc)')[0].split(date_string)[-1].replace('--','')


cleanr = re.compile('<.*?>')
clean_text = re.sub(cleanr, '', result)

print(clean_text)

%matplotlib inline
from wordcloud import WordCloud
import jieba
import matplotlib.pyplot as plt 

seglist = jieba.cut(clean_text, cut_all=False)
text = ''
for i in seglist:
    text = text + ' '+ i

wordcloud = WordCloud(font_path='simhei.ttf', width = 800, height = 800, 
                background_color ='white', min_font_size = 10).generate(text) 
  
# plot the WordCloud image                        
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show() 
