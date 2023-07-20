import glob
import pandas as pd
import os

csvs = glob.glob('/scratch/a.hek4/results/5km/csvs/*.csv')
out_file = '/scratch/a.hek4/results/5km.csv'

csv_list = []

for csv in csvs:
    try:
        if os.stat(csv).st_size>0:
              csv_list - csv_list.append(csv)
    except OSError:
        continue


dfList = [pd.read_csv(c) for c in csv_list]
    
df = pd.concat(dfList)  
df.to_csv(out_file)


