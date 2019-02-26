import pandas as pd
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-p", "--path", required=True,
                    help="the input path to data folder")


args = parser.parse_args()

# Paths to store the data
"""daily path :/home/ojas/Documents/independent_study_harry_perros/data/daily"""
"""daily path :/home/ojas/Documents/independent_study_harry_perros/data/weekly"""
"""daily path :/home/ojas/Documents/independent_study_harry_perros/data/monthly"""
"""daily path :/home/ojas/Documents/independent_study_harry_perros/data/yearly"""

os.chdir(args.path)
file_names = os.listdir(os.getcwd())
resultant_array_of_dataframes = []

for file_name in file_names:

    try:
        dataframe = pd.read_csv(file_name)
        #print(dataframe.keys())
        dataframe['timestamp'] = dataframe['timestamp'].astype('datetime64[m]')
        new_dataframe = dataframe[['node_id', 'timestamp', 'value_hrf']].groupby(['node_id','timestamp']).mean()

        string = file_name.split("_")
        new_dataframe.rename(columns={'value_hrf': 'value_hrf_' + string[0] + "_" + string[1]}, inplace=True)
        resultant_array_of_dataframes.append(new_dataframe)
    except:
        continue

def inner_join_on_data_node_frame(entire_data, node_data):

    result = pd.merge(entire_data,
                      node_data,
                      on=['node_id', 'timestamp'],
                      how='inner')
    return result

dataframe = resultant_array_of_dataframes[0]
for frame in resultant_array_of_dataframes[1:]:
    dataframe = inner_join_on_data_node_frame(dataframe, frame)

# Output path =  "/home/ojas/Documents/independent_study_harry_perros/data/extracted_data"
os.chdir("/home/ojas/Documents/independent_study_harry_perros/data/extracted_data")
"""output filename: output_daily.csv"""
"""output filename: output_weekly.csv"""
"""output filename: output_monthly.csv"""

dataframe.to_csv("output_weekly.csv")
