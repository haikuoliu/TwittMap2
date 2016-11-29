from flask import Flask
from streaming import *

app = Flask(__name__)


@app.route('/start_streaming/<keyword>')
def start_streaming(keyword):
    print "start_streaming!!!"
    # start streaming
    ls = TwitterMapListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, ls)
    # stream for the keyword, and send it to sqs
    stream.filter(track=[keyword])
    return 'OK'


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=4000,
        threaded=True
    )