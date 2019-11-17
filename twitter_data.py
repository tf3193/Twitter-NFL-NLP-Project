import tweepy

####input your credentials here
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

#Running through authenticating and creating the api object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=False)
#Chose to use utf-32 to avoid any potential loss of emoji(They might be usefull for sentiment)
txtFile = open('nfl.txt', 'a', encoding='utf-32')


'''
This seemed a little wonky, the doc is here
https://tweepy.readthedocs.io/en/latest/cursor_tutorial.html

'''
for tweet in tweepy.Cursor(api.search,q="#BUFvsMIA",count=5,
                           lang="en",
                           since="2019-11-16").items():
    print (tweet.text)
    txtFile.write(tweet.text)