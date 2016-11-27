from flask import Flask
from streaming import *

app = Flask(__name__)


@app.route('/')
def index():
    print "start_streaming!!!"
    # start streaming
    ls = TwitterMapListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, ls)
    # stream for the keyword, and send it to sqs
    stream.filter(track=["Trump", "basketball", "pretty", "Facebook", "LinkedIn",
                            "Amazon", "Google", "Uber", "Columbia", "New York"])


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        threaded=True
    )


