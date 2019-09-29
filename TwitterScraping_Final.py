# after we used the Twitter API to get data, we noticed that a lot of the tweets we pulled
# from the API were truncated... The API only showed us 140 characters of a Tweet. Unfortunately
# this included any URLs or @<other user> as a part of the character limit on what we can pull, but
# not what users can type into Twitter --> Our solution was to use the tweet ID we were getting from
# the API to find the Tweet on the website and scrape the actual Twitter site to get the full text of
# the tweet

import urllib.parse
from bs4 import BeautifulSoup
import AzureDBConnection_Final as db # importing one of our other scripts to connect to the Azure DB

# set user agent so Twitter doesn't know we're a bot
def getsource(url):
    req=urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}) #sends GET request to URL
    uClient=urllib.request.urlopen(req)
    pageHtml=uClient.read() #reads returned data and puts it in a variable
    uClient.close() #close the connection
    pageSoup=BeautifulSoup(pageHtml,'html.parser')
    return [pageSoup, pageHtml]

# when looking at Twitter, we found that the URL of any tweet had the structure of:
# base url (twitter.com)/ some search term (doesn't matter what it is)/ and tweet id

# function to get the tweet id from the Azure DB
def getTweetIdText(userName):
    selectQuery = "select distinct tweetid as statusID, TWEETMESSAGE from twitterData_modified where MSDAUSERNAME = '" + userName +"'"
    print(selectQuery)
    statusIDs = []
    tweetMessages = []
    try:
        db_cursor.execute(selectQuery)
        row = db_cursor.fetchone()
        while row:
            statusIDs += [str(row[0])]
            tweetMessages += [str(row[1])]
            row = db_cursor.fetchone()
    except Exception as exception:
        print("Error Occured", exception)
    return statusIDs, tweetMessages

# function to get the full Tweet text from Twitter and update the corresponding row in the Azure DB
def getFullTweetText(url):
    fullTweetMessage = ""
    try:
        sourceDetails = getsource(url)
        twitterSoup = sourceDetails[0]

        twitterTextContainer = twitterSoup.find('div',{'class':'permalink-inner permalink-tweet-container'})
        if twitterTextContainer is not None:
            twitterText = twitterTextContainer.find('div',{'class':'js-tweet-text-container'})
            if twitterText is not None:
                fullTweetMessage = twitterText.getText()
    except Exception as exception:
        print("Error Occured in getFullTweetText method. The error message is : ", exception)
    print(url)

    return fullTweetMessage

url = r'https://twitter.com/abc/status/'
userName  = '<insert MSDA username>'

#calling AzureDBConnection_Final.py to connect to DB
db_connection, db_cursor = db.get_conn()

statusIDs, tweetMessages = getTweetIdText(userName)
fullTweetTexts = []
try:
    for statusID in statusIDs:
        fullTweetText = str(getFullTweetText(url+statusID)).strip()
        fullTweetTexts += [fullTweetText]
        print(fullTweetText)
        if fullTweetText is not None and len(fullTweetText) > 0:
            print("--- Updating ---")
            updateQuery = "update  twitterData_modified set tweetMessage = ? where MSDAUSERNAME = ? and tweetid = ?"
            db_cursor.execute(updateQuery, fullTweetText, userName, statusID)
            db_connection.commit()
        else:
            print("Message Not Found")

except Exception as exception:
    print("The general error occured, the exception message is : ", exception)

finally :
    #close the db connection if any exception occurs.
    print("Closing the connection")
    db_cursor.close()
    db_connection.close()
    print("Closed the connection")