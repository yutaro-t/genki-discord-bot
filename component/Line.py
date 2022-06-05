import os
import re
from discord import Client
from linebot import LineBotApi
from linebot.models import TextSendMessage
from . import Component

channel_mention_re = re.compile("<#(\d+)>")


line_bot_api = LineBotApi(os.getenv('LINE_ACCESS_TOKEN'))
to = os.getenv('LINE_GROUP_ID')


class Line(Component):
    def __init__(self, client: Client):
        super().__init__("line", "ライン", client, alias=["l"], command="[送信内容]")

    async def on_message(self, message, contents):
        display_name = message.author.nick if message.author.nick is not None else message.author.name
        line_bot_api.push_message(to ,TextSendMessage(text=f'@{display_name}\n{" ".join(contents)}'))
        await message.channel.send("メッセージを送りました。")
        
        
    def get_help(self):
        return "\n".join([
            "ラインのメッセージを送ります。",
        ])
