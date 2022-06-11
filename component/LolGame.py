import os
import re
import sqlite3
from typing import Any, Dict, List, TypedDict
from discord import Client, Message, VoiceChannel, Member
import random 
import math
from . import Component
from riot_api import tournament

DB_NAME = os.getenv('SQLITE3_DB_NAME')
channel_mention_re = re.compile("<#(\d+)>")
member_mention_re = re.compile("<@(\d+)>")

def to_mention(s: str):
    return f"<@{s}>"

previous_players = {}
    
class LolGame(Component):
    def __init__(self, client: Client, g_prefix: str="k:"):
        self.g_prefix = g_prefix
        super().__init__("lolgame", "LoLゲーム作成", client, alias=["lg"], command="[オプション]")

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
        elif main_command == "setscore":
            await self.set_send_score(message, contents[2], int(contents[1]))
        elif main_command == "showscore" and len(contents) > 1:
            await self.send_score(message, contents[1])
        else:
            await self.create_teams(message, contents)
        
    def get_help(self):
        return "\n".join([
            f"独自レートシステムでマッチングをします。現在ボイスチャンネルにいる場合、そのチャンネルのメンバーでチーム分けをします。(詳細は`{self.g_prefix}lolgame help`)",
        ])
    def get_detail_help(self):
        com = f"{self.g_prefix}lolgame"
        return "\n".join([
            "**コマンド:**",
            f"`{com}` - 現在ボイスチャンネルにいる場合、そのチャンネルのメンバーでチーム分けをします",
            f"`{com} replay` - 前回のマッチと同じメンバーでプレイします",
            f"`{com} setscore [-100~100の値] [プレイヤー]` - レートを変更します。",
            f"`{com} showrate [プレイヤー]` - プレイヤーのレートを表示します。",
            f"`{com} help` - ヘルプを表示します",
            "**オプション:**",
            f"`{com} ext:[リスト(コンマ区切り)]` - プレイヤーを追加します",
            f"`{com} channel:[チャンネル]` - 参照するチャンネルを変更します",
            f"`{com} rm:[メンバーリスト(コンマ区切り)]` - プレイヤーを除きます",
            f"`{com} noCode:true` - トーナメントコードを生成しません(結果はレートに反映されません)",
        ])

    async def get_players(self, message: Message, setting: Dict[str, str]) -> List[str]:
        channel: VoiceChannel = None
        if setting.get("channel") is not None:
            m = channel_mention_re.match(setting.get("channel"))
            if m is None:
                raise Exception(f"チャンネル設定が不正です(値: {setting.get('channel')})。")
            channel = self.client.get_channel(int(m.groups()[0]))
        elif message.author.voice is not None and isinstance(message.author.voice.channel, VoiceChannel):
            channel = message.author.voice.channel

        members: List[Member] = [] if channel is None else channel.members
        players: List[str] = [m.id for m in members]
        if setting.get("ext") is not None:
            matches = [(s, member_mention_re.match(s)) for s in setting.get("ext").split(",")]
            for match in matches:
                if match[1] is None:
                    raise Exception(f"{match[0]}はユーザーではありません。")
            
            players.extend([match[1][1] for match in matches])
                
        if setting.get("rm") is not None:
            players = [p for p in players if p not in [member_mention_re.match(s)[1] for s in setting.get("rm").split(",")]]
        
        return players


    async def create_teams(self, message: Message, setting_strs: List[str]):
        
        setting = Component.parse_config(setting_strs)
        players = await self.get_players(message, setting)
        previous_players[message.guild.id] = players
        
        await self.create_teams_from_players(message, players, setting)
    
    
    async def retry_teams(self, message: Message, setting_strs: List[str]):
        setting = Component.parse_config(setting_strs)

        if previous_players.get(message.guild.id) is None:
            raise Exception("前回のチームはありません。")
        await self.create_teams_from_players(message, previous_players[message.guild.id], setting)
    
    
    async def send_help(self, message: Message):
        await message.channel.send(self.get_detail_help())

    async def create_teams_from_players(self, message: Message, players: List[str], setting: Dict[str, str]):
        (teamA, teamB, teamAsum, teamBsum) = self.create_balanced_teams([{'obj': p, 'score': self.get_score(p)} for p in players])

        resultA: List[str] = []
        resultA.append(f"🔵チーム:(スコア{teamAsum})")
        resultA.append(", ".join([to_mention(s) for s in teamA]))
        await message.channel.send("\n".join(resultA))

        resultB: List[str] = []
        resultB.append(f"🔴チーム:(スコア{teamBsum})")
        resultB.append(", ".join([to_mention(s) for s in teamB]))
        await message.channel.send("\n".join(resultB))

        if setting.get("noCode").lower() == "true":
            return

        # tournament_code = await tournament.create_code(setting.get("pick"))
        # await message.channel.send(f"トーナメントコード - {tournament_code}")

    
    Player = TypedDict('TypedDict', {'obj': Any, 'score': int})
    def create_balanced_teams(self, players: List[Player], rand_rate=0.3):
        if len(players) % 2 != 0:
            raise Exception("プレイヤー数は偶数でなければなりません。")

        sorted_players = sorted(players, key=lambda x: x["score"])
        for i in range(0, len(players) // 2 - 1):
            if random.random() < rand_rate:
                sorted_players[2 * i + 1], sorted_players[2 * i + 2] = sorted_players[2 * i + 2], sorted_players[2 * i + 1]
        
        teamA= [sorted_players[0]["obj"]]
        teamAsum = sorted_players[0]["score"]
        teamB = [sorted_players[1]["obj"]]
        teamBsum = sorted_players[1]["score"]

        for i in range(1, len(players) // 2):
            if (teamAsum < teamBsum and random.random() > rand_rate) or (teamAsum >= teamBsum and random.random() <= rand_rate):
                teamA += [sorted_players[2 * i + 1]["obj"]]
                teamAsum += sorted_players[2 * i + 1]["score"]
                teamB += [sorted_players[2 * i]["obj"]]
                teamBsum += sorted_players[2 * i]["score"]
            else:
                teamA += [sorted_players[2 * i]["obj"]]
                teamAsum += sorted_players[2 * i]["score"]
                teamB += [sorted_players[2 * i + 1]["obj"]]
                teamBsum += sorted_players[2 * i + 1]["score"]

        return (teamA, teamB, teamAsum, teamBsum)

    def get_score(self, playerID: str) -> int:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        res = cur.execute("SELECT score FROM account WHERE discord_id=?", (playerID, )).fetchone()
        conn.close()

        return res[0]
    
    async def send_score(self, message: Message, playerID: str):
        score = self.get_score(member_mention_re.match(playerID)[1])
        await message.channel.send(f"現在の {playerID} のレート: {score}")

    def set_score(self, playerID: str, score: int) -> int:
        if score > 100 or score < -100:
            raise Exception(f"スコアは-100~100の値で設定してください")
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("UPDATE account SET score=? WHERE discord_id=?", (score, playerID))
        res = cur.execute("SELECT score FROM account WHERE discord_id=?", (playerID, )).fetchone()
        if res != None:
            conn.commit()
        conn.close()
        if res == None:
            raise Exception(f"プレイヤーID{playerID}が見つかりませんでした")
        return res[0]
    
    async def set_send_score(self, message: Message, playerID: str, score: int):
        score = self.set_score(member_mention_re.match(playerID)[1], score)
        await message.channel.send(f"現在の {playerID} のレート: {score}")