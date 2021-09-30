
# Flask app so that interactive elements have a URL to call back to.
# This is using the default dev server and a http tunnel. Jank af

from flask import Flask, request, Response
import json
from slack import WebClient
from slack.errors import SlackApiError

OAUTH_TOKEN = "xoxb-2538044939847-2546117567878-Q548dhVCnL8I2v3dt4oylnuZ"

app = Flask(__name__)
client = WebClient(token=OAUTH_TOKEN)

### BUTTONS

stop_timer_button = [{
    "fallback": "Upgrade your Slack client to use messages like these.",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "callback_id": "stop_timer",
    "actions": [{"name": "press", "text": "I've taken a break", "type": "button"}]
}]

activate_button = [{
    "fallback": "Upgrade your Slack client to use messages like these.",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "callback_id": "stop_timer",
    "actions": [{"name": "press", "text": "Yes!","type": "button"}]
}]

deactivate_button = [{
    "fallback": "Upgrade your Slack client to use messages like these.",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "callback_id": "deactivate",
    "actions": [{"name": "press", "text": "Deactivate slackboss", "type": "button"}]
}]

settings_button = [{
    "fallback": "Upgrade your Slack client to use messages like these.",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "callback_id": "settings",
    "actions": [{"name": "press", "text": "Open settings", "type": "button"}]
}]

interval_menu = [{
    "fallback": "Upgrade your Slack client to use messages like these.",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "callback_id": "interval_option",
    "actions": [{"name": "games_list", "text": "Set time interval", "type": "select", "data_source": "external" }]
}]

### ENDPOINTS

@app.route("/interact", methods=['POST'])
def interact():
    payload = json.loads(request.form['payload'])
    callback_id = payload['callback_id']
    channel_id = payload['channel']['id']
    if callback_id == "stop_timer":
        response = client.chat_postMessage(channel=channel_id, text="Ok! Good job!")
    elif callback_id == 'settings':
        print("SETTINGS")
        send_settings(channel_id)
    elif callback_id == "interval_option":
        value = payload['actions'][0]['selected_options'][0]['value']
        send_message(f"Timer interval set to {value} minutes", channel_id)
    return request.data

@app.route("/options-load", methods=['POST'])
def options_load():
    payload = json.loads(request.form['payload'])
    callback_id = payload['callback_id']
    if callback_id == 'interval_option':
        menu_options = {'options': [
            dict(text='15 minutes', value='15'),
            dict(text='20 minutes', value='20'),
            dict(text='30 minutes', value='30'),
            dict(text='45 minutes', value='45'),
            dict(text='60 minutes', value='60')
        ]}
        return Response(json.dumps(menu_options), mimetype='application/json')
    else:
        assert False

### FUNCTIONS

def send_message(message, channel_id='U02GATBE7E0'):
    try:
        response = client.chat_postMessage(channel=channel_id, text=message)
    except SlackApiError as e:
      assert e.response["error"]

def send_settings(channel_id='U02GATBE7E0'):
    try:
        response = client.chat_postMessage(channel=channel_id, text="Settings", attachments=interval_menu)
    except SlackApiError as e:
      assert e.response["error"]

def send_stop_timer(channel_id='U02GATBE7E0'):
    try:
        response = client.chat_postMessage(channel=channel_id, text="Take a break!", attachments=[{
          "fallback": "meme",
          "text": "drink water!",
          "image_url": "https://i.imgur.com/PTCSYU6.jpeg",
        }] + stop_timer_button + interval_menu)
    except SlackApiError as e:
      assert e.response["error"]

def send_activation_message(channel_id='U02GATBE7E0'):
    try:
        response = client.chat_postMessage(channel=channel_id, text="Hi! Wanna activate slackboss?", attachments=activate_button)
    except SlackApiError as e:
      assert e.response["error"]

def send_active_response(channel_id='U02GATBE7E0'):
    try:
        response = client.chat_postMessage(channel=channel_id, text="Hi! What's up?", attachments=deactivate_button + settings_button)
    except SlackApiError as e:
      assert e.response["error"]

if __name__ == '__main__':
    # send_stop_timer()
    send_settings('C02FU1DQSAK')
    # send_active_response()
    # send_activation_message()




