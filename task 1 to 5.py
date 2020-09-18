
#edited from the code given in workshop4 Web crawling part, which is originaly used to
#crawling 'http://books.toscrape.com/'. and natural language processing part
#and workshop2 graph-making

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import unicodedata
import re
import matplotlib.pyplot as plt
import csv
import json
import nltk
from nltk.stem.porter import *
import matplotlib.pyplot as plt
import calendar
from numpy import arange
import numpy as np




base_url = 'http://comp20008-jh.eng.unimelb.edu.au:9889/main/'
seed_item = 'index.html'

seed_url = base_url + seed_item
page = requests.get(seed_url)
soup = BeautifulSoup(page.text, 'html.parser')

visited = {};
visited[seed_url] = True

links = soup.findAll('a')
seed_link = soup.findAll('a', href=re.compile("^index.html"))
to_visit_relative = [l for l in links if l not in seed_link]

to_visit = []
for link in to_visit_relative:
    to_visit.append(urljoin(seed_url, link['href']))

while (to_visit):
    link = to_visit.pop(0)
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    visited[link] = True
    to_visit
    new_links = soup.findAll('a')
    for new_link in new_links :
        new_item = new_link['href']
        new_url = urljoin(link, new_item)
        if new_url not in visited and new_url not in to_visit:
            to_visit.append(new_url)

with open('task1.csv', 'a', newline = '') as f:
    addtool = csv.writer(f)
    addtool.writerow(['url', 'headline'])
    for key in visited.keys():
        if key != "http://comp20008-jh.eng.unimelb.edu.au:9889/main/index.html":
            contain = requests.get(key)
            soup = BeautifulSoup(contain.text, 'html.parser')
            t = soup.findAll('h1')
            ti = re.compile(r'<[^>]+>',re.S)
            tit = ''.join(t[0])
            title = ti.sub('',tit)
            addtool.writerow([key, title])

f.close()

#above for task1

nltk.download('punkt')
nltk.download('stopwords')
porterStemmer = PorterStemmer()

player = ''
flag_n = 0
flag_r = 0
score = ''
namelist = []

with open('tennis.json') as t:
    infor = json.load(t)
t.close()
for i in range(644):
    namelist.append(' ' + infor[i]['name'] + ' ')
with open('task2.csv', 'a', newline = '') as f:
    addtool = csv.writer(f)
    addtool.writerow(['url', 'headline','player','score'])
    for key1 in visited.keys():
        if key1 != "http://comp20008-jh.eng.unimelb.edu.au:9889/main/index.html":
            contain = requests.get(key1)
            soup = BeautifulSoup(contain.text, 'html.parser')
            t = soup.findAll('h1')
            ti = re.compile(r'<[^>]+>',re.S)
            tit = ''.join(t[0])
            title = ti.sub('',tit)
            contain = requests.get(key1)
            soup = BeautifulSoup(contain.text, 'html.parser')
            a = soup.findAll('p')
            art = []
            length = len(a)
            for i in range(length-2):
                temp = ''.join(a[i])
                art.append(temp)
            art_t = ''.join(art)

            wordList = nltk.word_tokenize(art_t)
            from nltk.corpus import stopwords
            stopWords = set(stopwords.words('english'))

            filteredList = [w for w in wordList if not w in stopWords]


            le = len(filteredList)
            for i in range(0,le):
                for j in range(len(namelist)):
                    if (' ' + filteredList[i].upper() + ' ') in namelist[j]:
                        if (' ' + filteredList[i+1].upper() + ' ')in namelist[j]:
                            player = namelist[j]
                            flag_n = 1
                            break
                if flag_n ==1:
                    break

            pattern4 = re.compile(r"( \d{1,2}-\d{1,2}( \(\d{1,2}-\d{1,2}\))?){2,5}")
            result = pattern4.search(art_t)
            if result == None:
                flag_r =0
            else:
                flag_r =1
                score = result.group()
                #print(score)
            if flag_n ==1 and flag_r ==1:
                addtool.writerow([key1, title, player, score])
                flag_n = 0
                flag_r = 0
            score = ''
f.close()

#above for task2

dict = {}

with open('task2.csv', 'r',newline = '') as r:
    reader = csv.DictReader(r)
    for row in reader:
        if row['player'] in dict.keys():
            dict[row['player']].append(row['score'])
        else:
            dict[row['player']] = []
            dict[row['player']].append(row['score'])
r.close

dict_s={}
temp_list = []
pattern = re.compile(r'( \d{1,2}[/-]\d{1,2})')
ave = 0
sum = 0

for key in dict.keys():
    for record in dict[key]:
        result = pattern.findall(' '+record)
        ll = len(result)
        score = 0
        for j in range(ll):
            if result[j][2].isdigit():
                if result[j][3] != '-':
                    result[j][3] = '-'
            else:
                if result[j][2] != '-':
                    result[j][2] = '-'
            score = score + eval(result[j])
        temp_list.append(abs(score))
    l = len(temp_list)
    for i in range(l):
        sum = sum + temp_list[i]
    ave = sum/l
    dict_s[key] = ave
    ave = 0
    sum = 0
    temp_list = []




with open('task3.csv', 'a', newline = '') as f:
    addtool = csv.writer(f)
    addtool.writerow(['player','avg_game_difference'])
    player0 = ''
    ave = 0
    for key in dict_s.keys():
        player0 = key
        ave = dict_s[key]
        addtool.writerow([player0, ave])


f.close()

#above for task 3

dict_c = {}
lenr  = 0

temp_list = []
tool = [-1,-1]


for key in dict.keys():
    lenr = len(dict[key])
    dict_c[key] = lenr

for item in dict_c.items():
    tool[0] = item[1]
    tool[1] = item[0]
    temp_list.append(tool)
    tool = [-1, -1]

temp_list.sort(reverse=True)



topplayer = []
visitfrequency = []

for i in range(5):
    topplayer.append(temp_list[i][1])
    visitfrequency.append(temp_list[i][0])


plt.bar(arange(len(visitfrequency)),visitfrequency)
plt.xticks( arange(len(topplayer)),topplayer, rotation=15)
plt.savefig('task4.png')
#above for task4

plt.cla()

with open('tennis.json') as t:
    infor = json.load(t)
t.close()

validplayer=[]

for key in dict_s.keys():
    validplayer.append(key)

wonpact_dict = {}
for i in range(644):
    if (' ' + infor[i]['name'] + ' ') in validplayer:
        wonpact_dict[' ' + infor[i]['name'] + ' '] = infor[i]['wonPct']

xlist = []
ylist = []
for key in dict_s.keys():
    xlist.append(wonpact_dict[key])
    ylist.append(dict_s[key])

area = np.pi*4

plt.scatter(xlist, ylist, s=area, color = 'red')
plt.title('AVE VS. WINPCT')
plt.ylabel("average game difference")
plt.xlabel("wing percentage")
plt.savefig('task5.png')

#above for task5
