from Temperature_Sensor import Temperature_Sensor
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import datetime
import time
import IPython
import IPython.core.display


def extract_temperature(sensor):
    sensor.serial_protocol_detect()
    sensor.read_rom()
    sensor.read_scratchpad()
    sensor.convert_temperature()
    return sensor.get_readable_temperature(sensor.read_scratchpad())


def set_configuration():
    tls.set_credentials_file(username='cburn92', api_key='Mo832agwJKwbmbV1VJVA')
    tls.set_config_file(sharing='public',
                        world_readable=True,
                        plotly_streaming_domain="stream.plot.ly",
                        plotly_ssl_verification=True,
                        plotly_proxy_authorization=False,
                        plotly_api_domain="https://api.plot.ly",
                        auto_open=True,
                        plotly_domain="https://plot.ly")


def draw_graph_loop(stream, sensor):
    while True:
        x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        y = extract_temperature(sensor)
        stream.write(dict(x=x, y=y))
        time.sleep(0.5)  # plot a point every second
    stream.close()


def initialize_graph(stream_temp):
    trace1 = go.Scatter(x=[],y=[],mode='lines+markers',stream=stream_temp)
    data = go.Data([trace1])
    layout = go.Layout(title='Time Series')
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='python-streaming')


def create_real_time_graph(sensor):
    set_configuration()
    stream_id = "ygv88fjwgj"
    stream_temp = go.Stream(token=stream_id,maxpoints=80)
    initialize_graph(stream_temp)
    s = py.Stream(stream_id)
    s.open()
    time.sleep(5)
    draw_graph_loop(s, sensor)


def sense_temperature():
    # Main Code
    sensor = Temperature_Sensor.Temperature_Sensor()
    create_real_time_graph(sensor)


if __name__ == "__main__":
    sense_temperature()