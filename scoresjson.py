import json
from datetime import datetime
import math
from pytz import timezone    
import time

with open('scores.json') as f:
    jsondata = json.load(f)

league = (jsondata['events'][0]['tournament']['name'])
hometeam = (jsondata['events'][0]['homeTeam']['name'])
awayteam = (jsondata['events'][0]['awayTeam']['name'])


homescore  = (jsondata['events'][0]['homeScore']['current'])
awayscore  = (jsondata['events'][0]['awayScore']['current'])

def time_in_minutes(start_time, current_time):
    start_time = start_time.replace(tzinfo=current_time.tzinfo)
    hour_diff = (current_time - start_time).total_seconds() / 3600
    minutes_diff = hour_diff * 60
    return minutes_diff





for game in jsondata['events']:
    league = game['tournament']['name']
    hometeam = game['homeTeam']['name']
    awayteam = game['awayTeam']['name']
    homescore  = game['homeScore']['current']
    awayscore  = game['awayScore']['current']

    game_start_minutes = game['time']['currentPeriodStartTimestamp']
    game_start_time = datetime.utcfromtimestamp(game_start_minutes)
    current_uk_time = datetime.now(timezone('Europe/London'))

    time_difference = time_in_minutes(game_start_time, current_uk_time)

    
 

    print(league, "\n", hometeam, homescore, " - ", awayscore, awayteam)
    if time_difference >= 105:
        print("Match Minutes: FT")
    elif time_difference >= 47 and time_difference <= 62:
        print("Match Minutes: HT")
    if time_difference >= 62 and time_difference <= 105:
        print("Match Minutes: ", time_difference - 15)
    

    print("--------------------------------------------------")
   
 
    
