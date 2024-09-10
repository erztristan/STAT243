import os
import pandas as pd
import numpy as np
import time

# Calculated rows
rows = 100000
columns = 20

# Create numpy array of random numbers from a standard normal distribution
x = np.random.randn(rows, columns)
print(f"Count of MB:{str(x.nbytes/1e6)} MB")

x = x.round(decimals=12)

# Count MB of a csv-File
pd.DataFrame(x).to_csv("x.csv", header=False, index=False)
print(
    f"File size of the CSV with 12 decimal number: {str(os.path.getsize('x.csv')/1e6)} MB"
)

# Count MB of a pkl-File
pd.DataFrame(x).to_pickle("x.pkl", compression=None)
print(
    f"File size of the PKL with 12 decimal number: {str(os.path.getsize('x.pkl')/1e6)} MB"
)

x = x.round(decimals=4)

# Count MB of a csv-File
pd.DataFrame(x).to_csv("x.csv", header=False, index=False)
print(
    f"File size of the CSV with 4 decimal number: {str(os.path.getsize('x.csv')/1e6)} MB"
)

# Count MB of a pkl-File
pd.DataFrame(x).to_pickle("x.pkl", compression=None)
print(
    f"File size of the PKL with 4 decimal number: {str(os.path.getsize('x.pkl')/1e6)} MB"
)

# Count time reading CSV
t0 = time.time()
df_csv = pd.read_csv("x.csv")
print(f"Time to read CSV: {time.time() - t0:.4f} seconds")

# Count time reading Pickle
t0 = time.time()
df_pkl = pd.read_pickle("x.pkl")
print(f"Time to read Pickle: {time.time() - t0:.4f} seconds")

# Count time reading CSV with use chunks
t0 = time.time()
df_csv = pd.read_csv("x.csv", chunksize=10000, nrows=10000)
print(f"Time to read csv with chunksize 10000: {time.time() - t0:.4f} seconds")

# Count time reading CSV with use skiprows
t0 = time.time()
df_csv = pd.read_csv("x.csv", chunksize=10000, nrows=10000, skiprows=40000)
print(f"Time to read csv with chunks in the middle: {time.time() - t0:.4f} seconds")

# Count time reading CSV without  skiprows
t0 = time.time()
df_csv = pd.read_csv("x.csv", chunksize=10000, nrows=60000)
print(f"Time to read csv with chunks from beginning: {time.time() - t0:.4f} seconds")
