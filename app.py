
# Flask app so that interactive elements have a URL to call back to.
# This is using the default dev server and a http tunnel. Jank af

from datetime import datetime
from datetime import date
from flask import Flask, request, Response
import json
from slack import WebClient
from slack.errors import SlackApiError
import time
import os
import random

OAUTH_TOKEN = "xoxb-2538044939847-2546117567878-Q548dhVCnL8I2v3dt4oylnuZ"
USER_TOKEN ="xoxp-2538044939847-2565386880881-2543059939895-826f6a444d8a2a76c9e457bdfbd0f17f"

app = Flask(__name__)
client = WebClient(token=OAUTH_TOKEN)
user_client = WebClient(token=USER_TOKEN) 

###Initial Connection to Slackboss
##Attempts connection
##Testing connection - terminate program on failed connection (work in progress)
connected = client.api_test()
if connected['ok'] == False:
    print("Sorry, Slackboss forgot to pay the wifi bill and can't connect!")
    print("Please check your token and try again!")
    print("Token:", auth_token)
    quit()

time_to_break, duration = None, None


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

# Send button with break reminder
start_timer_button = [{
    "fallback": "Upgrade your Slack client to use messages like these.",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "callback_id": "start_timer",
    "actions": [{"name": "press", "text": "I am taking my break", "type": "button"}]
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

    elif callback_id == 'start_timer':
        on_break=True

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

### SLACKBOTDEMO CODE

###Channel Checker: tells you the conversation id of a channel and if it exists
#input: string, channel you are looking for
#output: string, conversation ID, returns None if the conversation doesn't exist
def checkChannel(myChannel):
    all_channels = client.conversations_list()
    #check all slack group channels to make sure this one exists
    for response in all_channels:
            for channel in response["channels"]:
                if channel["name"] == myChannel:
                    print(f"Found conversation ID:",channel["id"])
                    return channel["id"]
    print("We couldn't find a group with that name, sorry!")
    return None

###Message sender: sends message to channel (will be expanded to send to people
#and multiple groups)
#input: (string, string, optional strnig). (channel name of destination*or conversationID, text Message, attachment file path)
#output: None
def sendText(destinationChannel, message, attachments = None):
    try:
      response = client.chat_postMessage(
        channel=destinationChannel,
        text=message,
        attachments=attachments
      )
      print("Message sent to", destinationChannel, "successfully!")
    except SlackApiError as e:
      # You will get a SlackApiError if "ok" is False
      assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found''

##sends single image specified by image object, as well as message to channel of your choosing
#input: string, string, image object - give function the chanel to speak to and message and imageLink in image objecty
#output: None
def sendImage(destinationChannel, message, image = None):
    try:
      response = client.chat_postMessage(
        channel=destinationChannel,
        text=message,
        attachments = image
      )
      print("Message sent to", destinationChannel, "successfully!")
    except SlackApiError as e:
      # You will get a SlackApiError if "ok" is False
      assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'

#will pick a random meme from a list of image urls and then sends one to the specified channel
#input: int. range of memes available
#output: none. will simply post the image
def sendRandomMeme(destinationChannel, title, message = "Commencing Meme Blast..."):
    curr_directory = os.path.dirname(__file__) #<-- this is the computers absolute directory for this foler
    local_path = "Memes/StopWorkingMemes.txt"#<-- we are combining our current path with the next path to our memes

    #construct the local path from the absolute path
    memes_file_path = os.path.join(curr_directory, local_path)
    memes_file = open(memes_file_path, "r")
    list_of_memes = [(line.strip()).split() for line in memes_file]

    #select a meme randomly
    selected_meme = random.choice(list_of_memes)[0]

    image = [{"title": title, "image_url": selected_meme}]
    sendImage(destinationChannel, message, image)

#creates a dictionary calender that stores the break plans for each day
#only for septamber,october as of now for testing purposes
###months will have a list of days and each day will have its own list of breaks. each days
#has its own list because it stores the times of their breaks as well as there duration
#as follows (break time PST, break duration in mins)
def createCalender():
    cal = {"September": None, "October": None}
    #give the months the correct number of days (a dictionary may improve efficiancy)
    cal["September"] = [None for x in range(31)]
    cal["October"] = [None for x in range(32)]
    #add fake mock schedule for testing:
    #the pairs have (break time, duration) break times are in hours, so 16.25 *60 would convert it to minutes

    #break object format (float, float): (time of break in minutes, duration of break in minutes)
    break1 = (12.50 * 60, 5)
    #this means at 12:30 there will be a 5 min break. Convert hours to minute by multiplying by 60!!!
    break2 = (14.66 * 60, 30)
    break3 = (15 * 60, 30)
    break4 = (16 * 60, 30)

    cal["October"][1] = [break1, break2, break3, break4, (1400 * 60, 5)]#day 30 is position 31. pairs are (break time pst, break duration in mins)
    return cal

#this mightneed to be done for only one user at a time rather than in a channel
#link to Slack Api method https://api.slack.com/methods/dnd.setSnooze
#have this go when it is break time, set time length to the same as the break length
def setDoNotDisturb(destinationChannel, time):
    try:
        message = "Do Not Disturb set for {} minutes".format(time)
        sendText(destinationChannel, message)
        response = user_client.dnd_setSnooze(num_minutes=1)
        print("Began do not disturb time")
    except SlackApiError as e:
        print("Failed to set do not disturb time")
        assert e.response["error"]

def findNextBreak(calender):
    today = date.today()

    day = today.strftime("%d")
    month = today.strftime("%B")

    todays_sched = calender[month][int(day)]

    now = datetime.now()
    #track i to keep index place what breaks have passed and to delete
    i=1
    for break_time, break_duration in todays_sched:
        #convert current time into minutes
        current_hour_in_minutes = float(now.strftime("%H")) *60
        current_minute = float(now.strftime("%M"))
        formated_time_in_minutes = current_hour_in_minutes + current_minute

        #find how many minutes until next break
        if break_time >= formated_time_in_minutes:
            #to find how long until next break, subtract first the hours. this is because you need to convert
            #the time into minutes to get it correct
            time_until_break_in_minutes = break_time-formated_time_in_minutes
            # time_until_break_in_minutes = (time_until_break_in_minutes*60) - current_minute

            # time_until_break_in_minutes = (break_time-formated_time_in_minutes)

            calender[month][int(day)] = todays_sched[i:]
            return (time_until_break_in_minutes, break_duration)
        i += 1
    #return none if you can't find anything
    return (None, None)


id = checkChannel("hackathon")
# setDoNotDisturb(id, 2)
workday_is_over = False
calender = createCalender()
in_break = False
counter = 0
time_to_break, duration = findNextBreak(calender)
break_duration = 0
on_break=False

@app.route("/poll")
def poll_handler():
    global time_to_break, in_break, counter, break_duration, workday_is_over, duration, on_break
    time.sleep(1)
    if time_to_break == None:
        print("No more breaks today!")
        sendText(id, "No more breaks today!! Final Stretch!")

    elif in_break:
        if break_duration % 60 == 0:
            sendRandomMeme(id, "Take A Break Now!!!")
            sendText(id, "Break will end in " + str(duration - break_duration / 60))
            # for i in range(minutes * 60):
            #     time.sleep(1)
        break_duration += 1
        if break_duration >= duration * 60:
            sendText(id, "The break is over, back to work!!")
            in_break = False
            time_to_break, duration = findNextBreak(calender)
            break_duration = 0
    else:
        if counter % (60) == 0:
            sendText(id, str(time_to_break)+" mins until next break!")

        if time_to_break <= 0:
            sendRandomMeme(id, "Take A Break Now!!!")
            sendText(id, '', attachments=start_timer_button)
            not_on_break_timer=0
            while not on_break:
                if not_on_break_timer==300:
                    sendText('U02H32JVDHN', 'Tell your friend to take their break!')
                    break
                not_on_break_timer+=1
            sendText(id, "Break will end in " + str(duration))
            in_break = True    
        # start_break_timer(id, duration)
    print(counter, time_to_break, duration, break_duration)
    time_to_break -= 1.0 / 60
    counter += 1
    return ''

#test the functionality
# def TestFunctions():
    # sendText('U02H32JVDHN', '', attachments=start_timer_button)
    # start_break_timer('U02H32JVDHN', 2)
#     while not workday_is_over:
#         time.sleep(1)
#         if time_to_break == None:
#             print("No more breaks today!")
#             sendText(id, "No more breaks today!! Final Stretch!")

#         elif in_break:
#             sendRandomMeme(id, "Take A Break Now!!!")
#             sendText(id, "Break will end in " + str(minutes))
#             for i in range(minutes * 60):
#                 time.sleep(1)
#             sendText(id, "The break is over, back to work!!")
#             in_break = False
#             time_to_break, duration = findNextBreak(calender)
#         else:
#             if counter % (60 * 10) == 0:
#                 sendText(id, str(time_to_break)+" mins until next break!")

#             if time_to_break <= 1:
#                 in_break = True    
#             # start_break_timer(id, duration)
#         print(counter)
#         counter += 1

    # start_timer(1)

    # sendText(id, "This function is working correctly")
    # image_url = "https://pics.awwmemes.com/need-dis-sleepy-la-paresse-on-twitter-almost-lunch-time-54243381.png"
    # attachments = [{"title": "Take Your Break!!!", "image_url": image_url}]
    # sendImage(id, "Commencing Meme Blast...", attachments)

    # sendRandomMeme(id, "Take A Break Now!!!")

# TestFunctions()


