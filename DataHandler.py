import json
import os
import requests
import time as t
import pandas as pd

class DataHandler:
    def __init__(self):
        self.api_key = "bca37956d9d0c643fe8bca909180bb2c"
        
    
    def collect_data(self, sport = "americanfootball_nfl", regions = ["us", "us2"], markets = ["h2h"], odds_format = "decimal"):        
        ## SEND REQUEST ##
        # df = self._send_request(sport, regions, markets, odds_format, api_key = self.api_key, filename = "SampleData3.json")
        df = self._send_request_local("SampleData3.json")
        
        ## HANDLE REQUEST ##            
        for index, row in df.iterrows():
            sport = row["sport_key"]
            home = row["home_team"]
            away = row["away_team"]
            st = row["commence_time"]
            filename = DataHandler.build_filename(home, away, st, "csv")
                
            ## CONDITIONALLY CREATE SPORT DIRECTORY ##
            path = f"Data/{sport}/"
            if (not os.path.isdir(path)):
                os.mkdir(path)
                
            ## OPEN/CREATE FILE ##
            update_number = 0
            if (not os.path.isfile(path + filename)):
                file = open(path + filename, "w")
                file.write(f"Update,Time,Sportsbook,Type,{away},{home}\n")
            else:
                file = open(path + filename, "a+")
                file.seek(0, os.SEEK_SET)
                last_update_number = int(file.readlines()[-1].split(',')[0])
                update_number = last_update_number + 1
                file.seek(0, os.SEEK_END)
                
            ## WRITE TO FILE ##
            for item in row["bookmakers"]:
                book = item["key"]
                update_time = pd.to_datetime(item["last_update"]).tz_convert("us/eastern")
                bet_type = item["markets"][0]["key"]
                away_price = item["markets"][0]["outcomes"][1]["price"]
                home_price = item["markets"][0]["outcomes"][0]["price"]
                if bet_type == "h2h":
                    file.write(f"{update_number},{update_time},{book},{bet_type},{away_price},{home_price}\n")
            file.close()
            
    
    def list_sports(self):
        path = f"Data/"
        return [sport for sport in os.listdir(path) if os.path.isdir(os.path.join(path, sport))]
    
    
    def list_files(self, sport = "americanfootball_nfl"):
        path = f"Data/{sport}/"
        return os.listdir(path)
    
    
    def _send_request(self, sport, regions, markets, odds_format, filename=None):        
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
        
        
    def _send_request_local(self, request="./SampleData.json"):
        file = open(request, "r")
        odds_json = file.read()
        odds_df = pd.read_json(odds_json, orient="records")
        file.close()
        return odds_df
      
      
    @staticmethod      
    def build_filename(home, away, st, file_type):
        home = home.replace(' ', '')
        away = away.replace(' ', '')
        st = st.tz_convert("us/eastern")
        return f"{st.year}-{st.month}-{st.day}-{st.hour}-{st.minute}-{away}-{home}.{file_type}"


    
if __name__ == "__main__":
    handler = DataHandler()
    print(handler.list_sports())