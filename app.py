
# Flask app so that interactive elements have a URL to call back to.
# This is using the default dev server and a http tunnel. Jank af

from flask import Flask, request, Response
import json
from slack import WebClient
from slack.errors import SlackApiError
import time

OAUTH_TOKEN = "xoxb-2538044939847-2546117567878-Q548dhVCnL8I2v3dt4oylnuZ"

app = Flask(__name__)
client = WebClient(token=OAUTH_TOKEN)

### BUTTONS

# Buttons require the 'fallback' field or else they won't appear in the slack client. Sad

activate_button = [{
    "fallback": "Upgrade your Slack client to use messages like these.",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "callback_id": "activate_button",
    "actions": [{"name": "press", "text": "Yes!","type": "button"}]
}]

deactivate_button = [{
    "fallback": "Upgrade your Slack client to use messages like these.",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "callback_id": "deactivate_button",
    "actions": [{"name": "press", "text": "Deactivate slackboss indefinitely", "type": "button"}]
}]

# TODO not necessary if on strict schedule w/ break length
confirm_break_button = [{
    "fallback": "Upgrade your Slack client to use messages like these.",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "callback_id": "confirm_break_button",
    "actions": [{"name": "press", "text": "I've taken a break", "type": "button"}]
}]

set_timer_interval_button = [{
    "fallback": "Upgrade your Slack client to use messages like these.",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "callback_id": "set_timer_interval_button",
    "actions": [{"name": "press", "text": "Set timer interval length", "type": "button"}]
}]

set_break_duration_button = [{
    "fallback": "Upgrade your Slack client to use messages like these.",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "callback_id": "set_break_duration_button",
    "actions": [{"name": "press", "text": "Set break length", "type": "button"}]
}]

timer_interval_menu = [{
    "fallback": "Upgrade your Slack client to use messages like these.",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "callback_id": "timer_interval_menu",
    "actions": [{"name": "timer_interval_menu", "text": "Set time interval", "type": "select", "data_source": "external" }]
}]

break_duration_menu = [{
    "fallback": "Upgrade your Slack client to use messages like these.",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "callback_id": "break_duration_menu",
    "actions": [{"name": "break_duration_menu", "text": "Set break duration", "type": "select", "data_source": "external" }]
}]

### ENDPOINTS

@app.route("/interact", methods=['POST'])
def interact_handler():
    payload = json.loads(request.form['payload'])
    callback_id = payload['callback_id']
    channel_id = payload['channel']['id']
    original_message_ts = payload['message_ts']

    if callback_id == "confirm_break_button":
        response = client.chat_postMessage(channel=channel_id, text="Ok! Good job!")

    elif callback_id == 'activate_button':
        client.chat_update(channel=channel_id, ts=original_message_ts, text='Ok, Slackboss is activated!', attachments=[])

    elif callback_id == 'deactivate_button':
        client.chat_update(channel=channel_id, ts=original_message_ts, text='Ok, Slackboss is deactivated!', attachments=[])

    elif callback_id == 'set_timer_interval_button':
        # client.chat_update(channel=channel_id, ts=original_message_ts, text='Ok, Slackboss is deactivated!', attachments=[])
        send_timer_interval_menu(channel_id, ts=original_message_ts)

    elif callback_id == 'set_break_duration_button':
        send_break_duration_menu(channel_id, ts=original_message_ts)

    elif callback_id == "timer_interval_menu":
        value = payload['actions'][0]['selected_options'][0]['value']
        update_message(f"Timer interval set to {value} minutes", channel_id, ts=original_message_ts)

    elif callback_id == "break_duration_menu":
        value = payload['actions'][0]['selected_options'][0]['value']
        update_message(f"Break duration set to {value} minutes", channel_id, ts=original_message_ts)

    return request.data

@app.route("/options-load", methods=['POST'])
def options_load_handler():
    payload = json.loads(request.form['payload'])
    callback_id = payload['callback_id']
    if callback_id == 'timer_interval_menu':
        menu_options = {'options': [
            dict(text='15 minutes', value='15'),
            dict(text='20 minutes', value='20'),
            dict(text='30 minutes', value='30'),
            dict(text='45 minutes', value='45'),
            dict(text='60 minutes', value='60')
        ]}
        return Response(json.dumps(menu_options), mimetype='application/json')

    elif callback_id == 'break_duration_menu':
        menu_options = {'options': [
            dict(text='1 minute', value='1'),
            dict(text='2 minutes', value='2'),
            dict(text='5 minutes', value='5'),
            dict(text='10 minutes', value='10'),
            dict(text='15 minutes', value='15')
        ]}
        return Response(json.dumps(menu_options), mimetype='application/json')
    else:
        assert False

@app.route("/event", methods=['POST'])
def event_handler():
    payload = json.loads(request.get_data())
    channel_id = payload['event']['channel']
    send_default_active_response(channel_id)
    return request.get_data()
    # return json.loads(request.get_data())['challenge']

### FUNCTIONS

def send_message(message, channel_id='U02GATBE7E0'):
    try:
        response = client.chat_postMessage(channel=channel_id, text=message)
    except SlackApiError as e:
      assert e.response["error"]

def update_message(message, channel_id='U02GATBE7E0', ts=None, attachments=None):
    try:
        response = client.chat_update(channel=channel_id, ts=ts, text=message, attachments=None)
    except SlackApiError as e:
      assert e.response["error"]

def send_timer_interval_menu(channel_id='U02GATBE7E0', ts=None):
    try:
        if ts:
            response = client.chat_update(channel=channel_id, ts=ts, text="Ok, you can set time interval between breaks", attachments=timer_interval_menu)
        else:
            response = client.chat_postMessage(channel=channel_id, text="Ok, you can set time interval between breaks", attachments=timer_interval_menu)
    except SlackApiError as e:
      assert e.response["error"]

def send_break_duration_menu(channel_id='U02GATBE7E0', ts=None):
    try:
        if ts:
            response = client.chat_update(channel=channel_id, ts=ts, text="Ok, you can set the break duration", attachments=break_duration_menu)
        else:
            response = client.chat_postMessage(channel=channel_id, text="Set break duration", attachments=break_duration_menu)
    except SlackApiError as e:
      assert e.response["error"]

# prototype
def send_break_meme(channel_id='U02GATBE7E0'):
    try:
        response = client.chat_postMessage(channel=channel_id, text="Take a break!", attachments=[{
          "fallback": "meme",
          "text": "drink water!",
          "image_url": "https://i.imgur.com/PTCSYU6.jpeg",
        }] + confirm_break_button)
    except SlackApiError as e:
      assert e.response["error"]

def send_default_inactive_response(channel_id='U02GATBE7E0'):
    try:
        response = client.chat_postMessage(channel=channel_id, text="Hi! Wanna activate slackboss?", attachments=activate_button)
    except SlackApiError as e:
      assert e.response["error"]

def send_default_active_response(channel_id='U02GATBE7E0'):
    try:
        response = client.chat_postMessage(channel=channel_id, text="Hi! What's up?", attachments=deactivate_button + set_timer_interval_button + set_break_duration_button)
    except SlackApiError as e:
      assert e.response["error"]

while True:
    time.sleep(1)
    print('x')




