import os
import json

class TestInfoTable:
    def __init__(self, verbose=False):
        self.verbose = verbose
        
    def run(self):
        passed, tests = 0, 2
        if (self.test_files()):
            passed += 1
        else:
            print("Failed test_files. A file likely exists in the data directory, but is not present in the Info Table.")
            
        if (self.test_info_table()):
            passed += 1
        else:
            print("Failed test_info_table. A File ID is likely present in the Info Table, but not in the data directory.")
            
        print(f"TestInfoTable: {passed}/{tests} tests passed.")
        

    def test_files(self):
        if self.verbose: print("hello")
        file = open(f"data/info_table.json", "r")
        table = json.load(file)   
        file.close()
        
        error_free = True
        for sport in ["soccer_epl", "americanfootball_nfl"]:
            seasons = os.listdir(f"data/{sport}")
            for season in seasons:
                bet_types = os.listdir(f"data/{sport}/{season}")
                for bet_type in bet_types:
                    file_ids = os.listdir(f"data/{sport}/{season}/{bet_type}")
                    for file_id in file_ids:
                        file_id = file_id.split(".")[0]
                        if file_id not in table:
                            if self.verbose: print(f"File ID ({file_id}) not in table, but in {sport}/{season}/{bet_type}")
                            error_free = False
                            continue
                        if table[file_id]["sport"] != sport:
                            error_free = False
                            if self.verbose: print(f"Sport Error ({file_id}):\tTable: {table[file_id]['sport']}\tFile Location: {sport}")
                        if table[file_id]["season"] != season:
                            error_free = False
                            if self.verbose: print(f"Season Error ({file_id}):\tTable: {table[file_id]['season']}\tFile Location: {season}")
                        if bet_type not in table[file_id]["bet_type"]:
                            error_free = False
                            if self.verbose: print(f"Bet Type Error ({file_id}):\tTable: {table[file_id]['bet_type']}\tFile Location: {bet_type}")
                            
        return error_free

    
    def test_info_table(self):
        file = open(f"data/info_table.json", "r")
        table = json.load(file)   
        file.close()
        
        error_free = True
        for key in table:
            sport = table[key]["sport"]
            season = table[key]["season"]
            bet_types = table[key]["bet_type"]
            for bet_type in bet_types:
                if not os.path.isfile(f"data/{sport}/{season}/{bet_type}/{key}.csv"):
                    error_free = False
                    if self.verbose: print("Table Error: File ID {key} is in table, but not located in data/{sport}/{season}/{bet_type}/")
                    
        return error_free
    