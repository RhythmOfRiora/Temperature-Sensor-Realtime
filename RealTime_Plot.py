# This is a 1-Wire Temperature Sensor which produces real-time graphs. It uses a variety of Maxim hardware detailed
# in the docs.
#     Copyright (C) <2017>  <C. Burn>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#     Please contact cburn01@qub.ac.uk for any comments or queries.


from Temperature_Sensor import Temperature_Sensor
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import datetime
import time
import sys
import os
import json
import IPython
import IPython.core.display

###
#   This code takes a command line argument of the path to a .txt or .json file containing the following fields:
#   "api_key", "username", "stream_id". These refer to your Plotly username, API key and Stream ID which can be
#   found in the Settings section of your Plotly account.
###


# This function aggregates calls to functions in the Temperature Sensor class and returns a readable temperature.
def extract_temperature(sensor):
    sensor.serial_protocol_detect()
    sensor.read_rom()
    sensor.read_scratchpad()
    sensor.convert_temperature()
    return sensor.get_readable_temperature(sensor.read_scratchpad())


# This function ensures that the configuration files contain the correct details and are not corrupted.
def set_configuration(data):
    tls.set_credentials_file(username=data["username"], api_key=data['api_key'])
    tls.set_config_file(sharing='public',
                        world_readable=True,
                        plotly_streaming_domain="stream.plot.ly",
                        plotly_ssl_verification=True,
                        plotly_proxy_authorization=False,
                        plotly_api_domain="https://api.plot.ly",
                        auto_open=True,
                        plotly_domain="https://plot.ly")


# This function draws the "real time" graph in a loop.
def draw_graph_loop(stream, sensor):
    while True:
        x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        y = extract_temperature(sensor)
        stream.write(dict(x=x, y=y))
        time.sleep(0.5)  # plot a point every second
    stream.close()


# This function initializes the Plotly graph.
def initialize_graph(stream_temp):
    trace1 = go.Scatter(x=[],y=[],mode='lines+markers',stream=stream_temp)
    data = go.Data([trace1])
    layout = go.Layout(title='Time Series')
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='python-streaming')


# This function calls the setup and main graph loop.
def create_real_time_graph(sensor):
    config_file_path = sys.argv[1]
    with open(config_file_path) as data_file:
        data = json.load(data_file)
    set_configuration(data)
    stream_id = data["stream_id"]
    stream_temp = go.Stream(token=stream_id,maxpoints=80)
    initialize_graph(stream_temp)
    s = py.Stream(stream_id)
    s.open()
    time.sleep(5)
    draw_graph_loop(s, sensor)


# Main Code
def sense_temperature():
    sensor = Temperature_Sensor.Temperature_Sensor()
    extract_temperature(sensor)
    create_real_time_graph(sensor)


if __name__ == "__main__":
    sense_temperature()