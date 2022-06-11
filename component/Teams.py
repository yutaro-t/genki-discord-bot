import re
from typing import List
from discord import Client, Message, VoiceChannel, Member, Embed
import random 
import math
from . import Component

channel_mention_re = re.compile("<#(\d+)>")

previous_players = {}

class Teams(Component):
    def __init__(self, client: Client, g_prefix: str="k:"):
        self.g_prefix = g_prefix
        super().__init__("teams", "チーム分け", client, alias=["t", "team"], command="")

    async def on_message(self, message, contents):
        if len(contents) == 0:
            await self.create_teams(message, [])
            return

        main_command = contents[0].lower()
        setting_strs = contents[1:] if len(contents) > 1 else []

        if main_command == "create":
            await self.create_teams(message, setting_strs)
        elif main_command == "retry" or main_command == "replay":
            await self.retry_teams(message, setting_strs)
        elif main_command == "help" or main_command == "h":
            await self.send_help(message)
        else:
            await self.create_teams(message, contents)
        
    def get_help(self):
        return "\n".join([
            f"ランダムにチーム分けをします。現在ボイスチャンネルにいる場合、そのチャンネルのメンバーでチーム分けをします。(詳細は`{self.g_prefix}teams help`)",
        ])
    def get_detail_help(self):
        com = f"{self.g_prefix}teams"
        return "\n".join([
            "**コマンド:**",
            f"`{com}` - 現在ボイスチャンネルにいる場合、そのチャンネルのメンバーでチーム分けをします",
            f"`{com} replay` - 前回のマッチと同じメンバーでプレイします",
            f"`{com} help` - ヘルプを表示します",
            "**オプション:**",
            f"`{com} ext:[リスト(コンマ区切り)]` - プレイヤーを追加します",
            f"`{com} channel:[チャンネル]` - 参照するチャンネルを変更します",
            f"`{com} rm:[メンバーリスト(コンマ区切り)]` - プレイヤーを除きます",
        ])

    async def create_teams(self, message: Message, setting_strs: List[str]):
        
        setting = Component.parse_config(setting_strs)

        channel: VoiceChannel = None
        if setting.get("channel") is not None:
            m = channel_mention_re.match(setting.get("channel"))
            if m is None:
                raise Exception(f"チャンネル設定が不正です(値: {setting.get('channel')})。")
            channel = self.client.get_channel(int(m.groups()[0]))
        elif message.author.voice is not None and isinstance(message.author.voice.channel, VoiceChannel):
            channel = message.author.voice.channel

        members: List[Member] = [] if channel is None else channel.members
        players = [m.mention for m in members]
        if setting.get("ext") is not None:
            players.extend(setting.get("ext").split(","))
        if setting.get("rm") is not None:
            players = [p for p in players if p not in setting.get("rm")]
        
        previous_players[message.guild.id] = players
        
        await self.create_teams_from_players(message, players)
    
    
    async def retry_teams(self, message: Message, setting_strs: List[str]):
        setting = Component.parse_config(setting_strs)

        if previous_players.get(message.guild.id) is None:
            raise Exception("前回のチームはありません。")
        await self.create_teams_from_players(message, previous_players[message.guild.id])
    
    
    async def send_help(self, message: Message):
        await message.channel.send(self.get_detail_help())


    async def create_teams_from_players(self, message: Message, players: List[str]):
        random.shuffle(players)
        blue_team = players[0:math.ceil(len(players)/2)]
        red_team = players[math.ceil(len(players)/2):]

        resultA: List[str] = []
        resultA.append("🔵チーム:")
        resultA.append(", ".join(blue_team))
        await message.channel.send("\n".join(resultA))

        resultB: List[str] = []
        resultB.append("🔴チーム:")
        resultB.append(", ".join(red_team))
        await message.channel.send("\n".join(resultB))
        
