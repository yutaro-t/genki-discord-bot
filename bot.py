import os

import discord
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'おはようございます' in message.content:
        await message.channel.send('元気があっていいですね')
    elif 'おはよう' in message.content:
        await message.channel.send('タメ口はいかがなものでしょうか?')
    if message.content == 'kocho::valroll':
        if message.author.name == 'tepel':
            await message.channel.send(
                random.choice(['レイナ','セージ','ジェット','レイズ','ヴァイパー','フェニックス','ブリムストーン','ソーヴァ'])
            )
        else:
            await message.channel.send(
                random.choice(['レイナ','セージ','ジェット','レイズ','サイファー','オーメン','ヴァイパー','フェニックス','ブリムストーン','ソーヴァ','キルジョイ'])
            )
        


client.run(TOKEN)