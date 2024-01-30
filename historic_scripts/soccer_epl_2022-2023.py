from DataHandler import DataHandler

data_handler = DataHandler()

data_handler.collect_data(
    sport="soccer_epl", 
    regions=["us","us2"], 
    bookmakers=["betmgm", "bovada", "draftkings", "fanduel", "mybookieag", "williamhill_us", "espnbet", "hardrockbet", "tipico_us", "pinnacle"],
    markets="h2h", 
    odds_format="decimal", 
    request_type="historic", 
    date="yyyy-mm-ddThh:mm:ssZ"
    filename="Data/Sample_API_JSON/soccer_epl&us,us2&h2h&1-30-24-4-31pm.json"
)   