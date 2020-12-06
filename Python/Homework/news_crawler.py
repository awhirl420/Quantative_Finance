import requests
from bs4 import BeautifulSoup
import re


new_list = []
url = 'https://money.udn.com/money/index'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

div_tag = soup.find('div', {'id':'tab1'})

soup2 = BeautifulSoup(str(div_tag), 'html.parser')
a_tags = soup2.find_all('a')

for i in a_tags:
    print('title: {}, link: {}'.format(i.text, 'https://money.udn.com'+i['href']))
    new_list.append('https://money.udn.com'+i['href'])
    
from time import sleep
import os
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

        
def save_news(url):
    
   
    response = requests.get(url)
    sleep(1)
    soup = BeautifulSoup(response.text, 'html.parser')
    new_title = soup.find_all('h2',{'id':'story_art_title'})
    
    save_path = './news/'+new_title[0].text.replace(':','')
    
    article_body = soup.find_all('div',{'id':'article_body'})
    print('new title: {}'.format(new_title[0].text))

    ## create folder
    createFolder(save_path)
    soup2 = BeautifulSoup(str(article_body[0]), 'html.parser')


    ## save article contens in folder
    with open(save_path+'/contents.txt', 'w', encoding='utf-8') as f:  
        p_tags = soup2.find_all('p')
        print('new content: ')
        for i in p_tags:
            print(i.text)
            f.write(i.text)

    ## save image in article        
    img_tags = soup2.find_all('img')
    print('save image: ')
    for i in img_tags:
        print(i['src'])
        urlretrieve(i['src'], save_path+'/'+i['title']+'.jpg')
    print('==========\n\n')
    

for new_url in new_list:
    save_news(new_url)    
