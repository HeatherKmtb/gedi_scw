import glob
import pandas as pd
import os

csvs = glob.glob('/scratch/a.hek4/results/1_deg/csvs/summer/*.csv')
out_file = '/scratch/a.hek4/results/seasons.csv'

csv_list = list()

for csv in csvs:
    try:
        if os.stat(csv).st_size>0:
              csv_list.append(csv)
    except OSError:
        continue


dfList = [pd.read_csv(c) for c in csv_list]
    
df = pd.concat(dfList)  
df.to_csv(out_file)


