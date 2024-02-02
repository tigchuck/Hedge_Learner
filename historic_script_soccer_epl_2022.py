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
date = "2022-11-07T12:25:00Z"
end_date = pd.Timestamp("2022-11-14T00:00:00Z") # Christmas Break


loop = 0
while (pd.Timestamp(date) < end_date):
    timestamps = []
    if (loop % 100 == 0):
        dh.collect_data (
            sport=sport,
            bookmakers=bookmakers,
            markets=markets,
            odds_format=odds_format,
            request_type="historic",
            date=date,
            timestamps=timestamps,
            filename=f"{sport}-{markets}-{date}"
        )
    else:
        dh.collect_data(
            sport=sport, 
            bookmakers=bookmakers,
            markets=markets,
            odds_format=odds_format,
            request_type="historic",
            date=date,
            timestamps=timestamps
        )
    loop += 1
    _, _, date = timestamps
    print(date)
    print()

