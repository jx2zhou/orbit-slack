#import slack dependencies and random number generator and os for file nav
from slack import WebClient
from slack.errors import SlackApiError
import random
import os
# Flask app so that interactive elements have a URL to call back to.
# This is using the default dev server and a http tunnel. Jank af

from flask import Flask, request, Response
import json


#authentication token to connect to slackboss and create web client.
#do NOT save auth_token in public repo or we will automatically be forced
#to recreate the auth tocken and re-add slackbot to channels
auth_token = "xoxb-2538044939847-2546117567878-Q548dhVCnL8I2v3dt4oylnuZ"
client = WebClient(token=auth_token)

app = Flask(__name__)

#this is probably a bad idea, storing the users probably not great
users_store = {}

def save_users(users_array):
    for user in users_array:
        # Key user info on their unique user ID
        user_id = user["id"]
        # Store the entire user object (you may not need all of the info)
        users_store[user_id] = user

def getUsers():
    try:
        # Call the users.list method using the WebClient
        # users.list requires the users:read scope
        response = client.users_list()
        save_users(response["members"])
        print(users_store)
    except SlackApiError as e:
        print("error getting users")
        assert e.response["error"]
    



###Channel Checker: tells you the conversation id of a channel and if it exists
#input: string, channel you are looking for
#output: string, conversation ID, returns None if the conversation doesn't exist
def checkChannel(myChannel):
    all_channels = client.conversations_list()
    for response in all_channels:
            for channel in response["channels"]:
                if channel["name"] == myChannel:
                    print(f"Found conversation ID:",channel["id"])
                    return channel["id"]
    print("We couldn'y find a group with that name, sorry!")
    return None


###Same as the menu for break duration### 

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
        sendText(f"Timer interval set to {value} minutes", channel_id)
    return request.data

@app.route("/options-load", methods=['POST'])
def options_load():
    payload = json.loads(request.form['payload'])
    callback_id = payload['callback_id']
    if callback_id == 'interval_option':
        menu_options = {'options': [
            dict(text='1 minute', value='1'),
            dict(text='2 minutes', value='2'),
            dict(text='3 minutes', value='3'),
            dict(text='4 minutes', value='4'),
            dict(text='5 minutes', value='5')
        ]}
        return Response(json.dumps(menu_options), mimetype='application/json')
    else:
        assert False
        
def send_settings(channel_id='U02GATBE7E0'):
    try:
        response = client.chat_postMessage(channel=channel_id, text="Do Not Disturb Time Length", attachments=interval_menu)
    except SlackApiError as e:
      assert e.response["error"]
      
###

###Message sender: sends message to channel (will be expanded to send to people
#and multiple groups)
#input: (string, string, optional strnig). (channel name of destination*or conversationID, text Message, attachment file path)
#output: None
def sendText(destinationChannel, message, attachments = None):
    try:
      response = client.chat_postMessage(
        channel=destinationChannel,
        text=message
      )
      print("Message sent to", destinationChannel, "successfully!")
    except SlackApiError as e:
      # You will get a SlackApiError if "ok" is False
      print("Failed to send message")
      assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found''

#this mightneed to be done for only one user at a time rather than in a channel
#link to Slack Api method https://api.slack.com/methods/dnd.setSnooze
#have this go when it is break time, set time length to the same as the break length
def setDoNotDisturb(destinationChannel, time):
    try:
        message = "Do Not Disturb set for {} minutes".format(time)
        sendText(destinationChannel, message)
        response = client.dnd_setSnooze(num_minutes=time)
        print("Began do not disturb time")
    except SlackApiError as e:
        print("Failed to set do not disturb time")
        assert e.response["error"]
        

        
#test the functionality
def TestFunctions():
    id = checkChannel("hackathon")
    #send_settings(id)
    #setDoNotDisturb(id, 2)
    getUsers()

TestFunctions()
