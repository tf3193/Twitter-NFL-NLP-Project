import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
import json
from keras.preprocessing.text import Tokenizer, tokenizer_from_json
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model

class TwitterModel:

    def load_tokenizer(self, json_file):
        with open(json_file) as j:
            return tokenizer_from_json(json.load(j))

    def load_twitter_model(self, h5_file):
        return load_model(h5_file)

    def __init__(self, tokenizer_path, model_path):
        self.url_tok = re.compile(r'https?://\S+\b|www\.[^ ]+')
        self.mention_tok = re.compile(r'@\w+')
        self.neg_tok = re.compile(r"n't\b")
        self.tokenizer = self.load_tokenizer(tokenizer_path)
        self.model = self.load_twitter_model(model_path)

    def clean_tweet(self, tweet):

        cleaned = tweet.lower()
    
        # cleans up html encoding, ex. &amp; -> &
        cleaned = BeautifulSoup(tweet, 'lxml').get_text()

        try:
            cleaned = bytes(cleaned, encoding='latin_1').decode('utf-8-sig').replace(u"\ufffd", "?")
        except:
            cleaned = cleaned

        cleaned = self.neg_tok.sub(" not", cleaned)    
        cleaned = self.url_tok.sub('<URL>', cleaned)
        cleaned = self.mention_tok.sub('<USER>', cleaned)
        cleaned = re.sub("[^a-zA-Z<>:;\(\)]", " ", cleaned)

        return cleaned

    def clean_tweets_batch(self, tweets):
        return [self.clean_tweet(tweet) for tweet in tweets]

    def predict_with_threshold(self, probs, threshold):
        if threshold < 0.5:
            raise ValueError("Threshold must be 0.5 or greater")

        if threshold == 0.5:
            threshold == 0.50000000000000001

        total = 0
        positive = 0
        negative = 0

        length = len(probs)

        for i in range(0, length):
            if (probs[i] >= threshold):
                total = total + 1
                positive = positive + 1
    
            elif (probs[i] <= 1 - threshold):
                total = total + 1
                negative = negative + 1

        percent_positive = positive / total
        percent_ignored = ((length - total) / length)

        return [percent_positive, percent_ignored]

    def predict_tweets_batch(self, tweets, metric='weighted', threshold=0.5):
        added_tweet = False

        # Could only get model.predict_proba to work with length > 1
        if (len(tweets) == 1):
            tweets.append("Append tweet")
            added_tweet = True

        sequences = self.tokenizer.texts_to_sequences(self.clean_tweets_batch(tweets))
        
        # Our twitter model needs 250 here
        data = pad_sequences(sequences, maxlen=250)

        probs = self.model.predict_proba(data)

        if added_tweet:
            probs = probs[:-1]

        if metric == 'weighted':
            return [np.mean(probs, dtype=np.float64), 0.0]
        elif metric == 'category':
            return self.predict_with_threshold(probs, threshold)
        else:
            raise ValueError("Metric types are ['weighted', 'category']")
