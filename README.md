# Twitter-Steaming
In collaboration with Biljana Jovanova, Ashok Haralekere Motaiah, Ozan Aydin, Jacob Reyes, Sercan Demir, Rajesh Chodavarapu, and Nick Olivier

# Introduction
The main purpose of this project is to analyze Twitter “tweets” on a specific topic and see the user overall opinion by calculating the polarity of the tweets. For this project we used Python to get data from Twitter’s API, scrape a website for news article content, analyze polarity with NLTK, and store data in an Azure SQL DB. We then created a simple dashboard that would dynamically show the polarity of data we are gathering.

The topic we chose to analyze is cryptocurrency.

# Database Design
We configured a Microsoft Azure version of an MSSQL database. It contains two tables, one to hold the Tweets and their corresponding information and then one to hold information about cryptocurrency tickers/keywords that we webscraped from CoinDesk. It was important to create a system sequence that could be incremented so that we would not be overriding data when writing to the tables.

# Project Breakdown
Our first step was to find a place to store large amounts of data and could be access by multiple group members at the same time. We decided to utilize MSSQL in Azure. After designing the tables and database, we created a connection file (AzureDBConnection_Final.py) in python that could be accessed by our other python scripts.

getEachContent_Final.py uses BeautifulSoup to scrape the article links on CoinDesk (a news organization that focuses solely on crypocurrency news) and saves it to a file. CoinDeskScraping_Final.py loops through the file and scrapes the text and titles of the article. This information is saved in Azure and is used to get a rough estimate of what keywords to search for in Twitter.

TwitterStreaming_Final.py uses the Twitter API to pull streaming data that had specific hashtags that are specified in the script. We decided to pull steaming data instead of historical because the API limits the number of records you can pull back if going back in time. This code can be used to pull any type of data from Twitter, but for the purposes of this project, we only pulled crypto keywords. These tweers and additional information is stored in the Azure database. The tweets pulled from the API are truncated at 140 characters. These 140 characters included information such as URLs and @<other username>, not just tweet text. TwitterScraping_Final.py uses the tweet ID pulled from the API to find the tweet on Twitter.com and use BeautifulSoup to scrape the text of the tweer. This information is then updated in the database. We then created a near real time Tableau dashboard that is connected to the Azure database that looks at volumes of tweets and overall polarity.
