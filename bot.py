#!/usr/bin/env python3
import os

import discord
from dotenv import load_dotenv
from component import *
import traceback

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = "k:"

intents = discord.Intents().default()
intents.members = True

client = discord.Client(intents=intents)
lst = ComponentList(PREFIX, [Teams(client), Roll(client)])

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
    
    if message.content[0:len(PREFIX)] == PREFIX:
        try:
            await lst.on_message(message, message.content[len(PREFIX):])
        except Exception as e:
            await message.channel.send(f"[エラー] {e}")
            print(traceback.format_exc())


client.run(TOKEN)