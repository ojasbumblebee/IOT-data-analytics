import os
import pandas as pd
import numpy as np
import plotly
plotly.tools.set_credentials_file(username='ovbarve', api_key='CwuNsZPxOf5O8PdZoXSc')

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.grid_objs import Grid, Column


# Set path to data
os.chdir("../chicago-complete.daily.2018-12-03")

# Load data

def load_csv_data(filename):
    dataframe = pd.read_csv(filename)
    return dataframe

entire_data = load_csv_data("data.csv")
node_data = load_csv_data("nodes.csv")

# Print node.csv column keys
print(entire_data.keys())

# Plot Nodes on Map
def plot_nodes(node_data):
    latitudes_array = []
    longitudes_array = []
    for each_row in node_data.itertuples():
        # Put a circle marker at each node location
        latitudes_array.append(each_row.lat)
        longitudes_array.append(each_row.lon)
    return latitudes_array, longitudes_array

latitudes_array, longitudes_array = plot_nodes(node_data)


def inner_join_on_data_node_frames(entire_data, node_data):
    result = pd.merge(entire_data,
                      node_data[['node_id', 'lat', 'lon']],
                      on='node_id',
                      how='inner')
    return result


# First filter data based on sensor and then define range of permissible sensor values
entire_data = entire_data[entire_data.sensor == "tmp112"]
entire_data = entire_data[(entire_data['value_hrf'].astype(float) >= -50) &
                          (entire_data['value_hrf'].astype(float) <= 50)]
combined_frame  = inner_join_on_data_node_frames(entire_data, node_data)


print(combined_frame.keys())
#combined_frame = combined_frame.dropna(how='all')

print(len(combined_frame.node_id.unique()))

remove_n=80000
drop_indices = np.random.choice(combined_frame.index, remove_n, replace=False)
df_subset = combined_frame.drop(drop_indices)
print(len(df_subset.node_id.unique()))

working_frame  = df_subset.head(100)
lati = list(working_frame.lat.unique())[0]
long = list(working_frame.lon.unique())[0]
print(lati, long)
timings = list(working_frame.timestamp.unique())
print(timings)

for timing in timings:
    data_dict = {
        'x': [timing.lat],
        'y': [timing.lat],
        'mode': 'markers',
        'text': list(dataset_by_year_and_cont['country']),
        'marker': {
            'sizemode': 'area',
            'sizeref': 200000,
            'size': list(dataset_by_year_and_cont['pop'])
        },
        'name': continent
    }
    frame['data'].append(data_dict)

    figure['frames'].append(frame)
    slider_step = {'args': [
        [year],
        {'frame': {'duration': 300, 'redraw': False},
         'mode': 'immediate',
         'transition': {'duration': 300}}
    ],
        'label': year,
        'method': 'animate'}
    sliders_dict['steps'].append(slider_step)

"""
mapbox_access_token = 'pk.eyJ1Ijoib3ZiYXJ2ZSIsImEiOiJjanJtZ3BiOGgwajgwNDN1dXB2NTRoNTBtIn0.bcN73ZMjMLnAYI0SZQ_Vgg'

data = [
    go.Scattermapbox(
        lat=latitudes_array,
        lon=longitudes_array,
        mode='markers',
        marker=dict(
            size=16,
            cmax=91,
            cmin=0,
            color=[i for i in range(92)],
            colorbar=dict(
                title='Colorbar'
            ),
            colorscale='Viridis'
        ),
    )
]

sliders_dict = {
    'active': 0,
    'yanchor': 'top',
    'xanchor': 'left',
    'currentvalue': {
        'font': {'size': 20},
        'prefix': 'Year:',
        'visible': True,
        'xanchor': 'right'
    },
    'transition': {'duration': 300, 'easing': 'cubic-in-out'},
    'pad': {'b': 10, 't': 50},
    'len': 0.9,
    'x': 0.1,
    'y': 0,
    'steps': []
}

layout = go.Layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=latitudes_array[0],
            lon=longitudes_array[0]
        ),
        pitch=0,
        zoom=9
    ),
)

fig = dict(data=data, layout=layout)

py.plot(fig, filename='Chicago Mapbox')


"""