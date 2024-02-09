import pandas as pd
from DataHandler import DataHandler

dh = DataHandler()

# Initial Call
timestamps = []
sport = "soccer_epl"
bookmakers = ["betmgm", "bovada", "draftkings", "fanduel", "mybookieag", "williamhill_us", "espnbet", "hardrockbet", "tipico_us", "pinnacle"]
markets = "h2h"
odds_format = "decimal"
# init_date = "2020-09-05T00:00:00Z"
date = pd.Timestamp("2021-05-24T00:00:00Z")
end_date = pd.Timestamp("2021-05-25T00:00:00Z")


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
    ts, prev_ts, next_ts = timestamps
    print(f"Requested: {date.strftime('%Y-%m-%dT%XZ')}\n\tPulled: {ts}\n")
    date = date + pd.Timedelta(minutes=10)
    if (pd.Timestamp(next_ts) > date):
        date = pd.Timestamp(next_ts)
        

