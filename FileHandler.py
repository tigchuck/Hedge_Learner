import json
import os
import requests
import time as t
import pandas as pd


##################
# INFO TABLE STRUCTURE
# KEY => FILE_ID
# VALUE => DICTIONARY OF INFO
# VALUE KEYS => HOME TEAM, AWAY TEAM, START TIME, SPORT, SEASON
#
# FILE NAME STRUCTURE
# FILE_ID.csv
#
# ALL UPDATES TO ANY FILE MUST BE MADE USING THIS CLASS
##################


class FileHandler:
    def __init__(self, mount:str = "Data"):
        self.__mount = mount
        self.__read_table()
        
        
    def __read_table(self) -> None:
        file = open(f"{self.__mount}/info_table.json", "r")
        self.__table = json.load(file)
        file.close()
    
    
    def __write_table(self) -> None:
        file = open(f"{self.__mount}/info_table.json", "w")
        json_data = json.dumps(self.__table, indent=4)
        file.write(json_data)
        file.close()
        
    
    def __update_table(self, id:str, key:str, value:str) -> None:
        self.__table[file_id][key] = value
        self.__write_table()
        
        
    def read_file(self, file_id:str) -> pd.DataFrame:
        filepath = self.__get_filepath(file_id)
        return pd.read_csv(filepath)
    
    
    def append_file(self, file_id:str):
        pass
    
    
    def __create_file(self, file_id:str):
        pass
        
        
    def get_sport(self, file_id:str) -> str:
        if (file_id not in self.__table):
            raise ValueError("File ID ({file_id}) does not exist.")
        else:
            return self.__table[file_id]["sport"]
        
        
    def get_season(self, file_id:str) -> str:
        if (file_id not in self.__table):
            raise ValueError("File ID ({file_id}) does not exist.")
        else:
            return self.__table[file_id]["season"]
    
    
    def __get_filepath(file_id:str) -> str:
        sport = self.get_sport(file_id)
        season = self.get_season(file_id)
        return f"{self.__mount}/{sport}/{season}/{file_id}.csv"