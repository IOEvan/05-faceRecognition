# -*- coding: utf-8 -*-
import urllib.request
import bs4
from bs4 import BeautifulSoup
import codecs

def getHTMLText(url):  # 获取网页内容
    try:
        res = urllib.request.urlopen(url)
        html = res.read().decode('utf-8')
        return html
    except:
        return ''


def fillUnivList(ulist, html):  # 解析网页内容，并提取相关信息
    soup = BeautifulSoup(html, 'html.parser')
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag):
            # tds = tr('td')
            tds = tr('p')
            ulist.append([tds[0].string])


def printUnivList(ulist, num):
    res = codecs.open('data.txt', 'w', encoding='utf-8')  # 指定txt编码为utf-8
    for i in range(num):
        u = ulist[i]
        res.write(str(u[0]) + '\n')


def main():
    uinfo = []
    url = 'https://baike.baidu.com/starrank'  # 爬取的网页
    html = getHTMLText(url)
    fillUnivList(uinfo, html)
    printUnivList(uinfo, 20)


main()


