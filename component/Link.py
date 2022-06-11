
from discord import Client, Embed
from . import Component
from riot_api.summoner import by_name
import sqlite3
import os


DB_NAME = os.getenv('SQLITE3_DB_NAME')

class Link(Component):
    def __init__(self, client: Client):
        super().__init__("link", "RIOTアカウント連携", client, command="[アカウント名]")

    async def on_message(self, message, contents):
        if len(contents) == 0:
            raise Exception("アカウント名を入力してください")
        
        if len(contents) == 1:
            account_name = contents[0]
            summoner = await by_name(account_name)

            conn = sqlite3.connect(DB_NAME)
            cur = conn.cursor()
            cur.execute("INSERT INTO account(discord_id, lol_id, score) VALUES (?, ?, 0);", (message.author.id, summoner['name']))
            conn.commit()
            conn.close()
            embed = Embed(
                title=summoner['name'], 
                color=0x00FFFF
            )
            embed.add_field(name='Discordユーザー', value=message.author.mention, inline=True)
            embed.add_field(name='サモナーレベル', value=summoner['summonerLevel'], inline=True)
            embed.set_thumbnail(url=f'http://ddragon.leagueoflegends.com/cdn/12.10.1/img/profileicon/{summoner["profileIconId"]}.png')
            await message.channel.send("アカウントをリンクしました", embed=embed)
    
            
        
    def get_help(self):
        return "\n".join([
            "RIOTアカウントを登録します。",
        ])
