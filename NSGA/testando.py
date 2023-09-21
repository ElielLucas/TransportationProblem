import pandas as pd
print(pd.__version__)
# Create two sample DataFrames
df1 = pd.DataFrame({
    'A': [1, 2],
    'B': [3, 4]
})

df2 = pd.DataFrame({
    'A': [5],
    'B': [6]
})
# Append df2 to df1
df_combined = pd.concat([df1, df2], ignore_index=True)
print(df_combined)