import pandas as pd
import os
import matplotlib.pyplot as plt

os.chdir("../chicago-complete.weekly.2018-12-17-to-2018-12-23")


def load_csv_data(filename):
    dataframe = pd.read_csv(filename)
    return dataframe


def display_time_series():
    pass

chunksize = 10 ** 6
for chunk in pd.read_csv("data.csv", chunksize=chunksize):
    print(chunk.head())


#entire_data = load_csv_data("data.csv")
node_data = load_csv_data("nodes.csv")
#print(entire_data.head())


