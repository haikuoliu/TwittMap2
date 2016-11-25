from flask import render_template, request, Flask
import requests
import json
application = Flask(__name__)


@application.route('/')
def index():
    return render_template('index.html');


@application.route('/data/<keyword>')
def data(keyword):
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
    print results
    results = results['hits'];
    js_results = json.dumps(results);
    return js_results;


@application.route('/sns', methods = ['GET', 'POST', 'PUT'])
def sns():
    # AWS sends JSON with text/plain mimetype
    try:
        js = json.loads(request.data)
    except:
        pass

    hdr = request.headers.get('X-Amz-Sns-Message-Type')
    # subscribe to the SNS topic
    if hdr == 'SubscriptionConfirmation' and 'SubscribeURL' in js:
        requests.get(js['SubscribeURL'])

    if hdr == 'Notification':
        msg_process(js['Message'], js['Timestamp'])

    return 'OK\n'


def msg_process(msg, tstamp):
    js = json.loads(msg)
    msg = 'Region: {0} / Alarm: {1}'.format(
        js['Region'], js['AlarmName']
    )


@application.route('/googlemap/<keyword>')
def google_map(keyword):
    return render_template('googlemap_markers.html', keyword=keyword)

if __name__ == '__main__':
    application.run(
        host="0.0.0.0",
        port=5000
    )

