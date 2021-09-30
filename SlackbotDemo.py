from slack import WebClient
from slack.errors import SlackApiError
import logging 

slack_token = "xoxb-2538044939847-2546117567878-Q548dhVCnL8I2v3dt4oylnuZ"
client = WebClient(token=slack_token)

logger = logging.getLogger(__name__)

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

# file_name = 'https://i.imgur.com/PTCSYU6.jpeg'
file_name = './memes/michael_what.jpeg'

channel_id = 'C02FU1DQSAK'

try:
  response = client.chat_postMessage(
    channel=channel_id,
    text='Posting an image',
    attachments=[{
      "fallback": "meme",
      "text": "get back to work!",
      "image_url": "https://i.imgur.com/PTCSYU6.jpeg",
    }]
  )
  logger.info(response)
except SlackApiError as e:
  # You will get a SlackApiError if "ok" is False
  logger.error("error uploading file: {}".format(e))
  assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'

# bool = client.rtm_connect(with_team_state=False)