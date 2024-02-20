import yaml
import argparse
import time
import copy

import pandas as pd
from modules import DataHandler

parser = argparse.ArgumentParser(description='Hedge Learner Download Parser')
parser.add_argument('--config', default='./config.yaml')

def download():
    global args
    args = parser.parse_args()
    with open(args.config) as f:
        config = yaml.safe_load(f)
        
    for key in config:
        for k, v in config[key].items():
            setattr(args, k, v)
            
    dh = DataHandler()
    timestamps = []
    sport = args.sport
    bookmakers = args.bookmakers
    markets = args.markets
    odds_format = args.odds_format
    date = pd.Timestamp(args.start_date)
    end_date = pd.Timestamp(args.end_date)
    time_step = args.step
            
    loop = 0
    while (date < end_date):
        timestamps = []
        dh.collect_data(
            sport=sport, 
            bookmakers=bookmakers,
            markets=markets,
            odds_format=odds_format,
            request_type="historic",
            date=date.strftime("%Y-%m-%dT%XZ"),
            timestamps=timestamps
        )
        
        ts, prev_ts, next_ts = timestamps
        print(f"Loop {loop}\tDate Requested: {date.strftime('%Y-%m-%dT%XZ')}\tDate Received: {ts}")
        date = date + pd.Timedelta(minutes=time_step)
        if (pd.Timestamp(next_ts) > date):
            date = pd.Timestamp(next_ts)
        loop += 1



if __name__ == "__main__":
    download()