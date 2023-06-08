import glob
import pandas as pd

csvs = glob.glob('/scratch/a.hek4/results/1_deg/csvs/wwf_grid/12m/*.csv')
out_file = '/scratch/a.hek4/results/1_deg/csvs/wwf_grid_12m.csv'


dfList = [pd.read_csv(c) for c in csvs]
    
df = pd.concat(dfList)  
df.to_csv(out_file)


