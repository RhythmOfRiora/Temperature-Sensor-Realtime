from __future__ import division
import serial
import time



class Temperature_Sensor(object):
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


