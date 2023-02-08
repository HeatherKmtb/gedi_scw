import glob
import pandas as pd

csvs = glob.glob('/scratch/a.hek4/results/1_deg/csvs/GEDI02_B_2020_Q1/*.csv')
out_file = '/scratch/a.hek4/results/1_deg/csvs/2020_Q1.csv'


dfList = [pd.read_csv(c) for c in csvs]
    
df = pd.concat(dfList)  
df.to_csv(out_file)


