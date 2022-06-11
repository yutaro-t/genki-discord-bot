
import re
from discord import Client, Embed, Message
from . import Component
from riot_api.summoner import by_name
import sqlite3
import os


DB_NAME = os.getenv('SQLITE3_DB_NAME')
member_mention_re = re.compile("<@(\d+)>")

class Link(Component):
    def __init__(self, client: Client):
        super().__init__("link", "RIOTアカウント連携", client, command="me [LoLアカウント名] | [Discordユーザー] [LoLアカウント名] | check")

    async def on_message(self, message, contents):
        if len(contents) == 0:
            raise Exception("アカウント名を入力してください")
        
        if len(contents) == 1 and contents[0] == 'check' :
            await self.check(message)
            return 
        if len(contents) == 1:
            await self.create(message, contents[0], message.author.id)
            return
        if len(contents) == 2 and contents[0] == 'me':
            await self.create(message, contents[1], message.author.id)
            return
        
        match = member_mention_re.match(contents[0])
        if len(contents) == 2 and match is not None:
            await self.create(message, contents[1], match[1])
            return
        
        raise Exception("無効なコマンドです。")
    
    async def check(self, message: Message):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        res = cur.execute('SELECT discord_id, lol_id FROM account WHERE discord_id = ?', (message.author.id, )).fetchone()
        conn.close()
        summoner = await by_name(res[1])
        await message.channel.send(embed=self.create_summoner_embed(summoner, message.author.id))

    async def create(self, message: Message, lol_id: str, discord_id: str):
        summoner = await by_name(lol_id)

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute('INSERT OR IGNORE INTO account(discord_id, lol_id, score) VALUES (?, ?, 0)', (discord_id, summoner['name']))
        cur.execute('UPDATE account SET lol_id = ? WHERE discord_id = ?', (summoner['name'], discord_id))
        conn.commit()
        conn.close()

        await message.channel.send("アカウントをリンクしました", embed=self.create_summoner_embed(summoner, discord_id))
    
    def create_summoner_embed(self, summoner, discord_id: str):
        embed = Embed(
            title=summoner['name'], 
            color=0x00FFFF
        )
        embed.add_field(name='Discordユーザー', value=f"<@{discord_id}>", inline=True)
        embed.add_field(name='サモナーレベル', value=summoner['summonerLevel'], inline=True)
        embed.set_thumbnail(url=f'http://ddragon.leagueoflegends.com/cdn/12.10.1/img/profileicon/{summoner["profileIconId"]}.png')
        return embed

        
    def get_help(self):
        return "\n".join([
            "RIOTアカウントを登録します。",
        ])
