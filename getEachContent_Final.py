# this program is used to read links (gathered from the CoinDeskScraping_Final.py) to articles from CoinDesk and
# then save the content of each article in a seperate file

import pandas as pd
from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup
import re

# setting user agent so CoinDesk doesn't know it's a bot
def getsource(url):
    req=urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}) #sends GET request to URL
    uClient=urllib.request.urlopen(req)
    pageHtml=uClient.read() #reads returned data and puts it in a variable
    uClient.close() #close the connection
    pageSoup=BeautifulSoup(pageHtml,'lxml')
    return [pageSoup, pageHtml]

# function to get content from an article once you "click" on the link
def getArticleContent(articleLink):
    articleContentPageSoup = getsource(articleLink)[0]
    articleContent = ""
    for paras in articleContentPageSoup.find('div', {'class':'article-content-container noskimwords'}).findAll('p'):
        articleContent += paras.getText()
    return articleContent

# reading the CSV output for the CoinDeskScraping_Final.py script
# which returns information about article title, author, short description,
# data/time of publication, and the link to the article
csv=pd.read_csv('<insert path>')

# get the links to the articles from the file
hrefs=csv['link']

# for every article link, get the content and save it as a text file
for href in hrefs:
    articleContent=getArticleContent(href)
    filename = href.replace("https://www.coindesk.com/","")
    articleContentFileName = filename.replace("/","") + ".txt"
    file  = open(articleContentFileName,'w')
    file.write(articleContent)