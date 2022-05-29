﻿import re
from typing import List
from discord import Client, Message, VoiceChannel, Member
import random 
import math
from . import Component

channel_mention_re = re.compile("<#(\d+)>")

previous_players = {}

class Roll(Component):
    def __init__(self, client: Client):
        super().__init__("roll", "くじ引き", client, alias=["r", "kuji"], command="[選択肢リスト(コンマ区切り)]")

    async def on_message(self, message, contents):
        if len(contents) == 0:
            raise Exception("選択肢を入力してください")
        lst = "".join(contents).split(",")
        random.shuffle(lst)
        await message.channel.send(f"校長の選択: {lst[0]}")
        
    def get_help(self):
        return "\n".join([
            "くじ引きをします。",
        ])
