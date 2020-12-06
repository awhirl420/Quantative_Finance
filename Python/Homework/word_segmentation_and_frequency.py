import jieba
import json


ret = open("./speech.txt", "r").read().strip()
seglist = jieba.cut(ret, cut_all=False)

word_dict = {}
for item in seglist: 
    if item in word_dict:
        word_dict[item] += 1
    else:
        word_dict[item] = 1
        
print(word_dict)

with open("count.csv","w", encoding='utf-8-sig') as fd:
    fd.write("word,count\n")
    for k in word_dict:
        row = str(k)+','+str(word_dict[k])+'\n'
        fd.write(row)
        
        
        
%matplotlib inline
from wordcloud import WordCloud
import matplotlib.pyplot as plt 
ret = open("./speech.txt", "r").read().strip()
seglist = jieba.cut(ret, cut_all=False)
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
