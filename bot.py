#!/usr/bin/env python3
import os
from sre_parse import Verbose

import discord
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

@client.event
async def on_ready():

    print(
        f'{client.user} is connected'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'おはようございます' in message.content:
        await message.channel.send('元気があっていいですね')
    elif 'おはよう' in message.content:
        await message.channel.send('タメ口はいかがなものでしょうか?')
    
    if(message.content)
        


client.run(TOKEN)