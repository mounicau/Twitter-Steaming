# We used this program to connect to the Twitter API,
# pull live/streaming Tweets about specific hashtags,
# and put it in our Azure db

#import needed libraries
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import AzureDBConnection_Final as db #importing one of our other scripts to connect to DB
from textblob import TextBlob
import re

# each group member created a developer account with Twitter to pull data
# and ran the program for a different set of hashtags
# group members put in their credential information to connect to Twitter
access_token = '<insert credentials here>'
access_token_secret = '<insert credentials here>'
consumer_key = '<insert credentials here>'
consumer_secret = '<insert credentials here>'

# connect to the Azure Database by using the AzureDBConnection_Final.py
# script as a global script
db_connection, db_cursor = db.get_conn()

# included MSDA username as a column in our Azure DB
# so that we could keep track of who running the script
# for which keyword/hashtag
MSDAUSERNAME = "<insert username here>"

# this list determines what hashtags to pull from Twitter
# each group member had their own hashtags to pull
keywordsToFilterTwitter = ["ENTER KEYWORD HERE]
Keywords = ",".join(keywordsToFilterTwitter)

def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return '+'
    elif analysis.sentiment.polarity == 0:
        return '.'
    else:
        return '-'


def clean_tweet(tweet):
    # function to clean tweet text by removing links, special characters using regex statements
    cleanedTweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+)", " ", tweet).split())
    print("cleaned tweet", cleanedTweet)
    return cleanedTweet

def get_query():
    # function to give the SQL insert statement to put data from Twitter into our Azure DB
    return "insert into twitterData_modified (RecordID,MSDAUSERNAME,Keywords,CreatedAt,TweetID,TweetMessage,Source,UserID, " \
           "UserName,UserScreenName,location,UserFollowersCount,UserFriendsCount,UserListedCount,UserFavouritesCount," \
           "UserTweetsCount,AccountCreatedAt,Coordinates,Place,isRetweetedMessage,reTweetQuoteCount,reTweetReplyCount," \
           "reTweetcount,reTweetFavoriteCount,isReTweeted,isTweetFavorited,Polarity) values " \
           "(NEXT VALUE FOR Record_ID,?,?,?,?,?," \
           "?,?,?,?,?,?,?,?,?,?,?,?,?," \
           "?,?,?,?,?,?,?,?)"

class listener(StreamListener):
    # function to get and display the raw tweet, before we clean it or look at it's polarity
    def on_data(self, raw_data):
        def on_data(self, raw_data):
            print(raw_data)
       # loading in raw data as a JSON and getting the attributes we want from the raw Data
       # most important attributes for our analysis are id_str which is the unique id and
       # tweetText
       rawdataJSON = json.loads(raw_data)
       tweetText = rawdataJSON['text']
       created_at = rawdataJSON['created_at']
       id_str = rawdataJSON['id_str']
       text = rawdataJSON['text']
       source = rawdataJSON['source']
       userID = str(rawdataJSON['user']['id'])
       UserName = rawdataJSON['user']['name']
       UserScreenName = rawdataJSON['user']['screen_name']
       location = rawdataJSON['user']['location']
       UserFollowersCount= rawdataJSON['user']['followers_count']
       UserFriendsCount = rawdataJSON['user']['friends_count']
       UserListedCount = rawdataJSON['user']['listed_count']
       UserFavouritesCount = rawdataJSON['user']['favourites_count']
       UserTweetsCount = rawdataJSON['user']['statuses_count']
       AccountCreatedAt = rawdataJSON['user']['created_at']
       Geo = str(rawdataJSON['geo'])
       Coordinates = str(rawdataJSON['coordinates'])
       # doing null handling for the users who have more privacy settings on
       if Geo is None:
           Geo = 'NA'
       if Coordinates is None:
           Coordinates = 'NA'
       Place = str(rawdataJSON['place'])
       if Place is None:
           Place = 'NA'
       isRetweetedMessage = ''
       reTweetQuoteCount = 0
       reTweetReplyCount = 0
       reTweetcount = 0
       reTweetFavoriteCount = 0
       if rawdataJSON.get('retweeted_status') is None :
        isRetweetedMessage ='N'
       else:
        isRetweetedMessage = 'Y'
        reTweetQuoteCount = rawdataJSON['retweeted_status']['quote_count']
        reTweetReplyCount = rawdataJSON['retweeted_status']['reply_count']
        reTweetcount = rawdataJSON['retweeted_status']['retweet_count']
        reTweetFavoriteCount = rawdataJSON['retweeted_status']['favorite_count']

       isReTweeted = rawdataJSON['retweeted']
       isTweetFavorited = rawdataJSON['favorited']

       # calling query function to write the SQL insert statement
       query = get_query()
       polarity = get_tweet_sentiment(str(text))

       # args = what we are going to input into the DB
       args = (MSDAUSERNAME, Keywords, created_at, id_str, text, source, userID, UserName, UserScreenName,
               location, UserFollowersCount, UserFriendsCount,UserListedCount, UserFavouritesCount, UserTweetsCount, AccountCreatedAt, Coordinates, Place,
               isRetweetedMessage, reTweetQuoteCount, reTweetReplyCount,reTweetcount, reTweetFavoriteCount, str(isReTweeted), str(isTweetFavorited), polarity)
       print(args)
       #inserting data using the AzureDBConnection_Final.py as a global script
       db.insert_data(query,db_connection, db_cursor, args)

       # printing out to screen ("std out") so we can monitor the script
       # saving raw data to file to have a back up of data
       print("\n\n")
       saveFile = open('TwitterDB5.csv', 'a')
       saveFile.write(raw_data)
       saveFile.close()
       return True

   #displaying error code for troubleshooting
   def on_error(self, status_code):
       print(status_code)


# connecting to Twitter using the credentials above
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# using the functions and class created above to create a Twitter Steam
# and pull data about specific hashtags
twitterStream = Stream(auth, listener())
twitterStream.filter(track=keywordsToFilterTwitter)
