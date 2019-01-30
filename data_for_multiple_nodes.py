import pandas as pd
import os
import matplotlib.pyplot as plt

os.chdir("../chicago-complete.daily.2018-12-03")


def load_csv_data(filename):
    dataframe = pd.read_csv(filename)
    return dataframe


def display_time_series():
    pass


entire_data = load_csv_data("data.csv")
node_data = load_csv_data("nodes.csv")

entire_data.timestamp = pd.to_datetime(entire_data.timestamp)
entire_data.set_index('timestamp', inplace=True)
for i in range(5, 13):

    some_node_data = entire_data.loc[entire_data['node_id'] == node_data["node_id"][i]]

    try:
        data_meta_sense_bmp180 = some_node_data.loc[some_node_data['sensor'] == "tmp112"]
        temp_data_meta_sense_bmp180 = data_meta_sense_bmp180.loc[data_meta_sense_bmp180['parameter'] == "temperature"]
        temp_data_meta_sense_bmp180 = temp_data_meta_sense_bmp180['value_hrf'].astype(float)
        temp_data_meta_sense_bmp180.plot(y='value_hrf', label="tmp112_" + str(i), legend=True)
    except:
        pass

plt.title("temperature data from different nodes ")
plt.show()