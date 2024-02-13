from DataHandler import DataHandler
from FileHandler import FileHandler
from Indicators import fair_price, true_odds
import matplotlib.pyplot as plt  
import pandas as pd
import os

def main():
    file_id="0b1f0dfae67cca631732edf0ccb5ad33"
    bet_type="h2h"
    
    fair_price_df = fair_price(file_id=file_id, bet_type=bet_type, filters=["Home_Odds", "Away_Odds", "Draw_Odds"])
    # print(fair_price_df["Home_Odds"].ewm(min_periods=64, span=1.5).mean().iloc[62:])
    true_odds_df = true_odds(file_id=file_id, bet_type=bet_type, filters=["Home_Odds", "Away_Odds", "Draw_Odds"])

    fig, ax = plt.subplots(3,1)
    ax[0].plot(fair_price_df.index, fair_price_df["Home_Odds"])
    # ax[0].plot(fair_price_df.index, fair_price_df["Home_Odds"].rolling(16).mean())
    # ax[0].plot(fair_price_df.index, fair_price_df["Home_Odds"].ewm(span=16).mean())
    ax[0].plot(true_odds_df.index, true_odds_df["Home_Odds"])
    ax[0].legend(["Fair Price", "True Odds"])
    ax[1].plot(fair_price_df.index, fair_price_df["Away_Odds"])
    # ax[1].plot(fair_price_df.index, fair_price_df["Away_Odds"].rolling(16).mean())
    # ax[1].plot(fair_price_df.index, fair_price_df["Away_Odds"].ewm(span=16).mean())
    ax[1].plot(true_odds_df.index, true_odds_df["Away_Odds"])
    ax[2].plot(fair_price_df.index, fair_price_df["Draw_Odds"])
    # ax[2].plot(fair_price_df.index, fair_price_df["Draw_Odds"].rolling(16).mean())
    # ax[2].plot(fair_price_df.index, fair_price_df["Draw_Odds"].ewm(span=16).mean())
    ax[2].plot(true_odds_df.index, true_odds_df["Draw_Odds"])
    
    # DERIVATIVE OF EWM SEEMS LIKE IT COULD HAVE SOME VALUE BASED ON HOW POSITIVE OR NEGATIVE IT IS???
    # ax[1].plot(fair_price_df.index, fair_price_df["Home_Odds_Standard_Deviation"])
    # ax[1,1].plot(fair_price_df.index, fair_price_df["Away_Odds_Standard_Deviation"])
    # ax[1,2].plot(fair_price_df.index, fair_price_df["Draw_Odds_Standard_Deviation"])

    plt.show()


if __name__ == "__main__":
    main()