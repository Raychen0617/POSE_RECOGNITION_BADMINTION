import pandas as pd
import sys

csvfile = sys.argv[1]
df = pd.read_csv(csvfile)
print(df) 
