import numpy as np
import pandas as pd
import folium
from folium.plugins import HeatMap
import os

import subprocess
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer


# Set path to data
os.chdir("../chicago-complete.daily.2018-12-03")

# Load data

def load_csv_data(filename):
    dataframe = pd.read_csv(filename)
    return dataframe

entire_data = load_csv_data("data.csv")
node_data = load_csv_data("nodes.csv")
print(node_data.keys())
# create a map

#coordinates_frame = node_data[['lat', 'lon']]
folium_map = folium.Map(location=[node_data.lat[1], node_data.lon[1]],
                            zoom_start=10)

for each_row in node_data.itertuples():
    # Put a circle marker at each node location
    popup_text = " Street Address: {}<br> \n description: {}<br> "
    popup_text = popup_text.format(each_row.address,
                                   each_row.description)

    folium.CircleMarker(location=[each_row.lat, each_row.lon],radius=5, fill=True, popup=popup_text).add_to(folium_map)


# ------------------------------------------------------------------------------------------------
# custom temporary-HTML renderer
# https://stackoverflow.com/a/38945907/3494126

PORT = 7000
HOST = '127.0.0.1'
SERVER_ADDRESS = '{host}:{port}'.format(host=HOST, port=PORT)
FULL_SERVER_ADDRESS = 'http://' + SERVER_ADDRESS


def TemproraryHttpServer(page_content_type, raw_data):
    """
    temprorary http web server .
    has features for processing pages with a XML or HTML content.
    """

    class HTTPServerRequestHandler(BaseHTTPRequestHandler):
        """
        An handler of request for the server, hosting XML-pages.
        """

        def do_GET(self):
            """Handle GET requests"""

            # response from page
            self.send_response(200)

            # set up headers for pages
            content_type = 'text/{0}'.format(page_content_type)
            self.send_header('Content-type', content_type)
            self.end_headers()

            # writing data on a page
            self.wfile.write(bytes(raw_data, encoding='utf'))

            return

    if page_content_type not in ['html', 'xml']:
        raise ValueError('This server can serve only HTML or XML pages.')

    page_content_type = page_content_type

    # kill a process, hosted on a localhost:PORT
    subprocess.call(['fuser', '-k', '{0}/tcp'.format(PORT)])

    # Started creating a temprorary http server.
    httpd = HTTPServer((HOST, PORT), HTTPServerRequestHandler)

    # run a temprorary http server
    httpd.serve_forever()


def run_html_server(html_data=None):

    if html_data is None:
        html_data = """
        <!DOCTYPE html>
        <html>
        <head>
        <title>Page Title</title>
        </head>
        <body>
        <h1>This is a Heading</h1>
        <p>This is a paragraph.</p>
        </body>
        </html>
        """

    # open in a browser URL and see a result
    webbrowser.open(FULL_SERVER_ADDRESS)

    # run server
    TemproraryHttpServer('html', html_data)

# ------------------------------------------------------------------------------------------------

# now let's save the visualization into the temp file and render it
from tempfile import NamedTemporaryFile
tmp = NamedTemporaryFile()
folium_map.save(tmp.name)
with open(tmp.name) as f:
    folium_map_html = f.read()

run_html_server(folium_map_html)

