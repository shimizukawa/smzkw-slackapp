import os
import json

import bottle

TOKEN = os.environ.get('TOKEN', '')
PORT = int(os.environ.get('PORT', '8080'))

app = bottle.Bottle()


@app.route('/')
def ping():
    bottle.response.content_type = 'text/html'
    return """
    <html><body>
    <ul>
    <li><a href="/ping">ping response in JSON for testing</a></li>
    <li><a href="/post">POST button action from SlackApp</a></li>
    </ul>
    </body></html>
    """


@app.route('/ping')
def ping():
    bottle.response.content_type = 'application/json'
    return json.dumps({'message': 'pong'})


@app.route('/post', method='POST')
def post():
    data = bottle.request.json
    print('bottle.request.json:', data)
    data2 = bottle.request.forms
    print('bottle.request.forms:', data2)
    bottle.response.content_type = 'application/json'
    return data or data2


if __name__ == '__main__':
    bottle.run(app, host='0.0.0.0', port=PORT)
