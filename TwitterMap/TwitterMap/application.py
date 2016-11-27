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
        print "connected!!"
        print request.data
        print type(request.data)
        js = json.loads(request.data)
    except:
        pass

    hdr = request.headers.get('X-Amz-Sns-Message-Type')
    # subscribe to the SNS topic
    if hdr == 'SubscriptionConfirmation' and 'SubscribeURL' in js:
        requests.get(js['SubscribeURL'])

    if hdr == 'Notification':
        print "comes notification"
        # msg_process(js['Message'], js['Timestamp'])
        # send message to the front here
    return 'OK\n'


# process the message that we get frm sns
def msg_process(msg, tstamp):
    js = json.loads(msg)
    print "from sns!:" + js
    msg = 'Region: {0} / Alarm: {1}'.format(
        js['Region'], js['AlarmName']
    )
    print msg


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

