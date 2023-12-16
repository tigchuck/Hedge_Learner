import json
import os
import requests
import time as t
import pandas as pd
from FileHandler import FileHandler

class DataHandler(FileHandler):
    def __init__(self):
        super().__init__()
        self.api_key = "bca37956d9d0c643fe8bca909180bb2c"
        
    
    def collect_data(self, sport:str = "americanfootball_nfl", regions:list[str] = ["us", "us2"], markets:list[str] = ["h2h"], odds_format:str = "decimal") -> None:        
        ## SEND REQUEST ##
        # odds_df = self.__send_request(sport, regions, markets, odds_format, filename = "SampleData4.json")
        odds_df = self.__send_request_local("SampleData4.json")
        
        ## HANDLE REQUEST ##            
        for _, row in odds_df.iterrows():
            file_id = row["id"]
            sport = row["sport_key"]
            home_team = row["home_team"]
            away_team = row["away_team"]
            start_time = row["commence_time"]
                
            ## OPEN/CREATE FILE ##
            if (super().file_exists(file_id)):
                file_df = super().read_file(file_id)
                update_number = int(file_df.iloc[-1,:]["Update"]) + 1
            else:
                super().create_file(file_id, home_team, away_team, start_time, sport)
                update_number = 0

            ## WRITE TO FILE ##
            for item in row["bookmakers"]:
                sportsbook = item["key"]
                update_time = pd.to_datetime(item["last_update"]).tz_convert("us/eastern")
                bet_type = item["markets"][0]["key"]
                away_price = item["markets"][0]["outcomes"][1]["price"]
                home_price = item["markets"][0]["outcomes"][0]["price"]
                super().append_file(file_id, update_number, update_time, sportsbook, bet_type, home_price, away_price)
        
        
    def __send_request(self, sport:str, regions:list[str], markets:list[str], odds_format:str, filename:str=None) -> pd.DataFrame:        
        response = requests.get(f"https://api.the-odds-api.com/v4/sports/{sport}/odds", params = {"api_key": self.api_key, "regions": ','.join(regions), "markets": ','.join(markets), "oddsFormat": odds_format})
        if response.status_code != 200:
            print(f'Failed to get odds: status_code {response.status_code}, response body {response.text}')
        else:
            odds_json = response.json()
            
            print('Number of events:', len(odds_json))
            # print(odds_json)
            
            if filename != None:
                file = open(filename, "w")
                json.dump(odds_json, file)
                file.close()

            # Check the usage quota
            print('Remaining requests', response.headers['x-requests-remaining'])
            print('Used requests', response.headers['x-requests-used'])
            
            odds_df = pd.read_json(json.dumps(odds_json), orient="records")
            return odds_df
        
        
    def __send_request_local(self, request:str="./SampleData.json") -> pd.DataFrame:
        try:
            file = open(request, "r")
        except FileNotFoundError:
            print(f"File ({request}) not found.")
        else:
            odds_json = file.read()
            odds_df = pd.read_json(odds_json, orient="records")
            file.close()
            return odds_df