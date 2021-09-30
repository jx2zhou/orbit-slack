from slack import WebClient
from slack.errors import SlackApiError


auth_token = "xoxb-2538044939847-2546117567878-Q548dhVCnL8I2v3dt4oylnuZ"
client = WebClient(token=auth_token)

###Initial Connection to Slackboss
##Attempts connection
##Testing connection - terminate program on failed connection (work in progress)
# connected = client.rtm_connect(with_team_state=False)
# if connected['ok'] == False:
#     print("Sorry, Slackboss forgot to pay the wifi bill and can't connect!")
#     print("Please check your token and try again!")
#     print("Token:", auth_token)
#     quit()

##Attempt connection to specified channel
#return error on failure
#*note: plz readd slackboss app to any channels after changing auth token
# try:
#   response = client.chat_postMessage(
#     channel="hackathon",
#     text="Hello from your Slackboss version -2!"
#   )
# except SlackApiError as e:
#   # You will get a SlackApiError if "ok" is False
#   assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'



#dev tools for your use

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
#input: (string, string). (channel name of destination*or conversationID, text Message)
#output: None
def sendMessage(destinationChannel, message):
    try:
      response = client.chat_postMessage(
        channel=destinationChannel,
        text=message
      )
      print("Message sent to", destinationChannel, "successfully!")
    except SlackApiError as e:
      # You will get a SlackApiError if "ok" is False
      assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'

#test the functionality
def TestFunctions():
    id = checkChannel("hackathon")
    sendMessage(id, "This function is working correctly")


TestFunctions()
