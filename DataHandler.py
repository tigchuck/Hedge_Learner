import json
import os
import requests
import time as t
import pandas as pd

class DataHandler:
    def __init__(self):
        self.api_key = "bca37956d9d0c643fe8bca909180bb2c"
        
    
    def collect_data(self, sport:str = "americanfootball_nfl", regions:list[str] = ["us", "us2"], markets:list[str] = ["h2h"], odds_format:str = "decimal") -> None:        
        ## SEND REQUEST ##
        # df = self._send_request(sport, regions, markets, odds_format, filename = "SampleData4.json")
        df = self._send_request_local("SampleData4.json")
        
        ## HANDLE REQUEST ##            
        for _, row in df.iterrows():
            sport = row["sport_key"]
            home_team = row["home_team"]
            away_team = row["away_team"]
            st = row["commence_time"]
            filename = DataHandler.build_filename(home_team, away_team, st, "csv")
                
            ## CONDITIONALLY CREATE SPORT DIRECTORY ##
            path = f"Data/{sport}/"
            if (not os.path.isdir(path)):
                os.mkdir(path)
                
            ## OPEN/CREATE FILE ##
            update_number = 0
            if (not os.path.isfile(path + filename)):
                file = open(path + filename, "w")
                file.write(f"Update,Time,Sportsbook,Type,{away_team},{home_team}\n")
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
            
          
    def get_best_odds(self, **kwargs) -> pd.DataFrame:
        if ("odds" not in kwargs):
            odds_df = self.get_data(**kwargs)
        else:
            if (not isinstance(kwargs["odds"], pd.DataFrame)):
                raise ValueError("Odds argument is not pd.DataFrame.")
            odds_df = kwargs["odds"]
            
        home_team = odds_df.columns[5]  # COULD CHANGE IF STRUCTURE OF INFO CHANGES
        away_team = odds_df.columns[4]  # COULD CHANGE IF STRUCTURE OF INFO CHANGES
        best_odds_df = pd.DataFrame(columns=odds_df.columns)
        index = 0
        update_time = 0
        sportsbooks = dict()
        bet_type = ""
        home_odds = 0
        away_odds = 0
        for _, row in odds_df.iterrows():
            if (row["Update"] != index):
                best_odds_df.loc[len(best_odds_df)] = [index, update_time, sportsbooks, bet_type, home_odds, away_odds]
                index += 1
                update_time = 0
                sportsbooks = dict()
                bet_type = ""
                home_odds = 0
                away_odds = 0
            
            if (row[away_team] > away_odds):
                away_odds = row[away_team]
                update_time = row["Time"]
                sportsbooks[0] = row["Sportsbook"]
                bet_type = row["Type"]
                
            if (row[home_team] > home_odds):
                home_odds = row[home_team]
                update_time = row["Time"]
                sportsbooks[1] = row["Sportsbook"]
                bet_type = row["Type"]
                
        best_odds_df.loc[len(best_odds_df)] = [index, update_time, sportsbooks, bet_type, home_odds, away_odds] # ADD LAST ROW
        return best_odds_df
    
    
    def get_data(self, **kwargs) -> pd.DataFrame:
        ## NEED TO DO CHECKS IF READ_CSV FAILS ##
        if ("path" in kwargs):
            return pd.read_csv(kwargs["path"])
        elif ("sport" in kwargs):
            if ("filename" in kwargs):
                return self._get_data_with_filename(kwargs["filename"], kwargs["sport"])
            elif ("home" in kwargs and "away" in kwargs and "start_time" in kwargs):
                return self.get_data_with_args(kwargs["home"], kwargs["away"], kwargs["start_time"])
        else:
            raise ValueError("Arguments did not correspond to existing file so data could not be retrieved.")
        
    
    def list_sports(self) -> list[str]:
        path = f"Data/"
        return [sport for sport in os.listdir(path) if os.path.isdir(os.path.join(path, sport))]
    
    
    def list_files(self, sport:str = "americanfootball_nfl") -> list[str]:
        path = f"Data/{sport}/"
        return os.listdir(path)
    
    
    def _get_data_with_filename(self, filename:str, sport:str) -> pd.DataFrame:
        path = f"Data/{sport}/{filename}"
        return pd.read_csv(path)
       
        
    def _get_data_with_args(self, home:str, away:str, st:pd.Series.dt, sport:str) -> pd.DataFrame:
        filename = DataHandler.build_filename(home, away, st, "csv")
        return self._get_data_with_filename(filename, sport)
        
        
    def _send_request(self, sport:str, regions:list[str], markets:list[str], odds_format:str, filename:str=None) -> pd.DataFrame:        
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
        
        
    def _send_request_local(self, request:str="./SampleData.json") -> pd.DataFrame:
        try:
            file = open(request, "r")
        except FileNotFoundError:
            print(f"File ({request}) not found.")
        else:
            odds_json = file.read()
            odds_df = pd.read_json(odds_json, orient="records")
            file.close()
            return odds_df
      
      



    
if __name__ == "__main__":
    handler = DataHandler()
    print(handler.list_sports())