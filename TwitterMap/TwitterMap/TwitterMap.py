import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import config as Conf
import pandas as pd
from elasticsearch import Elasticsearch
import boto3
from codecs import open
from dateutil import parser
import time
import requests

consumer_key=Conf.TWITTER_APP_KEY
consumer_secret=Conf.TWITTER_APP_KEY_SECRET
access_token=Conf.TWITTER_ACCESS_TOKEN
access_token_secret=Conf.TWITTER_ACCESS_TOKEN_SECRET
es= Elasticsearch()
    
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='Erinyes')

def appendlog(f, s):
    f.write(u'[{0}] {1}\n'.format(time.strftime('%Y-%m-%dT%H:%M:%SZ'), s))
    f.flush()

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """    
    def __init__(self, f):
        super(StdOutListener, self).__init__()
        self.f = f

    def on_data(self, data):
        try:
            decoded = json.loads(data)
            if decoded.get('lang') == 'en' and decoded.get('coordinates') is not None:
                geo = decoded['coordinates']['coordinates']
                timestamp = parser.parse(decoded['created_at']).strftime('%Y-%m-%dT%H:%M:%SZ')
                tweet = {
                    'user': decoded['user']['screen_name'],
                    'text': decoded['text'],
                    'geo': geo,
                    'time': timestamp
                }
                encoded = json.dumps(tweet, ensure_ascii=False)
                queue.send_message(MessageBody=encoded)
                appendlog(self.f, encoded)
        except Exception as e:
            appendlog(self.f, '{0}: {1}'.format(type(e), str(e)))

    def on_error(self, status):
        if status == 420:  # rate limited
            appendlog(self.f, 'Error 420')
            return False

if __name__ == '__main__':
    with open('streaming.log', 'a', encoding='utf8') as f:
        appendlog(f, 'Program starts')
        l = StdOutListener(f)
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        stream = Stream(auth, l)
        stream.filter(track=['basketball', 'Trump', 'pretty', 'job', 'Microsoft'])
