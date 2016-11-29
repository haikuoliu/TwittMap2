from flask import render_template, request, Flask
from worker import *

app = Flask(__name__)


@app.route('/start_workers')
def start_workers():
    print "start_workers!!!"
    worker_pool(3)
    return 'OK'


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=3000
        # threaded=True
    )

