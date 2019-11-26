import tweepy
import pandas as pd
import os
teamsDF = pd.read_csv('teams.csv')

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
"""
'''
This seemed a little wonky, the doc is here
https://tweepy.readthedocs.io/en/latest/cursor_tutorial.html

'''
for tweet in tweepy.Cursor(api.search,q="#BUFvsMIA",count=5,
                           lang="en",
                           since="2019-11-16").items():
    print (tweet.text)
    txtFile.write(tweet.text)
"""


def get__hashtags_for_game(match):
    """
    Takes in a match such as "CARvsMIA" and returns hashtag values for home and away teams
    :param match:
    :return: hashtags for home and away cities and teams.
    """
    away, home = match.split('vs')
    away_hashtags = []
    home_hashtags = []
    away_hashtags.append('#' + teamsDF[teamsDF.short == away]['Team'].item())
    away_hashtags.append('#' + teamsDF[teamsDF.short == away]['CITY'].item())
    away_hashtags.append('#' + teamsDF[teamsDF.short == away]['hash'].item())
    home_hashtags.append('#' + teamsDF[teamsDF.short == home]['Team'].item())
    home_hashtags.append('#' + teamsDF[teamsDF.short == home]['CITY'].item())
    home_hashtags.append('#' + teamsDF[teamsDF.short == home]['hash'].item())

    return away_hashtags, home_hashtags


def get_games(file_name):
    """
    get all of the games hashtags from a csv of home and away games.
    :param file_name: path to a csv file with the list of games
    :return: a list of game hashtags
    """
    gameDF = pd.read_csv(file_name)
    game_list = []
    for index, row in gameDF.iterrows():
        #print(row)
        game_list.append("#" + (row['Home'] + 'vs' + row['Away']))
    return game_list


def scrape_twitter_for_game(game, file_name):
    """

    :param game:
    :return:
    """
    line_break = '-------------------------------------------------------------------------------\n'
    homeFile = open('data/' + file_name + '/home', 'w', encoding='utf-32')
    awayFile = open('data/' + file_name + '/away', 'w', encoding='utf-32')
    bothReferencedFile = open('data/' + file_name + '/bothReferenced', 'w', encoding='utf-32')
    everythingelseFile = open('data/' + file_name + '/everythingElse', 'w', encoding='utf-32')
    skipFile = open('data/' + file_name + '/skipped', 'w', encoding='utf-32')

    skip_words = ['recap', 'pts', 'rebs', 'blk', 'asts']
    for tweet in tweepy.Cursor(api.search, q=game, count=100,
                               lang="en",
                               since="2019-11-16",
                               tweet_mode='extended').items():
        tweet_text = tweet.full_text
        #Replace commans, colons and new lines with spaces
        tweet_text = tweet_text.replace(',', ' ')
        tweet_text = tweet_text.replace('\n', ' ')
        tweet_text = tweet_text.replace(':', ' ')
        tweet_text = tweet_text.lower()
        print(tweet_text)


        #remove the # symbol for the game hashtag
        away, home = get__hashtags_for_game(game[1:])
        #check if tweet has a skip word
        if not any(word.lower() in tweet_text for word in skip_words):
            if any(hashtag.lower() in tweet_text for hashtag in away) and any(hashtag.lower() in tweet_text for hashtag in home):
                bothReferencedFile.write(str(tweet.created_at) + ":" + tweet_text + ",")
            elif any(hashtag.lower() in tweet_text for hashtag in away):
                awayFile.write(str(tweet.created_at) + ":" + tweet_text + ",")
            elif any(hashtag.lower() in tweet_text for hashtag in home):
                homeFile.write(str(tweet.created_at) + ":" + tweet_text + ",")
            else:
                everythingelseFile.write(str(tweet.created_at) + ":" + tweet_text + ",")
        else:
            skipFile.write(str(tweet.created_at) + ":" + tweet_text + ",")

"""games = get_games('gamesNOV17.csv')
date = 'gamesNOV17'
for game in games:
    scrape_twitter_for_game(game, date + '/' + str(game))
print(games)
"""
games = get_games('gamesNOV24.csv')
date = 'gamesNOV24'
for game in games:
    scrape_twitter_for_game(game, date + '/' + str(game))




