import requests
import json
import math
from datetime import datetime, timedelta
from pytz import timezone    


url = "https://api.sofascore.com/api/v1/sport/football/events/live"

payload = ""
headers = {
    "authority": "api.sofascore.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "if-none-match": 'W/"b8583b5f9a"',  
    "origin": "https://www.sofascore.com",
    "referer": "https://www.sofascore.com/",
    "sec-ch-ua": '["Not\\\\/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"]',  
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",  
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

response = requests.request("GET", url, data=payload, headers=headers)

jsondata = json.loads(response.text)


def calculate_elapsed_minutes(start_time, current_time):

    start_time_local = start_time.astimezone(timezone('Africa/Bamako'))
    current_time_local = current_time.astimezone(timezone('Africa/Bamako'))

    elapsed_time = current_time_local - start_time_local
    elapsed_minutes = elapsed_time.total_seconds() / 60
   
    
    return math.ceil(elapsed_minutes)

   
    

for game in jsondata['events']:
    try:
        league = game['tournament']['name']
        hometeam = game['homeTeam']['name']
        awayteam = game['awayTeam']['name']
        homescore = game['homeScore']['current']
        awayscore = game['awayScore']['current']

        game_start_timestamp = game['time']['currentPeriodStartTimestamp']
        game_start_time_utc = datetime.utcfromtimestamp(game_start_timestamp)
        game_start_time = game_start_time_utc.replace(tzinfo=timezone('UTC'))

        current_time = datetime.now(timezone('UTC'))

        
        status_description = game['status']['description']
        elapsed_minutes = calculate_elapsed_minutes(game_start_time, current_time)

        print(league, "\n", hometeam, homescore, " - ", awayscore, awayteam)
        if status_description == '2nd half':
            elapsed_minutes += 45
        if elapsed_minutes > 90:
            extra_time = elapsed_minutes - 90
            print ("Minutes of match: 90 +", extra_time)
        if elapsed_minutes <= 90 and status_description == '2nd half':
            print(f"Minutes of match: {elapsed_minutes}'")

        if status_description == 'Halftime':
            print("Minutes of match: HT")
        if elapsed_minutes > 45 and status_description == '1st half':
            extra_time = elapsed_minutes - 45
            print ("Minutes of match: 45 +", extra_time)
        if status_description == '1st half' and elapsed_minutes <= 45:
            print(f"Minutes of match: {elapsed_minutes}'")
        

        print("--------------------------------------------------")
        
    except KeyError:
        print(league, "\n", hometeam, homescore, " - ", awayscore, awayteam)
        print("Time not available")
        print("--------------------------------------------------")



    
        
        
  
    