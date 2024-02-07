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
date = pd.Timestamp("2023-01-11T13:10:00Z")
end_date = pd.Timestamp("2023-05-29T00:00:00Z")


loop = 0
while (date < end_date):
    timestamps = []
    if (loop % 500 == 0):
        dh.collect_data (
            sport=sport,
            bookmakers=bookmakers,
            markets=markets,
            odds_format=odds_format,
            request_type="historic",
            date=date.strftime("%Y-%m-%dT%XZ"),
            timestamps=timestamps,
            filename=f"Data/Sample_API_JSON/{sport}-{markets}-{date.strftime('%Y-%m-%dT%XZ')}.json"
        )
    else:
        dh.collect_data(
            sport=sport, 
            bookmakers=bookmakers,
            markets=markets,
            odds_format=odds_format,
            request_type="historic",
            date=date.strftime("%Y-%m-%dT%XZ"),
            timestamps=timestamps
        )
    loop += 1
    print(f"Requested: {date.strftime('%Y-%m-%dT%XZ')}\n\tPulled: {timestamps[0]}\n")
    date = date + pd.Timedelta(minutes=10)

