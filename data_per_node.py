import pandas as pd
import os
import matplotlib.pyplot as plt

import subprocess
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer



from arcgis.gis import GIS
my_gis = GIS()
print(my_gis)
my_gis.map()


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


# now let's save the visualization into the temp file and render it
from tempfile import NamedTemporaryFile
tmp = NamedTemporaryFile()
my_gis.save(tmp.name)
with open(tmp.name) as f:
    folium_map_html = f.read()

run_html_server(folium_map_html)

"""
os.chdir("../chicago-complete.daily.2018-12-03")
def load_csv_data(filename):
    dataframe = pd.read_csv(filename)
    return dataframe

def display_time_series():
    pass

entire_data = load_csv_data("data.csv")
node_data = load_csv_data("nodes.csv")

entire_data.timestamp = pd.to_datetime(entire_data.timestamp)
entire_data.set_index('timestamp',inplace=True)
some_node_data = entire_data.loc[entire_data['node_id'] == node_data["node_id"][6]]

try:
    data_meta_sense_bmp180 = some_node_data.loc[some_node_data['sensor'] == "bmp180"]
    temp_data_meta_sense_bmp180 = data_meta_sense_bmp180 .loc[data_meta_sense_bmp180 ['parameter'] == "temperature"]
    temp_data_meta_sense_bmp180 = temp_data_meta_sense_bmp180['value_hrf'].astype(float)
    temp_data_meta_sense_bmp180.plot(y='value_hrf', label = "bmp180", legend = True)

    data_meta_sense_tmp112 = some_node_data.loc[some_node_data['sensor'] == "tmp112"]
    temp_data_meta_sense_tmp112 = data_meta_sense_tmp112.loc[data_meta_sense_tmp112['parameter'] == "temperature"]
    temp_data_meta_sense_tmp112 = temp_data_meta_sense_tmp112['value_hrf'].astype(float)
    temp_data_meta_sense_tmp112.plot(y='value_hrf', label = "tmp112", legend = True)


except:
    pass

plt.title("temperature data from different temperature sensors for a particular node")
plt.show()
"""