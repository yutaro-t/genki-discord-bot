import os
import aiohttp

API_KEY = os.getenv('RIOT_API_KEY')

async def by_name(name: str):
    async with aiohttp.ClientSession() as session:
        url = f'https://jp1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={API_KEY}'
        async with session.get(url) as response:
            return await response.json()