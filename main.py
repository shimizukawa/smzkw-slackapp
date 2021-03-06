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


@app.route('/slash', method='POST')
def slash():
    print(bottle.request.body.read())  # DEBUG
    f = bottle.request.forms
    if f['token'] != TOKEN:
        raise bottle.HTTPError(400, 'Invalid Token')

    response_data = {
        "response_type": "in_channel",
        "username": "まるこめ",
        "text": "wanさんはshotですか?",
        "attachments": [{
            "text": "1つ選んでね!",
            "fallback": "いまサーバー落ちてるわ",
            "callback_id": "wanshot",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {"name": "aji", "text": "合わせ味噌", "type": "button", "value": "miso"},
                {"name": "aji", "text": "料亭", "type": "button", "value": "ryoutei"},
                {"name": "aji", "text": "極", "style": "danger", "type": "button", "value": "kiwami",
                 "confirm": {"title": "まじで?", "text": "いっちゃう?",
                             "ok_text": "まじで！", "dismiss_text": "やめとく"}},
            ]
        }]
    }
    bottle.response.content_type = 'application/json'
    return json.dumps(response_data)


@app.route('/post', method='POST')
def post():
    payload = bottle.request.forms['payload']
    data = json.loads(payload)
    print(data)  # DEBUG
    if data['token'] != TOKEN:
        raise bottle.HTTPError(400, 'Invalid Token')

    user_name = data['user']['name']
    value = data['actions'][0]['value']
    taste = ''

    for a in data['original_message']['attachments'][0]['actions']:
        if a['value'] == value:
            taste = a['text']
            break

    text = f'{user_name}は `{taste}` を選びました'
    response_data = {"response_type": "in_channel", "username": "まるこめ", "text": text}
    bottle.response.content_type = 'application/json'
    return json.dumps(response_data)


if __name__ == '__main__':
    bottle.run(app, host='0.0.0.0', port=PORT)
