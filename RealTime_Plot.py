import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import datetime
import time
import Temperature_Sensor
import IPython
import IPython.core.display


def Extract_Temperature(sensor):
    sensor.serial_protocol_detect()
    sensor.read_rom()
    sensor.read_scratchpad()
    sensor.convert_temperature()
    return sensor.get_readable_temperature(sensor.read_scratchpad())
    time.sleep(0.5)


def Create_Realtime_Graph(sensor):
    tls.set_credentials_file(username='cburn92', api_key='Mo832agwJKwbmbV1VJVA')
    tls.set_config_file(sharing='public',
                        world_readable=True,
                        plotly_streaming_domain="stream.plot.ly",
                        plotly_ssl_verification=True,
                        plotly_proxy_authorization=False,
                        plotly_api_domain="https://api.plot.ly",
                        auto_open=True,
                        plotly_domain="https://plot.ly")

    stream_id = "ygv88fjwgj"

    # Make instance of stream id object
    stream_1 = go.Stream(
        token=stream_id,  # link stream id to 'token' key
        maxpoints=80  # keep a max of 80 pts on screen
    )

    # Initialize trace of streaming plot by embedding the unique stream_id
    trace1 = go.Scatter(
        x=[],
        y=[],
        mode='lines+markers',
        stream=stream_1  # (!) embed stream id, 1 per trace
    )

    data = go.Data([trace1])
    layout = go.Layout(title='Time Series')
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='python-streaming')

    # We will provide the stream link object the same token that's associated with the trace we wish to stream to
    s = py.Stream(stream_id)
    s.open()

    # Delay start of stream by 5 sec (time to switch tabs)
    time.sleep(5)

    while True:
        x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        y = Extract_Temperature(sensor)

        # Send data to your plot
        s.write(dict(x=x, y=y))
        time.sleep(0.5)  # plot a point every second
    s.close()


def Sense_Temperature():
    # Main Code
    sensor = TempSense()
    Create_Realtime_Graph()


if __name__ == "__main__":
    Sense_Temperature()