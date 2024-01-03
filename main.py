from DataHandler import DataHandler
from OddsMath import OddsMath

def main():
    handler = DataHandler()
    handler.collect_data(request_type="local", filename="SampleData6.json")
    # for filename in handler.list_files(sport="americanfootball_nfl"):
    #     if (filename in file_set):
    #         print(filename)
    #     file_set.add(filename)
    #     df = handler.get_data(filename = filename, sport = "americanfootball_nfl")
    #     odds_df = handler.get_best_odds(odds = df)
        
    #     home_team = odds_df.columns[5]  # COULD CHANGE IF STRUCTURE OF INFO CHANGES
    #     away_team = odds_df.columns[4]  # COULD CHANGE IF STRUCTURE OF INFO CHANGES
    #     best_implied_odds = float("inf")
    #     for _, row in odds_df.iterrows():
    #         home_prob = OddsMath.implied_prob(row[home_team])
    #         away_prob = OddsMath.implied_prob(row[away_team])
    #         best_implied_odds = min(best_implied_odds, away_prob + home_prob)
    #     if (best_implied_odds < 1):
    #         print(f"{away_team} @ {home_team}: {best_implied_odds}\n")

if __name__ == "__main__":
    print("Running...")
    main()