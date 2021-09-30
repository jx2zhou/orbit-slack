#import slack dependencies and random number generator and os for file nav
from slack import WebClient
from slack.errors import SlackApiError
import random
import os

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
    for response in all_channels:
            for channel in response["channels"]:
                if channel["name"] == myChannel:
                    print(f"Found conversation ID:",channel["id"])
                    return channel["id"]
    print("We couldn'y find a group with that name, sorry!")
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

##sends single image
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

#input: int. range of memes available
#output: none. will simply post the image
def sendRandomMeme(destinationChannel, title, message = "Commencing Meme Blast..."):
    curr_directory = os.path.dirname(__file__) #<-- this is the computers absolute directory for this foler
    local_path = "Memes/StopWorkingMemes.txt"#<-- we are combining our current path with the next path to our memes
    memes_file_path = os.path.join(curr_directory, local_path)
    memes_file = open(memes_file_path, "r")
    list_of_memes = [(line.strip()).split() for line in memes_file]
    selected_meme = random.choice(list_of_memes)[0]
    #image = buildAttachment(title, selected_meme)
    image = [{"title": title, "image_url": selected_meme}]
    sendImage(destinationChannel, message, image)


#test the functionality
def TestFunctions():
    id = checkChannel("hackathon")

    #sendText(id, "This function is working correctly")
    #image_url = "https://pics.awwmemes.com/need-dis-sleepy-la-paresse-on-twitter-almost-lunch-time-54243381.png"
    #attachments = [{"title": "Take Your Break!!!", "image_url": image_url}]
    #sendImage(id, "Commencing Meme Blast...", attachments)
    
    sendRandomMeme(id, "Take A Break Now!!!")

TestFunctions()
