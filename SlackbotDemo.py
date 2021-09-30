from slack import WebClient
from slack.errors import SlackApiError



slack_token = "xoxb-2538044939847-2546117567878-1O9yWKZQJxMWoNkLc9tRLJJm"
client = WebClient(token=slack_token)

###channel Checking

# channel_name = "hackathon"
# conversation_id = None
# try:
#     # Call the conversations.list method using the WebClient
#     print("hello")
#     for response in result client.conversations_list():
#         if conversation_id is not None:
#             break
#         for channel in result["channels"]:
#             if channel["name"] == channel_name:
#                 conversation_id = channel["id"]
#                 #Print result
#                 print(f"Found conversation ID: {conversation_id}")
#                 break
#
# except SlackApiError as e:
#     print(f"Error: {e}")

try:
  response = client.chat_postMessage(
    channel="C02FU1DQSAK",
    text="Hello from your Slackboss version -1!"
  )
except SlackApiError as e:
  # You will get a SlackApiError if "ok" is False
  assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'

# bool = client.rtm_connect(with_team_state=False)
print("test")
