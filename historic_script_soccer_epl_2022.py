import pandas as pd
from DataHandler import DataHandler

dh = DataHandler()

# Initial Call
timestamps = []
sport = "soccer_epl"
bookmakers = ["betmgm", "bovada", "draftkings", "fanduel", "mybookieag", "williamhill_us", "espnbet", "hardrockbet", "tipico_us", "pinnacle"]
markets = "h2h"
odds_format = "decimal"
# init_date = "2022-08-01T00:00:00Z"
init_date = "2022-09-01T00:05:00Z"
# end_date = pd.Timestamp("2022-11-14T00:00:00Z")
# end_date = pd.Timestamp("2022-09-01T00:00:00Z")

dh.collect_data(
    sport=sport, 
    bookmakers=bookmakers,
    markets=markets,
    odds_format=odds_format,
    request_type="historic",
    date=init_date,
    timestamps=timestamps
)
_, _, ts = timestamps

while (pd.Timestamp(ts) < end_date):
    timestamps = []
    dh.collect_data(
        sport=sport, 
        bookmakers=bookmakers,
        markets=markets,
        odds_format=odds_format,
        request_type="historic",
        date=ts,
        timestamps=timestamps
    )
    _, _, ts = timestamps
    print(ts)
    print()

