import os
import sys

import dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from src.utils.query_wiki import get_summary

project_dir = os.path.dirname(__file__)
dotenv_path = os.path.join(project_dir, '.env')
dotenv.load_dotenv(dotenv_path)

# Initializes app with bot token and signing secret in .env file
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Listens to incoming messages that mention the app
# To learn available listener arguments,
# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.event("app_mention")
def mention_response(ack, payload, say):
    # say() sends a message to the channel where the event was triggered
    say(f"oh, it's you again <@{payload['user']}>")
    search_term = ' '.join(payload['text'].split()[1:])
    say(f"you want to know something about {search_term}? i'll TELL you something about {search_term}")
    say(get_summary(search_term))

@app.event("message")
def handle_message_events(logger, event, say):
    # say(f"hey <@{event['user']}>")
    # search_term = ' '.join(event['text'])
    # say(f"you want to know something about {search_term}? i'll TELL you something about {search_term}")
    # say(get_summary(search_term))
    logger.info(event['text'])

# Start app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()