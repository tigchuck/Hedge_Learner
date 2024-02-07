from DataHandler import DataHandler
from FileHandler import FileHandler
from Indicators import fair_price, true_odds
import matplotlib.pyplot as plt  
import pandas as pd

def main():
    print(pd.Timestamp("2022-11-14T00:00:00Z") + pd.Timedelta(minutes=15))
    file_id="0b1f0dfae67cca631732edf0ccb5ad33"
    bet_type="h2h"
    
    # fair_price_df = fair_price(file_id=file_id, bet_type=bet_type, filters=["Home_Odds", "Away_Odds", "Draw_Odds"])
    true_odds(file_id=file_id, bet_type=bet_type, filters=["Home_Odds", "Away_Odds", "Draw_Odds"])

    # fig, ax = plt.subplots(2, 3)
    # ax[0,0].plot(fair_price_df.index, fair_price_df["Home_Odds"])
    # ax[0,1].plot(fair_price_df.index, fair_price_df["Away_Odds"])
    # ax[0,2].plot(fair_price_df.index, fair_price_df["Draw_Odds"])
    # ax[1,0].plot(fair_price_df.index, fair_price_df["Home_Odds_Standard_Deviation"])
    # ax[1,1].plot(fair_price_df.index, fair_price_df["Away_Odds_Standard_Deviation"])
    # ax[1,2].plot(fair_price_df.index, fair_price_df["Draw_Odds_Standard_Deviation"])

    # plt.show()

if __name__ == "__main__":
    main()