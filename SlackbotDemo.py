####IMPORTANT NOPTICE!!! the way the app is currently programnmed takes a calender
#made from the createCalender function. In this function i only set breaks for today!
# if you want to test plz change these breaks in this function!!! we will add functionality
#to set breaks somewhere else lateer

#import slack dependencies and random number generator and os for file nav
from slack import WebClient
from slack.errors import SlackApiError
import random
import os
import time
#so you can schedule breaks
from datetime import datetime
from datetime import date
import math

#authentication token to connect to slackboss and create web client.
#do NOT save auth_token in public repo or we will automatically be forced
#to recreate the auth tocken and re-add slackbot to channels
auth_token = "xoxb-2538044939847-2546117567878-Q548dhVCnL8I2v3dt4oylnuZ"
client = WebClient(token=auth_token)

###Initial Connection to Slackboss
##Attempts connection
##Testing connection - terminate program on failed connection (work in progress)
connected = client.api_test()
if connected['ok'] == False:
    print("Sorry, Slackboss forgot to pay the wifi bill and can't connect!")
    print("Please check your token and try again!")
    print("Token:", auth_token)
    quit()

#################################dev tools for our use####################################

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
        text=message
      )
      print("Message sent to", destinationChannel, "successfully!")
    except SlackApiError as e:
      # You will get a SlackApiError if "ok" is False
      assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found''


 ###############DEPRACTED###############################
##builds attachment in correct format to be sent to slackboss ###############DEPRACTED
#input: string, string. image title and image image_url
#output: dictionary preformated to be sent to slackboss
#*optional: add feature to build atachment but also select random attachment from list
def buildAttachment(imageTitle, imageLink):
    my_attachment = [{"title": imageTitle, "image_url": imageLink}]
    return my_attachment
 ###############DEPRACTED###############################

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
    break2 = (17.05 * 60, 30)
    break3 = (17.05 * 60, 30)

    cal["September"][30] = [break1, break2, break3]#day 30 is position 31. pairs are (break time pst, break duration in mins)
    return cal

#############DEPRECATED#########################
#input: give this dates and times to add breaks on calender object
#BREAKS MUST BE IN ORDER
# def planWorkSchedule(breakTimes):
#     now = datetime.now()
#
#     current_time = now.strftime("%H:%M")
#     print("Current Time =", current_time)
#############DEPRECATED#########################


##function helps calculate the number of minutes until the next break, it also remembers the duration of that break
#input: calender object created from createCalender() containing schedules
#output: (float, float): (how long in minutes until next break, duration of break in minutes)
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

#start a timer that ends when your next break starts
def start_break_timer(id, minutes):
    sendRandomMeme(id, "Take A Break Now!!!")
    sendText(id, "Break will end in " + str(minutes))
    for i in range(minutes):
        time.sleep(60)
    sendText(id, "The break is over, back to work!!")

#test the functionality
def TestFunctions():
    # word= "test"
    # print(word[1:])
    id = checkChannel("hackathon")
    workday_is_over = False
    calender = createCalender()
    while not workday_is_over:
        time_to_break, duration = findNextBreak(calender)
        if time_to_break == None:
            print("No more breaks today!")
            sendText(id, "No more breaks today!! Final Stretch!")
        else:
            sendText(id, str(time_to_break)+" mins until next break!")
            time.sleep(time_to_break*60)

            start_break_timer(id, duration)
    #start_timer(1)

    #sendText(id, "This function is working correctly")
    #image_url = "https://pics.awwmemes.com/need-dis-sleepy-la-paresse-on-twitter-almost-lunch-time-54243381.png"
    #attachments = [{"title": "Take Your Break!!!", "image_url": image_url}]
    #sendImage(id, "Commencing Meme Blast...", attachments)

    sendRandomMeme(id, "Take A Break Now!!!")

TestFunctions()
