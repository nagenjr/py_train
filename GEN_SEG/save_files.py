import pandas as pd

# set Date as the index
df = pd.read_csv('vip.csv', keep_default_na=False)
value = df['Devices'].values["i"]

# iterate through each column and save it
for col in df.columns:
    df[col].to_csv({col}.csv', index=True)


