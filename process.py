import sys
import re
import json
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

def main():

    raw_tweets = open(sys.argv[1])
    processed_tweets = process(raw_tweets)
    processed_tweets = [tweet for tweet in processed_tweets if tweet != []]
    tfidf = TfidfVectorizer(tokenizer=lambda i:i, lowercase=False)
    tfs = tfidf.fit_transform(processed_tweets)

    print(tfs)

    #for tweet in processed_tweets:
    #    print (tweet)

def process(raw_tweets):
    tweets = []
    # open file of tweets to parse
    for line in raw_tweets:
        try:
            tweets.append(json.loads(line))
        except:
            continue

    # remove non-ascii tweets in order to get mostly english text
    tweet_texts = []
    for tweet in tweets:
        if 'text' in tweet:
            try:
                tweet['text'].encode('ascii')
            except UnicodeEncodeError:
                continue
            tweet_texts.append(tweet['text'])

    tokenized = tokenize(tweet_texts)
    stop_removed = remove_stopwords(tokenized)
    #stemmed = stem(stop_removed)
    lemmatized = lemmatize(stop_removed)
    return lemmatized

def tokenize(tweets):
    tokenizer = nltk.TweetTokenizer()
    tweets_tokenized = []
    for text in tweets:
        cleaned = clean_text(text)
        tweets_tokenized.append(tokenizer.tokenize(cleaned))
    return tweets_tokenized

def clean_text(text):
    strip_urls = re.sub(r"http\S+", "", text)
    strip_punctuation = ''.join(char for char in strip_urls if char not in string.punctuation)
    clean_text = strip_punctuation.lower()
    return clean_text


def remove_stopwords(tweets):
    stop = set(stopwords.words('english'))
    # add some tweet-specific terms for stopword list
    stop.update(('rt', ':', ',', '.'))
    tweets_stop = []
    for tweet in tweets:
        tweet_trimmed = [token for token in tweet if token not in stop]
        tweets_stop.append(tweet_trimmed)
    return tweets_stop

def stem(tweets):
    stemmer = PorterStemmer()
    stemmed_tweets = []
    for tweet in tweets:
        # do not stem user mentions
        stemmed = [stemmer.stem(token) if token[0] != '@' else token for token in tweet]
        stemmed_tweets.append(stemmed)
    return stemmed_tweets

def lemmatize(tweets):
    lemmatizer = WordNetLemmatizer()
    lemmatized_tweets = []
    for tweet in tweets:
        # do not stem user mentions
        lemmatized = [lemmatizer.lemmatize(token) if token[0] != '@' else token for token in tweet]
        lemmatized_tweets.append(lemmatized)
    return lemmatized_tweets

if __name__ == "__main__":
    main()