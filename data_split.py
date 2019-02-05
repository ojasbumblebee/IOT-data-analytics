import pandas as pd
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-s", "--sensor", required=True,
                    help="mention name of sensor for which the query is being made")
parser.add_argument("-p", "--parameter", required=True,
                    help="what parameter of the sensor is being extracted out")
parser.add_argument("--path", required=True,
                    help="the input path to data folder")


args = parser.parse_args()
print(args)

os.chdir("../chicago-complete.daily.2018-12-03")

path_name = os.path.split(os.getcwd())
print(path_name)
# Load data

def load_csv_data(filename):
    dataframe = pd.read_csv(filename)
    return dataframe

entire_data = load_csv_data("data.csv")
node_data = load_csv_data("nodes.csv")

# Print node.csv column keys
print(entire_data.keys())

def inner_join_on_data_node_frame(entire_data, node_data):

    result = pd.merge(entire_data,
                      node_data[['node_id', 'lat', 'lon']],
                      on='node_id',
                      how='inner')
    return result

combined_data_frame = inner_join_on_data_node_frame(entire_data, node_data)
print(combined_data_frame.keys())

#Filter the combined data frame for the desired sensor values
combined_data_frame = combined_data_frame.loc[combined_data_frame['sensor'] == args.sensor]
combined_data_frame = combined_data_frame.loc[combined_data_frame['parameter'] == args.parameter]
combined_data_frame = combined_data_frame.dropna(how="all")

#filter data values for corrupt data
sensor_data = load_csv_data("sensors.csv")
def inner_join_on_data_sensor_frame(combined_data_frame, sensor_data):

    result = pd.merge(combined_data_frame,
                      sensor_data[['sensor', 'parameter', 'hrf_minval', 'hrf_maxval']],
                      on=['sensor', 'parameter'],
                      how='inner')
    return result

combined_data_frame = inner_join_on_data_sensor_frame(combined_data_frame, sensor_data)
print(combined_data_frame.keys())

combined_data_frame= combined_data_frame[(combined_data_frame['value_hrf'].astype(float)
                                        >= combined_data_frame['hrf_minval'].astype(float)[0]) &
                                        (combined_data_frame['value_hrf'].astype(float)
                                         <= combined_data_frame['hrf_maxval'].astype(float)[0])]


# Paths to store the data
"""daily path :/home/ojas/Documents/independent_study_harry_perros/data/daily"""
"""daily path :/home/ojas/Documents/independent_study_harry_perros/data/weekly"""
"""daily path :/home/ojas/Documents/independent_study_harry_perros/data/monthly"""
"""daily path :/home/ojas/Documents/independent_study_harry_perros/data/yearly"""
os.chdir("/home/ojas/Documents/independent_study_harry_perros/data/weekly")

combined_data_frame.to_csv(args.sensor+"_"+args.parameter+"_"+path_name[1]+".csv")
