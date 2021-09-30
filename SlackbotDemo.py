from slack import WebClient
from slack.errors import SlackApiError
import logging 
import asyncio
from SlackbotTimer import Timer

slack_token = "xoxb-2538044939847-2546117567878-Q548dhVCnL8I2v3dt4oylnuZ"
client = WebClient(token=slack_token)

logger = logging.getLogger(__name__)

# file_name = 'https://i.imgur.com/PTCSYU6.jpeg'
file_name = './memes/michael_what.jpeg'

channel_id = 'C02FU1DQSAK'

def main():
  try:
    bot_timer = Timer()
    print('starting timer')
    bot_timer.start_timer(10)
    print('posting image')
    response = client.chat_postMessage(
      channel=channel_id,
      text='New message from slackboss!',
      attachments=[{
        "fallback": "meme",
        "text": "did u drink any water today?",
        "image_url": "https://i.imgur.com/PTCSYU6.jpeg",
      }]
    )
    logger.info(response)
  except SlackApiError as e:
    logger.error("error uploading file: {}".format(e))
    assert e.response["error"] 

# bool = client.rtm_connect(with_team_state=False)

if __name__ == "__main__":
  main()