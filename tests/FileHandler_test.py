import sys
import os
import json
import pandas as pd
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from FileHandler import FileHandler

def test_init_table(test_dictionary):
	file = open(f"tests/Data_test/info_table.json", "w")
	json_data = json.dumps(test_dictionary, indent=4)
	file.write(json_data)
	file.close()
	
	handler = FileHandler(mount="tests/Data_test")
	return test_dictionary == handler._FileHandler__table

def test_create_file():
    handler = FileHandler(mount="tests/Data_test")
    handler.create_file("b", "soccer", "2023-2024", "h2h", "Everton", "Liverpool", pd.Timestamp("12-21-23 08:00:00"), ["Update", "Time", "Sportsbook", "Home_Odds", "Away_Odds", "Draw_Odds"]) 
    print(handler._FileHandler__table)
    
def test_append_file():
    handler = FileHandler(mount="tests/Data_test")
    handler.append_file("b", "h2h", "Update", "Time", "Sportsbook", "Home_Odds", "Away_Odds", "Draw_Odds", Update=0, Time="12-20-23 08:00:00", Sportsbook="draftkings", Home_Odds=2.1, Away_Odds=1.5, Draw_Odds=1.7)
    odds_df = handler.read_file("b", "h2h")
    print(odds_df)
    
if __name__ == "__main__":
    test_dict = {"a": {"sport": "football"}}
    
    if (not test_init_table(test_dict)):
        print("init_table test failed.")
        
    test_create_file()
    test_append_file()



        
        
