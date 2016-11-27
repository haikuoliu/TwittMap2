from flask import render_template, request, Flask
from streaming import *
from worker import *
app = Flask(__name__)


@app.route('/test')
def test():
    return render_template('index.html');


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


@app.route('/start_workers')
def start_workers():
    print "start_workers!!!"
    worker_pool(3)
    return 'OK'


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        threaded=True
    )


