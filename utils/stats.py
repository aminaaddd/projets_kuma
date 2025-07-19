import pandas as pd

pd.set_option('display.max_columns', None)

df = pd.read_excel("06_09_2021_matches_Algeria.xlsx")

df = df.dropna(how="all") 

print(df.columns.tolist())
