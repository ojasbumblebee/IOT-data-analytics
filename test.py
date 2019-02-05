import os
import pandas as pd
import numpy as np
import time
import plotly
plotly.tools.set_credentials_file(username='ovbarve', api_key='CwuNsZPxOf5O8PdZoXSc')

from plotly.grid_objs import Grid, Column


# Set path to data
os.chdir("../chicago-complete.daily.2018-12-03")
import plotly.plotly as py
import plotly.graph_objs as go

mapbox_access_token = 'pk.eyJ1Ijoib3ZiYXJ2ZSIsImEiOiJjanJtZ3BiOGgwajgwNDN1dXB2NTRoNTBtIn0.bcN73ZMjMLnAYI0SZQ_Vgg'

# mapbox_access_token = 'ADD_YOUR_TOKEN_HERE'
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

def data_filter(entire_data):
    # First filter data based on sensor and then define range of permissible sensor values
    entire_data = entire_data[entire_data.sensor == "tmp112"]
    entire_data = entire_data[(entire_data['value_hrf'].astype(float) >= -50) &
                              (entire_data['value_hrf'].astype(float) <= 50)]
    return entire_data

def inner_join_on_data_node_frames(entire_data, node_data):

    result = pd.merge(entire_data,
                      node_data[['node_id', 'lat', 'lon']],
                      on='node_id',
                      how='inner')
    return result

latitudes_array, longitudes_array = plot_nodes(node_data)
entire_data = data_filter(entire_data)
combined_frame = inner_join_on_data_node_frames(entire_data, node_data)

print(combined_frame.timestamp.unique())

columns = []
for i, year in enumerate(latitudes_array):
    #print(longitudes_array[i])
    lons = longitudes_array
    lats = latitudes_array
    columns.append(Column(lons, "x{}".format(i + 1)))
    columns.append(Column(lats, "y{}".format(i + 1)))

grid = Grid(columns)

py.grid_ops.upload(grid, "try_one"+str(time.time()), auto_open=False)


trace1 = go.Scattermapbox(
    # GENERAL
    lonsrc = grid.get_column_reference("x1"),
    latsrc = grid.get_column_reference("y1"),
    mode = "markers",
    hoverinfo = "lon+lat+text",
)

animation_time = 1000
transition_time = 300
slider_transition_time = 300

slider = dict(

    # GENERAL
    plotlycommand = "animate",
    values = latitudes_array,
    initialValue = latitudes_array[0],
    visible = True,

    # ARGUMENTS
    args = [
        "slider.value",
        dict(
            duration = animation_time,
            ease = "cubic-in-out",
        ),
    ],

)

sliders = dict(

    # GENERAL
    active = 0,
    steps = [],

    currentvalue = dict(
        font = dict(size = 16),
        prefix = "latitudes : ",
        xanchor = "right",
        visible = True,
    ),
    transition = dict(
        duration = slider_transition_time,
        easing = "cubic-in-out",
    ),

    # PLACEMENT
    x = 0.1,
    y = 0,
    pad = dict(t = 40, b = 10),
    len = 0.9,
    xanchor = "left",
    yanchor = "top",
)

for year in latitudes_array:

    slider_step = dict(

            # GENERAL
            method = "animate",
            value = year,
            label = year,

            # ARGUMENTS
            args = [
                [year],
                dict(
                    frame = dict(duration = animation_time, redraw = False),
                    transition = dict(duration = slider_transition_time),
                    mode = "immediate",
                    ),
                ],

            )

    sliders["steps"].append(slider_step)


updatemenus = dict(

    # GENERAL
    type = "buttons",
    showactive = False,
    x = 0.1, #x = 1.1
    y = 0, #y = 1
    pad = dict(t = 60, r = 10),
    xanchor = "right",
    yanchor = "top",
    direction = "left",

    # BUTTONS
    buttons=[
        dict(
            method = "animate",
            label = "Play",

            # PLAY
            args = [
                None,
                dict(
                    frame = dict(duration = animation_time, redraw = False), # False quicker but disables animations
                    fromcurrent = True,
                    transition = dict(duration = transition_time, easing = "quadratic-in-out"), # easing = "cubic-in-out"
                    mode = "immediate",
                    ),
                ],
            ),
        dict(
            method = "animate",
            label = "Pause",

            # PAUSE
            args = [
                [None], # Note the list
                dict(
                    frame = dict(duration = 0, redraw = False), # Idem
                    mode = "immediate",
                    transition = dict(duration = 0),
                    ),
                ],
            ),
        ],
)

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
    updatemenus = [updatemenus],
    sliders = [sliders],
)

frames = []

for i, year in enumerate(latitudes_array):

    # Create frame for each subplot
    frame_trace1 = dict(
        lonsrc = grid.get_column_reference("x{}".format(i + 1)),
        latsrc = grid.get_column_reference("y{}".format(i + 1))
    )

    frame = dict(
        data=[frame_trace1],
        name=year,
        traces=[0],
    )
    frames.append(frame)

data = [trace1]
figure = dict(data=data, layout=layout, frames=frames)
py.create_animations(figure, filename="try_one"+str(time.time()), auto_open=True)