
# Watch this video for more information about that library https://www.youtube.com/watch?v=aP8rSN-1eT0
import time
import math

import machine

from nrf24l01 import NRF24L01
from machine import SPI, Pin, I2C
from time import sleep
import struct

# sleep(5)

pitch_pin = machine.ADC(27)

csn = Pin(14, mode=Pin.OUT, value=1)  # Chip Select Not
ce = Pin(17, mode=Pin.OUT, value=0)  # Chip Enable
led = Pin(25, Pin.OUT)  # Onboard LED
payload_size = 32

# Define the channel or 'pipes' the radios use.
# switch round the pipes depending if this is a sender or receiver pico

send_pipe = b"\xd2\xf0\xf0\xf0\xf0"
receive_pipe = b"\xe1\xf0\xf0\xf0\xf0"


def setup():
    print("Initialising the nRF24L0+ Module")
    nrf = NRF24L01(SPI(0), csn, ce, payload_size=payload_size)
    nrf.open_tx_pipe(send_pipe)
    nrf.open_rx_pipe(1, receive_pipe)
    nrf.start_listening()
    return nrf


def flash_led(times: int = None):
    ''' Flashed the built in LED the number of times defined in the times parameter '''
    for _ in range(times):
        led.value(1)
        sleep(0.01)
        led.value(0)
        sleep(0.01)


# def send(nrf, msg):
#     msg += ';'
#
#     nrf.stop_listening()
#     for n in range(len(msg)):
#         try:
#             encoded_string = msg[n].encode()
#             byte_array = bytearray(encoded_string)
#             buf = struct.pack("s", byte_array)
#             nrf.send_start(buf)
#             # print("message",msg[n],"sent")
#             print("sent")
#             flash_led(1)
#         except OSError:
#             print("Sorry message not sent")
#     nrf.start_listening()

def send(nrf, msg):
    msg += ';'

    nrf.stop_listening()
    try:
        encoded_string = msg.encode()
        byte_array = bytearray(encoded_string)
        buf = struct.pack("s", byte_array)
        nrf.send_start(byte_array)
        print(f"msg: {msg}")
        print(f"encoded_string: {encoded_string}")
        print(f"byte_array: {byte_array}")
        print(f"buf: {buf}")
        # print("message",msg[n],"sent")
        # print("sent")
        # flash_led(1)
    except OSError:
        print("Sorry message not sent")
    print("message sent")
    nrf.start_listening()
#
#
# def send_all(nrf, buf):
#     nrf.stop_listening()
#     encoded_string = msg.encode()
#     nrf.send_all(encoded_string)
#     # flash_led(1)
#     nrf.start_listening()


# main code loop
# flash_led(1)
nrf = setup()
nrf.start_listening()
msg_string = ""

i = 0
last = time.ticks_ms()
# delta_time = time.ticks_diff(current_time, last_time) / 1000

# from ST7735 import TFT
# from sysfont import sysfont
#
# spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11), miso=None)
#
# tft = TFT(spi, 12, 15, 13)
#
# tft.initr()
#
# tft.rgb(True)
#
# tft._offset = (2, 1)
#
# tft.fill(TFT.BLACK)
#
# tft.rotation(1)
print("zaczynam")
# while True:
#     msg = ""
#     # Check for Messages
#     # print("waiting for message")
#     if nrf.any():
#         print("got something")
#         package = nrf.recv()
#         # print(f"package: {package}")
#         # message = struct.unpack("s", package)
#         message = package
#         message = message.replace(b'\x00', b'')
#         print(f"message: {message.decode()}")
#         # msg = message.decode()
#         # msg_string += msg
#         # # flash_led(1)
#         #
#         # print(repr(message), len(message), end='\n')
#         # print(msg)
#
#         # # Check for the new line character
#         # if (msg[-1] == ";") and (len(msg_string) <= 50):
#         #     # print("full message", i, "\n\t", msg_string, msg)
#         #     print(msg_string, end='\r')
#         #
#         #     msgs2disp = msg_string.split("\t")
#         #     v = 40
#         #     for msg2disp in msgs2disp:
#         #         # print(time.time() - last, time.time(), last)
#         #         if (time.ticks_diff(time.ticks_ms(), last) / 1000) < .01:
#         #             break
#         #         # tft.fill(TFT.BLACK)
#         #         tft.text((5, v), msg2disp, TFT.WHITE, sysfont, 1)
#         #         v += 8
#         #         last = time.ticks_ms()
#         #     msg_string = ""
#         #     i += 1
#         # else:
#         #     if len(msg_string) <= 50:
#         #         msg_string = msg_string + msg
#         #     else:
#         #         msg_string = ""
#
#         # print(f"msg_string: {msg_string}")

while True:
    print(pitch_pin.read_u16())
