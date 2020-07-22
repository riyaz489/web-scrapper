import requests
# its a light weight lib
# we can scrape data from one page and for another page we again have to send request and get html data and scrape it
from bs4 import BeautifulSoup
import collections

# BeautifulSoup library is build on the top of the HTML parsing libraries
# like html5lib, lxml, html.parser, etc.
# so first it will parse request raw html page(which came in string format) using the specified parser then
# it will do its searching


data = []
URL = 'https://push.oliveboard.in/assignment/urls.txt'
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib')
sd = soup.find('body')
subLinks = str(sd.next).split('\n')
for link in subLinks:
    if link == '':
        continue
    res = requests.get(link)
    soup = BeautifulSoup(res.content, 'html5lib')

    # get footer data
    w = soup.find('div', attrs={'id': 'footer'})
    if w:
        w = w.next
        data.extend(str(w).lower().split(' '))

    # getting footer data, while removing a tags data from it
    w = soup.find('div', attrs={'class': 'footer'})
    if w:
        for child in w.find_all("a"):
            child.decompose()
            temp = str(w.text).lower().split(' ')
            data.extend(temp)

    # getting only p tags while removing a tags from it
    qw = soup.find_all('p')
    for w in qw:
        if w.a:
            continue
        temp = str(w.text).lower().split(' ')
        data.extend(temp)

    # getting span tags, a tags and heading tags text
    a = soup.find_all(['a', 'span', 'h1', 'h2', 'h3'])
    for r in a:
        data.extend(str(r.text).lower().split(' '))


def remove_special_chars(v):
    if v == '' or v == '\n':
        return False
    return True


filtered_list = filter(remove_special_chars, data)
print(collections.Counter(filtered_list))
