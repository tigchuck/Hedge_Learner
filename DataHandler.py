import json
import os
import time as t
import pandas as pd

class DataHandler:
    def __init__(self):
        self.api_key = "bca37956d9d0c643fe8bca909180bb2c"
        self.sport = "americanfootball_nfl"
        self.regions = ["us", "us2"]
        self.markets = ["h2h"]
        
    
    def collect_data(self, request="request"):
        ## BUILD REQUEST ##
        api_request = DataHandler.build_request(self.api_key, self.sport, self.regions, self.markets)
        
        ## SEND REQUEST ##
        df = DataHandler.send_request("./SampleData.json")
        
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
                file.write(f"{update_number},{update_time},{book},{bet_type},{away_price},{home_price}\n")
            file.close()
            
    
    @staticmethod
    def build_request(api_key, sport, regions, markets):
        request = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={api_key}&regions={','.join(regions)}&markets={','.join(markets)}"
        return request
    
    @staticmethod
    def send_request(request="./SampleData.json"):
        ## SEND REQUEST ##
        df = pd.read_json(request)
        return df
      
    @staticmethod      
    def build_filename(home, away, st, file_type):
        home = home.replace(' ', '')
        away = away.replace(' ', '')
        st = st.tz_convert("us/eastern")
        return f"{st.year}-{st.month}-{st.day}-{st.hour}-{st.minute}-{away}-{home}.{file_type}"
    
    
if __name__ == "__main__":
    handler = DataHandler()
    handler.collect_data()