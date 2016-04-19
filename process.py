import sys
import re
import json
import nltk
from nltk.corpus import stopwords

def main():

    raw_tweets = open(sys.argv[1])
    processed_tweets = process(raw_tweets)

    for tweet in processed_tweets:
        print (tweet)

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
    processed = remove_stopwords(tokenized)
    return processed

def tokenize(tweets):
    tokenizer = nltk.TweetTokenizer()
    tweets_tokenized = []
    for text in tweets:
        clean_text = re.sub(r"http\S+", "", text)
        tweets_tokenized.append(tokenizer.tokenize(clean_text))
    return tweets_tokenized


def remove_stopwords(tweets):
    stop = set(stopwords.words('english'))
    # add some tweet-specific terms for stopword list
    stop.update(('RT', ':', ',', '.'))
    tweets_stop = []
    for tweet in tweets:
        tweet_trimmed = [token for token in tweet if token not in stop]
        tweets_stop.append(tweet_trimmed)
    return tweets_stop

if __name__ == "__main__":
    main()