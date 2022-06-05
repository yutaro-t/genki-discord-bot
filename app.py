import os
from os.path import join, dirname
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from dotenv import load_dotenv
import requests, json


load_dotenv(join(dirname(__file__), '.env'))

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('LINE_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
webhook_url  = os.getenv('DISCORD_WEBHOOK_URL')
PREFIX = "k "



@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if 'おはようございます' in event.message.text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="元気があっていいですね"))
    elif 'おはよう' in event.message.text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="タメ口はいかがなものでしょうか?"))
    elif event.message.text[0:len(PREFIX)] == PREFIX:
        profile = line_bot_api.get_group_member_profile(event.source.group_id, event.source.user_id)
        display_name = profile.display_name
        main_content = {'content': f'{display_name} - {event.message.text[len(PREFIX):]}'}
        headers = {'Content-Type': 'application/json'}
        requests.post(webhook_url, json.dumps(main_content), headers=headers)
    


if __name__ == "__main__":
    app.run()