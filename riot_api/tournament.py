import datetime
import os
from typing import Union
import aiohttp

API_KEY = os.getenv('RIOT_API_KEY')
PROVIDER_ID = os.getenv('TOURNAMENT_PROVIDER_ID')

async def create_code(pick: Union[str, None]) -> str:
        
    if pick not in ["BLIND_PICK", "DRAFT_MODE", "ALL_RANDOM", "TOURNAMENT_DRAFT", None]:
        raise Exception("pickが不正です。(可能な値: BLIND_PICK, DRAFT_MODE, ALL_RANDOM, TOURNAMENT_DRAFT)")
    
    async with aiohttp.ClientSession() as session:
        url1 = f'https://americas.api.riotgames.com/lol/tournament-stub/v4/tournaments?api_key={API_KEY}'
        json1 = {"name": f"makotornament{datetime.datetime.now().isoformat()}","providerId": PROVIDER_ID}
        pick = pick if pick is not None else "BLIND_PICK"
        async with session.post(url1, json=json1) as result1:
            tournament_code = await result1.text()
            url2 = f'https://americas.api.riotgames.com/lol/tournament-stub/v4/codes?count=1&tournamentId={tournament_code}&api_key={API_KEY}'
            json2 = {"mapType": "SUMMONERS_RIFT","pickType": pick,"spectatorType": "ALL","teamSize": 5}
            async with session.post(url2, json=json2):
                return tournament_code