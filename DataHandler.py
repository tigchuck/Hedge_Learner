import json
import os
import requests
import time as t
import pandas as pd
from FileHandler import FileHandler
from Credentials import API_KEY


##################
# Requests and Manages data from SportsOdds API.
# Reads and Interprets information stored in the Data/ directory.
# This module will be utilized by the learner to retrieve necessary information.
# Manages storing information about file structure.
# Reads and Updates file structure table to know how to interpret files in Data/ directory.
# This file also stores a list of existing files within each sport allowing more easy access to this information for external modules.
##################


class DataHandler(FileHandler):
    def __init__(self, mount="Data", structure=None):
        """
        Constructor
        
        param structure: For testing purposes, is table that stores information about the structure of files.
        type structure: dict()
        param mount: The mount point for where data is stored
        type mount: str
        """
        
        super().__init__(mount=mount)
        self.__mount = mount
        self.api_key = API_KEY
        self.__init_price_dict()
        if (structure == None):
            self.__init_structure()
        else:
            self.__structure = structure


    ## PRIVATE METHODS ##
    
    def __init_price_dict(self) -> None:
        file = open(f"{self.__mount}/price_dictionary.json", "r")
        self.__price_dict = json.load(file)
        file.close()  
    
    def __init_structure(self) -> None:
        file = open(f"{self.__mount}/file_structure.json", "r")
        try:
            self.__structure = json.load(file)
        except json.decoder.JSONDecodeError:
            self.__structure = dict()
        finally:
            file.close()  
            
    def __get_structure(self, sport:str, bet_type:str):
        return self.__structure[sport]["structure"][bet_type]
    
    def __read_prices(self, sport:str, bet_type:str, home_team:str, away_team:str, data:dict):
        if (data["key"] != bet_type):
            return
        
        keys = self.__structure[sport]["structure"][bet_type][3:]
        values = dict()
        check = False
        for key in keys:
            args = self.__price_dict[key]
            if (args[1] == "Home"):
                name = home_team
            elif (args[1] == "Away"):
                name = away_team
            else:
                name = args[1]
                
            for outcome in data[args[0]]:   
                if (outcome["name"] == name):    # Make sure pulling correct team for home/away
                    values[key] = outcome[args[2]]
                    check = True
                    break
                
            if (not check):
                raise ValueError(f"{args[1]} is not a proper key.")
            
        return values
    
    
    ## PUBLIC METHODS ##
    
    def calculate_season(self, sport:str, start_time):
        if (isinstance(start_time, str)):
            start_time = pd.Timestamp(start_time)
        season = None
        for loop_season in self.list_seasons(sport):
            loop_date = pd.Timestamp(self.__structure[sport]["seasons"][loop_season])
            if ((season == None or loop_date > pd.Timestamp(self.__structure[sport]["seasons"][season])) and
                (start_time >= loop_date)):
                    season = loop_season
        return season
    
    def list_sports(self):
        return list(self.__structure.keys())
    
    def list_seasons(self, sport:str):
        return list(self.__structure[sport]["seasons"].keys())
    
    def list_bet_types(self, sport:str) -> list[str]:
        return list(self.__structure[sport]["structure"].keys())
    
    
    
    
    ## REQUEST METHODS ##
    
    def collect_data(self, sport:str=None, regions:list[str]=None, bookmakers:list[str]=None, markets:str=None, odds_format:str="decimal", request_type:str="default", **kwargs) -> None:        
        ## SEND REQUEST ##
        if (request_type == "default"):
            if (sport == None or markets == None):
                raise ValueError("sport and markets must be assigned values for default data collection.")
            elif (regions == None and bookmakers == None):
                raise ValueError("At least on of regions or bookmakers must be specified for default data collection.")
            odds_df = self.__send_request(sport, regions, bookmakers, markets, odds_format, filename=kwargs["filename"])
        elif (request_type == "historic"):
            pass
            # odds_df = self.__send_request_historic(sport, regions, markets, odds_format, kwargs["update_time"])
        elif (request_type == "local"):
            odds_df = self.__send_request_local(kwargs["filename"])
        else:
            raise ValueError(f"{request_type} is not a valid request type.")
        
        ## HANDLE REQUEST ##            
        for _, row in odds_df.iterrows():
            file_id = row["id"]
            sport = row["sport_key"]
            bet_type = markets
            home_team = row["home_team"]
            away_team = row["away_team"]
            start_time = row["commence_time"].strftime('%Y-%m-%dT%XZ')
            season = self.calculate_season(sport, start_time)

            ## OPEN/CREATE FILE ##
            if (super().file_exists(file_id, bet_type)):
                file_df = super().read_file(file_id, bet_type)
                update_number = int(file_df.iloc[-1,:]["Update"]) + 1
            elif (super().id_exists(file_id)):
                super().create_file(file_id, bet_type, self.__get_structure(sport, bet_type))
                update_number = 0
            else:
                super().create_file(file_id, bet_type, self.__get_structure(sport, bet_type), sport=sport, season=season, home_team=home_team, away_team=away_team, start_time=start_time)
                update_number = 0
                
            ## VERIFY START TIME HAS NOT CHANGED ##
            if (start_time != super().get_start_time(file_id)):
                super().set_start_time(file_id, start_time)

            ## WRITE TO FILE ##
            for item in row["bookmakers"]:
                values = self.__read_prices(sport, bet_type, home_team, away_team, item["markets"][0])
                if (values == None):
                    continue
                else:
                    values["Update"] = update_number
                    values["Time"] = item["last_update"]
                    values["Sportsbook"] = item["key"]
                    super().append_file(file_id, bet_type, *self.__get_structure(sport, bet_type), **values)
        
        
    def __send_request(self, sport:str, regions:list[str], bookmakers:list[str], markets:str, odds_format:str, filename:str=None) -> pd.DataFrame:  
        # Only send 1 market at a time. This will make copying them into files more simple.    
        response = requests.get(
            f"https://api.the-odds-api.com/v4/sports/{sport}/odds", 
            params = {
                "api_key": self.api_key, 
                "regions": ",".join(regions), 
                "bookmakers": ",".join(bookmakers), 
                "markets": markets, 
                "oddsFormat": odds_format
            }
        )
        
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
    
    
    def __send_request_historic(self, sport:str, regions:list[str], markets:list[str], odds_format:str, update_time:str) -> pd.DataFrame:
        pass
        
        
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