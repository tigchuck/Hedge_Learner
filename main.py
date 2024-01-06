from DataHandler import DataHandler
from OddsMath import OddsMath

def main():
    handler = DataHandler()
    handler.collect_data(
        sport="americanfootball_nfl", 
        regions=["us","us2"], 
        bookmakers=["betmgm", "bovada", "draftkings", "fanduel", "mybookieag", "williamhill_us", "espnbet", "hardrockbet", "tipico_us", "pinnacle"],
        markets="h2h", 
        odds_format="decimal", 
        request_type="default", 
        filename="Data/Sample_API_JSON/americanfootball_nfl&us,us2&h2h&1-6-24-11-53.json"
    )    
    handler.collect_data(
        sport="americanfootball_nfl", 
        regions=["us","us2"], 
        bookmakers=["betmgm", "bovada", "draftkings", "fanduel", "mybookieag", "williamhill_us", "espnbet", "hardrockbet", "tipico_us", "pinnacle"],
        markets="spreads", 
        odds_format="decimal", 
        request_type="default", 
        filename="Data/Sample_API_JSON/americanfootball_nfl&us,us2&spreads&1-6-24-11-53.json"
    )




if __name__ == "__main__":
    main()