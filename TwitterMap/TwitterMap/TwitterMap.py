import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

consumer_key="uuchxIS2TFhIwAniWsnlq0Pwv"
consumer_secret="I9uQ7S2iKRFiFsbW7v1pLc2QETn74QasyVwDZ02jnnXTcsVDYG"
access_token="785668193465401348-FakTCROba7Icmsf87d0MJOA9YyiTnZk"
access_token_secret="UZpgs53Qd1CNJgQ9OqeCyLbp7b2mgIbpZWrRn1GR68lW1"

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['basketball'])