from DataHandler import DataHandler
from OddsMath import OddsMath

def main():
    handler = DataHandler()
    handler.collect_data(sport="americanfootball_nfl", regions=["us","us2"], markets="h2h", odds_format="decimal", request_type="default", filename="Data/Sample_API_JSON/americanfootball_nfl&us,us2&h2h&1-5-24-6-00.json")    
    handler.collect_data(sport="americanfootball_nfl", regions=["us","us2"], markets="spreads", odds_format="decimal", request_type="default", filename="Data/Sample_API_JSON/americanfootball_nfl&us,us2&spreads&1-5-24-6-00.json")




if __name__ == "__main__":
    main()