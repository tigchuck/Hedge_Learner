from DataHandler import DataHandler

def main():
    data_handler = DataHandler()
    # file_handler = FileHandler()
    # file_handler.get_data(file_ids=["a50417b93fb8ac1e9653946bb4850eb4"], bet_type="h2h", before_commence=True)
    timestamps=[]
    data_handler.collect_data(
        sport="soccer_epl", 
        regions=["uk"],
        markets="h2h",
        odds_format="decimal",
        request_type="historic",
        date="2021-10-30T00:00:00Z",
        filename="Data/Sample_API_JSON/soccer_epl_sample_historical_request.json",
        timestamps=timestamps
    )
    print(timestamps) 
    # data_handler.collect_data(
    #     sport="americanfootball_nfl", 
    #     regions=["us","us2"], 
    #     bookmakers=["betmgm", "bovada", "draftkings", "fanduel", "mybookieag", "williamhill_us", "espnbet", "hardrockbet", "tipico_us", "pinnacle"],
    #     markets="spreads", 
    #     odds_format="decimal", 
    #     request_type="default", 
    #     filename="Data/Sample_API_JSON/americanfootball_nfl&us,us2&spreads&1-7-24-1-20pm.json"
    # )
    # data_handler.collect_data("americanfootball_nfl", None, None, "h2h", "decimal", "local", filename="Data/Sample_API_JSON/americanfootball_nfl&us2&h2h&1-5-24-5-10.json")

if __name__ == "__main__":
    main()