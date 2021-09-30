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
try:
  response = client.chat_postMessage(
    channel="hackathon",
    text="Hello from your Slackboss version -2!"
  )
except SlackApiError as e:
  # You will get a SlackApiError if "ok" is False
  assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'



###channel Checking (work in progress)
#
# channel_name = "hackathon"
# conversation_id = None
# try:
#     # Call the conversations.list method using the WebClient
#     result = client.conversations_list()
#     if conversation_id is not None:
#         for channel in result["channels"]:
#             if channel["name"] == channel_name:
#                 conversation_id = channel["id"]
#                 #Print result
#                 print(f"Found conversation ID: {conversation_id}")
#
# except SlackApiError as e:
#     print(f"Error: {e}")
