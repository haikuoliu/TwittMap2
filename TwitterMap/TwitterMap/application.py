from flask import render_template, request, Flask
from flask_socketio import SocketIO, send
from streaming import *
from worker import *
import requests

application = Flask(__name__)
application.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(application)


@application.route('/')
def index():
    return render_template('index.html');


@application.route('/data/<keyword>')
def data(keyword):
    # get data from es
    r = requests.post('http://search-twitter-1-kf5qeriqw5iu6uasbyv6dmwfbq.us-west-2.es.amazonaws.com/_search/',"",{
            "size": 10000, "query": {
                "query_string": {
                    # "fields": ["text", "_index"],
                    # "query":  keyword + " AND user"
                    "query": "_index: sentitwitter"
                }
            }
        }
    )
    results = json.loads(r.content);
    results = results['hits'];
    js_results = "eqfeed_callback(" + json.dumps(results) + ");";
    return js_results


@application.route('/updatedata/<keyword>')
def updatedata(keyword):
    # get data from es
    r = requests.post('http://search-twitter-1-kf5qeriqw5iu6uasbyv6dmwfbq.us-west-2.es.amazonaws.com/_search/',"",{
            "size": 10000, "query": {
                "query_string": {
                    # "fields": ["text", "_index"],
                    # "query":  keyword + " AND user"
                    "query": "(_index: sentitwitter)"
                }
            }
        }
    )
    results = json.loads(r.content);
    # print results
    results = results['hits'];
    js_results = json.dumps(results);
    return js_results;


# this is the endpoint of sns
@application.route('/sns', methods=['GET', 'POST', 'PUT'])
def sns():
    # AWS sends JSON with text/plain mimetype
    try:
        js = json.loads(request.data)
    except:
        pass

    hdr = request.headers.get('X-Amz-Sns-Message-Type')

    if hdr == 'Notification':
        print "comes notification"
        print "Message:" + js['Message']
        # send message to the front here
        socketio.emit('real_tweets', js['Message'])
   # subscribe to the SNS topic
    elif hdr == 'SubscriptionConfirmation' and 'SubscribeURL' in js:
        requests.get(js['SubscribeURL'])
    return 'OK\n'


@application.route('/google_map/<keyword>')
def google_map(keyword):
    return render_template('googlemap_markers.html', keyword=keyword)


# for real time via socket
@application.route('/google_map_real/<keyword>')
def google_map_real(keyword):
    return render_template('googlemap_markers_realtime.html', keyword=keyword)


if __name__ == '__main__':
    socketio.run(
        application,
        host="0.0.0.0",
        port=5000
        # threaded=True
    )

