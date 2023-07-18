import glob
import pandas as pd

csvs = glob.glob('/scratch/a.hek4/results/5km/1-initial_csvs/*.csv')
out_file = '/scratch/a.hek4/results/5km_cd_investigation.csv'


dfList = [pd.read_csv(c) for c in csvs]
    
df = pd.concat(dfList)  
df.to_csv(out_file)


