import os
from slack_bolt import App
from pathlib import Path
from dotenv import load_dotenv
from slack_sdk import WebClient

env_path = Path('.') / '.env'
load_dotenv(override=True)


app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.event('message')
def update_home_tab(client, event, _):
    client.chat_postMessage(channel=event['channel'], text='olá dona do meu coração e da minha existencia <3')

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))