import os
import re
import dotenv
import openai
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from .controller.chatgpt import ChatGPTController

# Initializes your app with your bot token and signing secret
dotenv.load_dotenv()
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET=os.environ.get("SLACK_SIGNING_SECRET")
app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.event("app_mention")
def handle_app_mention(body, say, logger):
    controller = ChatGPTController(app)
    thread_ts = body['event'].get('thread_ts', None) or body['event']['ts']
    channel = body['event']['channel']
    _ = controller.handle(say=say, channel=channel, thread_ts=thread_ts)
    logger.info(body)
    print(body)


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
