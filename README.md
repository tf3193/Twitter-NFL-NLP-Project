# marist-NLP-Project
## Description
Can we find a correlation between how an NFL team is perceived and their win percentages during a game? We want to perform a sentiment analysis on each NFL team during a game and use statistitcs generated from ESPN as a real time win percentages to find correlations. Two end goals for this would be to figure out if we can predict the outcome of a game based on sentiment analysis throughout the game, and if we can predict a team's chance to win only by the fan perception. 
## Steps to Completion
- Scrape twitter for specific hashtag's to get live data
- Scrape ESPN or other sport stastical data. 
- Perform a sentiment analysis on the tweets. 
- Create a regression model using sentiment as a feature to predict outcomes and real time win chance. 
## Technologies of Interest
- Keras with TensorFlow back-end to create a sentiment model for tweets (potential dataset with over 1.5 million tweets categorized as positive or negative sentiment here: http://thinknook.com/twitter-sentiment-analysis-training-corpus-dataset-2012-09-22/)
- Tweepy, a Python library for accessing Twitter API. Of particular interst is the streaming API here: https://tweepy.readthedocs.io/en/latest/streaming_how_to.html
- nflscrapR library to grab statistical and win probability data for NFL games here: https://github.com/maksimhorowitz/nflscrapR
- rpy2 library as an option to call nflscrapR code (this is R source code) directly from python code here: https://rpy2.readthedocs.io/en/version_2.8.x/introduction.html
