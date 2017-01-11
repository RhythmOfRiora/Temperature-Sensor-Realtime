from __future__ import division
import serial
import serial.tools.list_ports
import time



class Temperature_Sensor(object):
    def __init__(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if p.description[0:8] == "Prolific" or p.vid == 0x067b:
                port_conn = str(p.device).encode('ascii', 'ignore')
        self.port = serial.Serial(port_conn)


# Reset before issuing another command.
    def reset(self):
        self.port.write("\xE3\xC1\xE1\xCC")
        self.port.read(2)


# Do DS2480B reset/detect.
    def serial_protocol_detect(self):
        self.port.send_break(2 / 1000.0)
        time.sleep(2 / 1000.0)
        self.port.write("\xC1")  # Reset Pulse
        time.sleep(2 / 1000.0)
        self.port.write("\x17\x45\x5B\x0F\x91")
        resp = self.port.read(5)
        if resp != "\x16\x44\x5a\x00\x93":
            raise Exception("DS2480B not found.")
        self.reset()


# Do a presence check for the 1-Wire device on the bus.
    def read_rom(self):
        self.port.write("\xE3\xC1\xE1")
        self.port.read(1)
        self.port.write("\x33")
        self.port.write("\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF")
        resp = self.port.read(9)
        time.sleep(0.2)
        # for i in resp:
        #     print hex(ord(i)),
        # print
        self.reset()


# Read the scratchpad where the temperature data will be stored.
    def read_scratchpad(self):
        byte_list = []
        self.port.write("\xBE")
        self.port.write("\xFF" * 9)
        resp = self.port.read(10)
        for i in resp:
            byte_list.append(ord(i))
        self.reset()
        return byte_list[1:]


# Initiate a temperature conversion and store on the scratchpad.
    def convert_temperature(self):
        self.port.write("\x44")
        time.sleep(1)
        resp = self.port.read(1)
        self.reset()


# Convert the temperaturefrom the scratchpad format specified in the DS to a readable format in Celsius.
    def get_readable_temperature(self, byte_list):
        b = byte_list[1] << 8 | byte_list[0]
        print "The current temperature is: ", b / 16
        return b/16
        #print "The current temperature is: ", b/16


