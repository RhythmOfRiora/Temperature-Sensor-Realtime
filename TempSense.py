from __future__ import division
import serial
import time
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import datetime
#import Temperature_Sensor.Temperature_Sensor.Temperature_Sensor
import IPython
import IPython.core.display



class TempSense(object):
    def __init__(self):
        self.port = serial.Serial('COM7')


    def reset(self):
        self.port.write("\xE3\xC1\xE1\xCC")
        self.port.read(2)


    def serial_protocol_detect(self):
    # Do DS2480B reset/detect
        self.port.send_break(2 / 1000.0)
        time.sleep(2 / 1000.0)
        self.port.write("\xC1")  # Reset Pulse
        time.sleep(2 / 1000.0)
        self.port.write("\x17\x45\x5B\x0F\x91")
        resp = self.port.read(5)
        if resp != "\x16\x44\x5a\x00\x93":
            raise Exception("DS2480B not found.")
        self.reset()


    def read_rom(self):
        self.port.write("\x33")
        self.port.write("\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF")
        resp = self.port.read(9)
        self.reset()


    def read_scratchpad(self):
        bytelist = []
        self.port.write("\xBE")
        self.port.write("\xFF" * 9)
        resp = self.port.read(10)
        for i in resp:
            bytelist.append(ord(i))
        self.reset()
        return bytelist[1:]


    def convert_temperature(self):
        self.port.write("\x44")
        time.sleep(1)
        resp = self.port.read(1)
        self.reset()


    def get_readable_temperature(self, byte_list):
        b = byte_list[1] << 8 | byte_list[0]
        return b/16
        #print "The current temperature is: ", b/16


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
    Create_Realtime_Graph(sensor)


if __name__ == "__main__":
    Sense_Temperature()