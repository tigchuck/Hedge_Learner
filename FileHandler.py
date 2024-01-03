import json
import os
import requests
import time as t
import pandas as pd


##################
# Manages files in the Data/ directory.
# Reads, Creates, and Appends files.
# Manages table storing file information.
# Reads, Updates, Modifies, and Writes to storage this table.
##################


class FileHandler:
    def __init__(self, table = None, mount = "Data"):
        """
        Constructor
        
        param table: For testing purposes, is table that stores information about each file.
        type table: dict()
        param mount: The mount point for where data is stored
        type mount: str
        """
        self.__mount = mount
        
        if (table == None):
            self.__init_table()
        else:
            self.__table = table
        
    
    
    ## PUBLIC METHODS ##  
          
    def read_file(self, file_id:str, bet_type:str) -> pd.DataFrame:
        """
        Read file as Pandas DataFrame.
        
        param file_id: ID of file to be read
        type file_id: str
        param bet_type: Type of bet file to read
        type bet_type: str
        return: File data
        rtype: Pandas.DataFrame
        """
        
        if (not self.file_exists(file_id)):
            raise ValueError("File ID ({file_id}) does not exist.")
        filepath = self.__get_filepath(file_id, bet_type)
        return pd.read_csv(filepath)
       
       
    def append_file(self, file_id:str, bet_type:str, *args, **kwargs):
        """
        Adds new line of data to file.
        Args and Kwargs because different sports and/or bet types require different info.
        
        param file_id: ID of file to be read
        type file_id: str
        param bet_type: Type of bet file to read
        type bet_type: str
        param args: names of all the kwargs in the order they should be read into the file
        type args: list of str
        param kwargs: values pertaining to each of the arguments necessary for the file
        type kwargs: dictionary(str, str)
        """
        
        if (not self.file_exists(file_id)):
            raise ValueError(f"File ID {file_id} does not exist.")
        filepath = self.__get_filepath(file_id, bet_type)
        file = open(filepath, "a")
        
        arr = []
        for arg in args:
            arr.append(kwargs[arg])
        line = ','.join(str(obj) for obj in arr)
        line += "\n"
        file.write(line)
        file.close()
        
          
    def create_file(self, file_id:str, sport:str, season:str, bet_type:str, home_team:str, away_team:str, start_time:str, columns:list[str]):
        if (self.file_exists(file_id)):
            raise ValueError(f"File already exists for {file_id}.")
        
        if (not self.directory_exists(sport)):
            self.create_directory(sport)
        if (not self.directory_exists(f"{sport}/{season}")):
            self.create_directory(f"{sport}/{season}")
        if (not self.directory_exists(f"{sport}/{season}/{bet_type}")):
            self.create_directory(f"{sport}/{season}/{bet_type}")
          
        self.__update_table(file_id, "sport", "season", "home_team", "away_team", "start_time", sport=sport, season=season, home_team=home_team, away_team=away_team, start_time=start_time)
        filepath = self.__get_filepath(file_id, bet_type)
        file = open(filepath, "w")
        file.write(f"{','.join(columns)}\n")
        file.close()
        
        
    def file_exists(self, file_id:str) -> bool:
        return file_id in self.__table
    
    
    def directory_exists(self, directory:str) -> bool:
        return os.path.isdir(f"{self.__mount}/{directory}/")
    
    
    def create_directory(self, directory:str) -> None:
        os.mkdir(f"{self.__mount}/{directory}/")
        


    ## GETTERS AND SETTERS ##
    
    def get_sport(self, file_id:str) -> str:
        if (not self.file_exists(file_id)):
            raise ValueError("File ID ({file_id}) does not exist.")
        else:
            return self.__read_table(file_id, "sport")
       
           
    def set_sport(self, file_id:str, sport:str) -> None:
        if (not self.file_exists(file_id)):
            raise ValueError("File ID ({file_id}) does not exist.")
        else:
            self.__update_table(file_id, "sport", sport=sport)
            
        
    def get_season(self, file_id:str) -> str:
        if (not self.file_exists(file_id)):
            raise ValueError("File ID ({file_id}) does not exist.")
        else:
            return self.__read_table(file_id, "season")
        
        
    def set_season(self, file_id:str, season:str) -> None:
        if (not self.file_exists(file_id)):
            raise ValueError("File ID ({file_id}) does not exist.")
        else:
            self.__update_table(file_id, "season", season=season)
            
        
    def get_home_team(self, file_id:str) -> str:
        if (not self.file_exists(file_id)):
            raise ValueError("File ID ({file_id}) does not exist.")
        else:
            return self.__read_table(file_id, "home_team")
        
    
    def set_home_team(self, file_id:str, home_team:str) -> None:
        if (not self.file_exists(file_id)):
            raise ValueError("File ID ({file_id}) does not exist.")
        else:
            self.__update_table(file_id, "home_team", home_team=home_team)
            
    
    def get_away_team(self, file_id:str) -> str:
        if (not self.file_exists(file_id)):
            raise ValueError("File ID ({file_id}) does not exist.")
        else:
            return self.__read_table(file_id, "away_team")

  
    def set_away_team(self, file_id:str, away_team:str) -> None:
        if (not self.file_exists(file_id)):
            raise ValueError("File ID ({file_id}) does not exist.")
        else:
            self.__update_table(file_id, "away_team", away_team=away_team)


    def get_start_time(self, file_id:str) -> str:
        if (not self.file_exists(file_id)):
            raise ValueError("File ID ({file_id}) does not exist.")
        else:
            start_time = self.__read_table(file_id, "start_time")
            return pd.Timestamp(start_time)


    def set_start_time(self, file_id:str, start_time:str) -> None:
        if (not self.file_exists(file_id)):
            raise ValueError("File ID ({file_id}) does not exist.")
        else:
            self.__update_table(file_id, "start_time", start_time=start_time)
            
    
    # NEED UPDATE
    def get_file_ids(self, sport:str, season:str, bet_type:str):
        if (not self.__is_valid_sport(sport)):
            raise ValueError(f"{sport} is not a valid sport.")
        elif(not self.directory_exists(sport)):
            raise ValueError(f"{sport} is not a valid directory.")
        else:
            path = f"{self.__mount}/{sport}/"
            return [filename.split(".csv")[0] for filename in os.listdir(path) if os.path.isfile(os.path.join(path, filename))]
    
        
            
    ##  PRIVATE METHODS ##    
    
    def __get_filepath(self, file_id:str, bet_type:str) -> str:
        sport = self.get_sport(file_id)
        season = self.get_season(file_id)
        return f"{self.__mount}/{sport}/{season}/{bet_type}/{file_id}.csv"
    
    
    def __init_table(self) -> None:
        """
        Initialize table containing information about each file.
        """
        
        file = open(f"{self.__mount}/info_table.json", "r")
        try:
            self.__table = json.load(file)
        except json.decoder.JSONDecodeError:
            self.__table = dict()
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
        
        
    def __update_table(self, file_id:str, *args, **kwargs) -> None:
        if (not self.file_exists(file_id)):
            self.__table[file_id] = dict()
            
        for arg in args:
            self.__table[file_id][arg] = kwargs[arg]
        self.__write_table()
            