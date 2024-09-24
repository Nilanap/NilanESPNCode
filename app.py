from flask import Flask, render_template, jsonify
import requests
import json
import math
from datetime import datetime, timedelta
from pytz import timezone

app = Flask(__name__)


def fetch_baseball():
    import requests

    url = 'https://api.sofascore.com/api/v1/sport/baseball/events/live'

    payload = ""
    headers = {
        "authority": "www.sofascore.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "_gcl_au=1.1.1667870649.1692208788; ... (your cookie data) ... ",
        "dnt": "1",
        "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    response = requests.request("GET", url, data=payload, headers=headers)

    jsondata = json.loads(response.text)



    for game in jsondata['events']:
            
        league = game['tournament']['name']
        hometeam = game['homeTeam']['name']
        awayteam = game['awayTeam']['name']
        homescore = game['homeScore']['current']
        awayscore = game['awayScore']['current']
        status = game['des']
        print(league, "\n", hometeam, homescore, " - ", awayscore, awayteam, "--------------------", "\n")

        





def fetch_live_scores():
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

    
        
    scores = []
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

            score_info = ""



            # Fix Extra time.
            if status_description == '2nd half':
                elapsed_minutes += 45
            if elapsed_minutes > 90:
                score_info = f"{league}\n{hometeam} {homescore} - {awayscore} {awayteam}\nStatus: {status_description}\n{'Minutes in match: 90+'}'\n"
            if elapsed_minutes <= 90 and status_description == '2nd half':
                score_info = f"{league}\n{hometeam} {homescore} - {awayscore} {awayteam}\nStatus: {status_description}\nMinutes in match: {elapsed_minutes}'\n"


            if status_description == 'Halftime':
                score_info = f"{league}\n{hometeam} {homescore} - {awayscore} {awayteam}\nStatus: {status_description}\nMinutes in match: HT\n"
                

            if elapsed_minutes > 45 and status_description == '1st half':
                score_info = f"{league}\n{hometeam} {homescore} - {awayscore} {awayteam}\nStatus: {status_description}\n{'Minutes in match: 45+'}'\n"
            if status_description == '1st half' and elapsed_minutes <= 45:
                score_info = f"{league}\n{hometeam} {homescore} - {awayscore} {awayteam}\nStatus: {status_description}\nMinutes in match: {elapsed_minutes}'\n"
            
            scores.append(score_info)  # Add score information to the list

        except KeyError:
            score_info = f"{league}\n{hometeam} - {awayscore} {awayteam}\nTime not available\n"
            scores.append(score_info)  # Add score information to the list

    return scores

def fetch_epl_scores():

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
    prem_scores = []

    def calculate_elapsed_minutes(start_time, current_time):

        start_time_local = start_time.astimezone(timezone('Africa/Bamako'))
        current_time_local = current_time.astimezone(timezone('Africa/Bamako'))
        elapsed_time = current_time_local - start_time_local
        elapsed_minutes = elapsed_time.total_seconds() / 60
        
            
        return math.ceil(elapsed_minutes)

    for game in jsondata['events']:   

        league = game['tournament']['name']
        country = game['tournament']['category']['name']
        if league == 'Premier League' and country == 'England':
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

                score_info = ""


                # Fix Extra time.
                if status_description == '2nd half':
                    elapsed_minutes += 45
                if elapsed_minutes > 90:
                    score_info = f"{league}\n{hometeam} {homescore} - {awayscore} {awayteam}\nStatus: {status_description}\n{'Minutes in match: 90+'}'\n"
                if elapsed_minutes <= 90 and status_description == '2nd half':
                    score_info = f"{league}\n{hometeam} {homescore} - {awayscore} {awayteam}\nStatus: {status_description}\nMinutes in match: {elapsed_minutes}'\n"


                if status_description == 'Halftime':
                    score_info = f"{league}\n{hometeam} {homescore} - {awayscore} {awayteam}\nStatus: {status_description}\nMinutes in match: HT\n"
                    

                if elapsed_minutes > 45 and status_description == '1st half':
                    score_info = f"{league}\n{hometeam} {homescore} - {awayscore} {awayteam}\nStatus: {status_description}\n{'Minutes in match: 45+'}'\n"
                if status_description == '1st half' and elapsed_minutes <= 45:
                    score_info = f"{league}\n{hometeam} {homescore} - {awayscore} {awayteam}\nStatus: {status_description}\nMinutes in match: {elapsed_minutes}'\n"
                
                prem_scores.append(score_info)  # Add score information to the list

            except KeyError:
                score_info = f"{league}\n{hometeam} - {awayscore} {awayteam}\nTime not available\n"
                prem_scores.append(score_info)  # Add score information to the list

    return prem_scores
         
def fetch_ucl_scores():

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
    ucl_scores = []

    def calculate_elapsed_minutes(start_time, current_time):

        start_time_local = start_time.astimezone(timezone('Africa/Bamako'))
        current_time_local = current_time.astimezone(timezone('Africa/Bamako'))
        elapsed_time = current_time_local - start_time_local
        elapsed_minutes = elapsed_time.total_seconds() / 60
        
            
        return math.ceil(elapsed_minutes)

    for game in jsondata['events']:   

        league = game['tournament']['name']
        if league == 'UEFA Champions League' or league == 'UEFA Champions League, Playoff Round':
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

                score_info = ""


                # Fix Extra time.
                if status_description == '2nd half':
                    elapsed_minutes += 45
                if elapsed_minutes > 90:
                    score_info = f"{league}\n{hometeam} {homescore} - {awayscore} {awayteam}\nStatus: {status_description}\n{'Minutes in match: 90+'}'\n"
                if elapsed_minutes <= 90 and status_description == '2nd half':
                    score_info = f"{league}\n{hometeam} {homescore} - {awayscore} {awayteam}\nStatus: {status_description}\nMinutes in match: {elapsed_minutes}'\n"


                if status_description == 'Halftime':
                    score_info = f"{league}\n{hometeam} {homescore} - {awayscore} {awayteam}\nStatus: {status_description}\nMinutes in match: HT\n"
                    

                if elapsed_minutes > 45 and status_description == '1st half':
                    score_info = f"{league}\n{hometeam} {homescore} - {awayscore} {awayteam}\nStatus: {status_description}\n{'Minutes in match: 45+'}'\n"
                if status_description == '1st half' and elapsed_minutes <= 45:
                    score_info = f"{league}\n{hometeam} {homescore} - {awayscore} {awayteam}\nStatus: {status_description}\nMinutes in match: {elapsed_minutes}'\n"
                
                ucl_scores.append(score_info)  # Add score information to the list

            except KeyError:
                score_info = f"{league}\n{hometeam} - {awayscore} {awayteam}\nTime not available\n"
                ucl_scores.append(score_info)  # Add score information to the list

    return ucl_scores



@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html', scores=None)

@app.route("/templates/all_scores.html")
def all_scores():
    return render_template('all_scores.html')

@app.route("/templates/epl_scores.html")
def epl_scores():
    return render_template('epl_scores.html')

@app.route("/templates/ucl_scores.html")
def ucl_scores():
    return render_template('ucl_scores.html')

@app.route("/get_scores", methods=['POST'])
def get_scores():
    scores1 = fetch_live_scores()
    return jsonify(scores1=scores1)

@app.route("/get_eplscores", methods=['POST'])
def get_eplscores():
    premscores = fetch_epl_scores()  
    return jsonify(premscores=premscores)

@app.route("/get_uclscores", methods=['POST'])
def get_uclscores():
    uclscores = fetch_ucl_scores()  
    return jsonify(uclscores=uclscores)

if __name__ == '__main__':
    app.run(debug=True, port=5555)

