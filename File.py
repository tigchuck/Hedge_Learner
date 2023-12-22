class File:
    def __init__(self, file_id, sport, season, start_time, home_team, away_team):
        self.file_id = file_id
        self.sport = sport
        self.season = season
        self.start_time = start_time
        self.home_team = home_team
        self.away_team = away_team
        
    def get_file_path(self, mount="Data", bet_type="h2h"):
        return f"{mount}/{self.sport}/{self.season}/{bet_type}/{self.file_id}.csv"
        
    def get_file_id(self):
        return self.file_id
    
    def get_sport(self):
        return self.sport
    
    def get_season(self):
        return self.season
    
    def get_start_time(self):
        return self.start_time
    
    def get_home_team(self):
        return self.home_team
    
    def get_away_team(self):
        return self.away_team
    
    def set_file_id(self, file_id):
        self.file_id = file_id
        
    def set_sport(self, sport):
        self.sport = sport
        
    def set_season(self, season):
        self.season = season
        
    def set_start_time(self, start_time):
        self.start_time = start_time
        
    def set_home_team(self, home_team):
        self.home_team = home_team
        
    def set_away_team(self, away_team):
        self.away_team = away_team