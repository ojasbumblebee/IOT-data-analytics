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


def load_csv_data(filename):
    dataframe = pd.read_csv(filename)
    return dataframe

def inner_join_on_data_node_frame(entire_data, node_data):

    result = pd.merge(entire_data,
                      node_data[['node_id', 'lat', 'lon']],
                      on='node_id',
                      how='inner')
    return result


def inner_join_on_data_sensor_frame(combined_data_frame, sensor_data):

    result = pd.merge(combined_data_frame,
                      sensor_data[['sensor', 'parameter', 'hrf_minval', 'hrf_maxval']],
                      on=['sensor', 'parameter'],
                      how='inner')
    return result


def filter_corrupt_entries(combined_data_frame):
    # filter data values for corrupt data
    combined_data_frame = combined_data_frame[(combined_data_frame['value_hrf'].astype(float)
                                               >= combined_data_frame['hrf_minval'].astype(float)[0]) &
                                              (combined_data_frame['value_hrf'].astype(float)
                                               <= combined_data_frame['hrf_maxval'].astype(float)[0])]
    return combined_data_frame


def filter_data_for_sensor_and_parameter(combined_data_frame):
    # Filter the combined data frame for the desired sensor values

    print(combined_data_frame['sensor'].unique())
    combined_data_frame = combined_data_frame.loc[combined_data_frame['sensor'] == args.sensor]
    combined_data_frame = combined_data_frame.loc[combined_data_frame['parameter'] == args.parameter]
    combined_data_frame = combined_data_frame.dropna(how="all")

    return combined_data_frame

def adapter(current_data_chunk, sensor_data, node_data):


    #Call filtering on sensor and parameter
    current_data_chunk = filter_data_for_sensor_and_parameter(current_data_chunk)


    combined_data_frame = inner_join_on_data_node_frame(current_data_chunk, node_data)

    combined_data_frame = inner_join_on_data_sensor_frame(combined_data_frame, sensor_data)

    # Call filtering for sensor range and NaN values
    combined_data_frame = filter_corrupt_entries(combined_data_frame)


    return combined_data_frame


"""Here starts refactoring"""
os.chdir(args.path)

path_name = os.path.split(os.getcwd())
# Load data
node_data = load_csv_data("nodes.csv")
sensor_data = load_csv_data("sensors.csv")

resultant_frame = []
chunksize = 10 ** 6
for current_data_chunk in pd.read_csv("data.csv", chunksize=chunksize):
    print(current_data_chunk.keys())
    resultant_frame.append(adapter(current_data_chunk, sensor_data, node_data))
    break

crash()
# Paths to store the data

combined_data_frame = pd.concat(resultant_frame)


"""daily path :/home/ojas/Documents/independent_study_harry_perros/data/daily"""
"""daily path :/home/ojas/Documents/independent_study_harry_perros/data/weekly"""
"""daily path :/home/ojas/Documents/independent_study_harry_perros/data/monthly"""
"""daily path :/home/ojas/Documents/independent_study_harry_perros/data/yearly"""
os.chdir("/home/ojas/Documents/independent_study_harry_perros/data/denver_data")

combined_data_frame.to_csv(args.sensor+"_"+args.parameter+"_"+path_name[1]+".csv")





