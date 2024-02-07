import pandas as pd
import numpy as np
from FileHandler import FileHandler

# I could precompute fair prices...?
# Could include standard dev as part of this DataFrame
# Should look into pd.groupby
def fair_price(file_id:str, bet_type:str, filters:list[str]):
    fh = FileHandler()
    file_df = fh.read_file(file_id, bet_type, start_time_cutoff=True)
    print(len(file_df))
    update_number = int(file_df.iloc[-1,:]["Update"])
    columns = [None] * ((len(filters) * 3) + 1) 
    columns[0] = "Time"
    for i in range(len(filters)):
        filter = filters[i]
        book = filter + "_Sportsbook"
        sd = filter + "_Standard_Deviation"
        columns[(i * 3) + 1] = filter
        columns[(i * 3) + 2] = book
        columns[(i * 3) + 3] = sd
        
    price_df = pd.DataFrame(index=range(update_number + 1), columns=columns)
    for i in range(update_number+1):
        if (i % 1000 == 0):
            print(i)
        filtered_file_df = file_df.where(file_df["Update"] == i, inplace=False)
        filtered_sd = filtered_file_df.loc[:, filters].std(ddof=0) # ddof set to 0 so no divide by zero when only one row
        for j in range(len(filters)):
            filter = filters[j]
            data_row = filtered_file_df.iloc[filtered_file_df[filter].idxmax()] # Picks first instance of max, which may be problematic
            price_df.iloc[i, 0] = data_row["Time"] # Not sure how I should handle time
            price_df.iloc[i, (j*3)+1] = data_row[filter]
            price_df.iloc[i, (j*3)+2] = data_row["Sportsbook"]
            price_df.iloc[i, (j*3)+3] = filtered_sd[filter]
            
    return price_df    

