# Import libraries
import pandas as pd
import random

# Original file name
dataset_file= 'fluprint_export.csv'
# Read the file
df = pd.read_csv(dataset_file)
# Set an empty list for the selected rows
out_rows = []
# Randomly choose rows
for i in range(1000):
    out_rows.append(random.randint(1,df.shape[0]))
# Select the rows and save the output
df.iloc[out_rows, :].to_csv('selected samples.csv')
