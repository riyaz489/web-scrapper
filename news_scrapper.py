import requests
from bs4 import BeautifulSoup
from dateutil import parser
import datetime
import csv
import os


filename = 'news.csv'
file_exists = os.path.isfile(filename)
data = []
URL = 'https://indianexpress.com/section/technology/'
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib')
flag = 1
counter = 0
while flag:
    top_news = soup.find('div',  attrs={'class': 'top-article'})
    next_page_url = top_news.find('a', attrs={'class': 'next page-numbers'})['href']
    article_list = top_news.find('ul', attrs={'class': 'article-list'})
    for row in article_list.find_all('li'):
        # data is not sorted by date. so if we get more than 15 news of 6 months older date then
        # we will stop fetching data
        if counter > 15:
            flag = 0
            break
        news = {}
        news['link'] = row.h3.a['href']
        news['headline'] = row.h3.a.text
        # requesting to news url for more info
        req = requests.get(news['link'])
        news_soup = BeautifulSoup(req.content, 'html5lib')
        news['date'] = news_soup.find('span', attrs={'itemprop': 'dateModified'})['content']
        news['date'] = parser.parse(news['date'])
        if (datetime.date.today()-news['date'].date()).days >= 180:
            counter += 1
        news_article = news_soup.find('div', attrs={'itemprop': 'articleBody', 'class': 'full-details'})
        news['description'] = ''
        for news_para in news_article.find_all('p'):
            news['description'] += news_para.text
        # adding data to list
        data.append(news)

    # appending data to csv
    with open(filename, 'a') as f:
        w = csv.DictWriter(f, delimiter=',', lineterminator='\n', fieldnames=['link', 'headline', 'date', 'description'])
        if not file_exists:
            w.writeheader()
        for row in data:
            w.writerow(row)

    # calling next page
    r = requests.get(next_page_url)
    soup = BeautifulSoup(r.content, 'html5lib')
