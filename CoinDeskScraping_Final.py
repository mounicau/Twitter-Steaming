# this program scrapes CoinDesk and gets metadata about cryptocurrency articles
# that metadata will be used for analysis and to get the full article text using
# another script, getEachContent_Final.py

import urllib.parse
from bs4 import BeautifulSoup

#set user agent so CoinDesk doesn't know we're a bot
def getsource(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'})  # sends GET request to URL
    uClient = urllib.request.urlopen(req)
    pageHtml = uClient.read()  # reads returned data and puts it in a variable
    uClient.close()  # close the connection
    pageSoup = BeautifulSoup(pageHtml, 'lxml')
    return [pageSoup, pageHtml]

#function to get the link, title, publication time, description, and author of an article on CoinDesk
def getArticleInfo(coinDeskScrapeSoup):
    articleDetails = []
    for content in coinDeskScrapeSoup.findAll('div', {'id': 'content'}):
        for postDiv in content.findAll('div', {'class': 'post-info'}):
            href = postDiv.a.get('href')
            title = postDiv.a.get('title')
            time = postDiv.find('p', {'class': 'timeauthor'}).time.getText()
            desc = postDiv.find('p', {'class': 'desc'}).getText()
            cite = postDiv.find('p', {'class': 'timeauthor'}).cite.getText().strip()
            myList = [href, title, time, desc, cite]
            articleDetails = articleDetails + myList
    return articleDetails


# function to find the last page number (last page is denoted by » on the website).
# this will let us loop through each page and get the article metadata
def getLastPageNumber(coinDeskScrapeSoup):
    for page in coinDeskScrapeSoup.findAll('div', {'class': 'pagination'}):
        for anchors in page.findAll('a'):
            if (anchors.getText() == '»'):
                lastPage = anchors.get('href')
                # pagination looks like page/<page number>/?
                # startIndex strips off the beginning until the page number
                startIndex = lastPage.index('page/') + 5
                # endEndex strips off everything after the page number
                endIndex = lastPage.index('/?')
                lastPageNumber = lastPage[startIndex:endIndex]
    return lastPageNumber

# https://www.coindesk.com/?s=bitcoin
baseURL = r'https://www.coindesk.com/'
searchQuery = '?s='
term = "<search term you want articles for>"

url = baseURL + searchQuery + urllib.parse.quote_plus(term)
sourceDetails = getsource(url)  # gets the whole source code
pageHtmlCode = sourceDetails[1] # html code
coinDeskScrapeSoup = sourceDetails[0] #soupified code

firstPage = 1
lastPage = int(getLastPageNumber(coinDeskScrapeSoup))

# loop through every page and get the article metadata
for pageNumber in range(firstPage, lastPage + 1):
    articlePageUrl = baseURL + 'page/' + str(pageNumber) + '/' + searchQuery + urllib.parse.quote_plus(term)
    eachPageSoup = getsource(articlePageUrl)[0]
    eachPageArticleInfo = getArticleInfo(eachPageSoup)
    print(eachPageArticleInfo)
