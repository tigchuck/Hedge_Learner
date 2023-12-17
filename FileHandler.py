import json
import os
import requests
import time as t
import pandas as pd


##################
# INFO TABLE STRUCTURE
# KEY => FILE_ID
# VALUE => DICTIONARY OF INFO
# VALUE KEYS => HOME TEAM, AWAY TEAM, START TIME, SPORT
#
# FILE NAME STRUCTURE
# FILE_ID.csv
#
# ALL UPDATES TO ANY FILE MUST BE MADE USING THIS CLASS
##################


class FileHandler:
    def __init__(self, mount:str = "Data"):
        self.__mount = mount
        self.__init_table()
        
        
    ## PUBLIC METHODS ##
        
    def read_file(self, file_id:str) -> pd.DataFrame:
        filepath = self.__get_filepath(file_id)
        return pd.read_csv(filepath)
    
    
    def append_file(self, file_id:str, update_number:int, update_time:pd.Timestamp, sportsbook:str, bet_type:str, home:float, away:float):
        if (not self.file_exists(file_id)):
            raise ValueError(f"File ID {file_id} does not exist.")
        elif (not self.__is_valid_update_number(update_number)):
            raise ValueError(f"{update_number} is not a valid update number.")
        elif (not self.__is_valid_time(update_time)):
            raise ValueError(f"{update_time} is not a valid update time.")
        elif (not self.__is_valid_sportsbook(sportsbook)):
            raise ValueError(f"{sportsbook} is not a valid sportsbook.")
        elif (not self.__is_valid_bet_type(bet_type)):
            raise ValueError(f"{bet_type} is not a valid bet type.")
        elif (not self.__is_valid_price(home)):
            raise ValueError(f"{home} is not a valid price.")
        elif (not self.__is_valid_price(away)):
            raise ValueError(f"{away} is not a valid price.")
        else:
            filepath = self.__get_filepath(file_id)
            file = open(filepath, "a")
            file.write(f"{update_number},{update_time},{sportsbook},{bet_type},{away},{home}\n")
            file.close()
    
    
    def create_file(self, file_id:str, home:str, away:str, start_time:pd.Timestamp, sport:str):
        if (self.file_exists(file_id)):
            raise ValueError(f"File already exists for {file_id}.")
        elif(not self.directory_exists(sport)):
            self.create_directory(sport)
        self.__update_table(file_id, "home_team", home)
        self.__update_table(file_id, "away_team", away)
        self.__update_table(file_id, "start_time", start_time.strftime("%Y-%m-%d %X"))
        self.__update_table(file_id, "sport", sport)
        filepath = self.__get_filepath(file_id)
        file = open(filepath, "w")
        file.write(f"Update,Time,Sportsbook,Type,{away},{home}\n")
        file.close()
        

    def get_file_ids(self, sport:str):
        if (not self.__is_valid_sport(sport)):
            raise ValueError(f"{sport} is not a valid sport.")
        elif(not self.directory_exists(sport)):
            raise ValueError(f"{sport} is not a valid directory.")
        else:
            path = f"{self.__mount}/{sport}/"
            return [filename.split(".csv")[0] for filename in os.listdir(path) if os.path.isfile(os.path.join(path, filename))]
                
    
    def file_exists(self, file_id:str) -> bool:
        return file_id in self.__table
    
    
    def directory_exists(self, directory:str) -> bool:
        return os.path.isdir(f"{self.__mount}/{directory}/")
    
    
    def create_directory(self, directory:str) -> None:
        os.mkdir(f"{self.__mount}/{directory}/")
    
        
    def get_sport(self, file_id:str) -> str:
        if (not self.file_exists(file_id)):
            raise ValueError("File ID ({file_id}) does not exist.")
        else:
            return self.__read_table(file_id, "sport")
        
        
    def set_sport(self, file_id:str, sport:str) -> None:
        if (not self.file_exists(file_id)):
            raise ValueError("File ID ({file_id}) does not exist.")
        elif (not self.__is_valid_sport(sport)):
            raise ValueError(f"{sport} is not a valid sport.")
        else:
            self.__update_table(file_id, "sport", sport)
        
        
    def get_home_team(self, file_id:str) -> str:
        if (not self.file_exists(file_id)):
            raise ValueError("File ID ({file_id}) does not exist.")
        else:
            return self.__read_table(file_id, "home_team")
        
        
    def set_home_team(self, file_id:str, team:str) -> None:
        if (not self.file_exists(file_id)):
            raise ValueError("File ID ({file_id}) does not exist.")
        elif (not self.__is_valid_team(team)):
            raise ValueError(f"{team} is not a valid team.")
        else:
            self.__update_table(file_id, "home_team", team)
        
        
    def get_away_team(self, file_id:str) -> str:
        if (not self.file_exists(file_id)):
            raise ValueError("File ID ({file_id}) does not exist.")
        else:
            return self.__read_table(file_id, "away_team")
        
        
    def set_away_team(self, file_id:str, team:str) -> None:
        if (not self.file_exists(file_id)):
            raise ValueError("File ID ({file_id}) does not exist.")
        elif (not self.__is_valid_team(team)):
            raise ValueError(f"{team} is not a valid team.")
        else:
            self.__update_table(file_id, "away_team", team)
        
        
    def get_start_time(self, file_id:str) -> str:
        if (not self.file_exists(file_id)):
            raise ValueError("File ID ({file_id}) does not exist.")
        else:
            start_time = self.__read_table(file_id, "start_time")
            return pd.Timestamp(start_time)
        
        
    def set_start_time(self, file_id:str, start_time:pd.Timestamp) -> None:
        if (not self.file_exists(file_id)):
            raise ValueError("File ID ({file_id}) does not exist.")
        elif (not self.__is_valid_time(start_time)):
            raise ValueError(f"{start_time} is not a valid start time.")
        else:
            self.__update_table(file_id, "start_time", start_time.strftime("%Y-%m-%d %X"))
        
        
    ## PRIVATE METHODS ##
    
    def __init_table(self) -> None:
        file = open(f"{self.__mount}/info_table.json", "r")
        try:
            self.__table = json.load(file)
        except json.decoder.JSONDecodeError:
            self.__table = dict()
        finally:
            file.close()
        
        
    def __read_table(self, file_id:str, key:str) -> None:
        if (not self.file_exists(file_id)):
            raise ValueError("File ID {file_id} does not exist.")
        else:
            return self.__table[file_id][key]
    
    
    def __write_table(self) -> None:
        file = open(f"{self.__mount}/info_table.json", "w")
        json_data = json.dumps(self.__table, indent=4)
        file.write(json_data)
        file.close()
        
    
    def __update_table(self, file_id:str, key:str, value:str) -> None:
        if (not self.file_exists(file_id)):
            if (self.__is_valid_id(file_id)):
                self.__table[file_id] = dict()
            else:
                raise ValueError(f"{file_id} is not a valid file ID.")
        self.__table[file_id][key] = value
        self.__write_table()
    
    
    def __get_filepath(self, file_id:str) -> str:
        sport = self.get_sport(file_id)
        return f"{self.__mount}/{sport}/{file_id}.csv"
    
    
    def __is_valid_id(self, file_id:str) -> bool:
        return isinstance(file_id, str)
    
    
    def __is_valid_sport(self, sport:str) -> bool:
        return isinstance(sport, str)
    
    
    def __is_valid_time(self, update_time:pd.Timestamp) -> bool:
        return isinstance(update_time, pd.Timestamp)
    
    
    def __is_valid_team(self, team:str) -> bool:
        return isinstance(team, str)
    
    
    def __is_valid_update_number(self, num:int) -> bool:
        return isinstance(num, int) and num >= 0
    
    
    def __is_valid_sportsbook(self, sportsbook:str) -> bool:
        return isinstance(sportsbook, str)
    
    
    def __is_valid_bet_type(self, bet_type:str) -> bool:
        return isinstance(bet_type, str) and bet_type in ["h2h", "spreads", "totals"]
    
    
    def __is_valid_price(self, price:str) -> bool:
        return isinstance(price, float) and price >= 1