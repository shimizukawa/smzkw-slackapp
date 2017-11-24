import os
import json

import bottle

TOKEN = os.environ.get('TOKEN', '')
PORT = int(os.environ.get('PORT', '8080'))

app = bottle.Bottle()


@app.route('/ping')
def ping():
    bottle.response.content_type = 'application/json'
    return json.dumps({'message': 'pong'})


@app.route('/post', method='POST')
def post():
    data = bottle.request.json
    print(data)
    bottle.response.content_type = 'application/json'
    return data


if __name__ == '__main__':
    bottle.run(app, host='0.0.0.0', port=PORT)
