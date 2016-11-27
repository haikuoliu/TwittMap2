import json
import config as Conf
from codecs import open
from dateutil import parser
import tweepy
import boto3

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='Erinyes')

consumer_key = Conf.TWITTER_APP_KEY
consumer_secret = Conf.TWITTER_APP_KEY_SECRET
access_token = Conf.TWITTER_ACCESS_TOKEN
access_token_secret = Conf.TWITTER_ACCESS_TOKEN_SECRET


class TwitterMapListener(tweepy.StreamListener):
    def __init__(self):
        super(TwitterMapListener, self).__init__()

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
                encoded_message = json.dumps(tweet, ensure_ascii=False)
                queue.send_message(MessageBody=encoded_message)
                print encoded_message
        except Exception as e:
            print 'error'

    def on_error(self, status):
        print status
        return False


if __name__ == '__main__':
    ls = TwitterMapListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, ls)
    stream.filter(track=["Trump", "basketball", "pretty", "Facebook", "LinkedIn",
                            "Amazon", "Google", "Uber", "Columbia", "New York"])