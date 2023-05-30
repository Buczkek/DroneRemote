
# Watch this video for more information about that library https://www.youtube.com/watch?v=aP8rSN-1eT0
import time
import math
import urandom

import machine

from nrf24l01 import NRF24L01
from machine import SPI, Pin
import struct

# sleep(5)


def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


pitch_pin = machine.ADC(27)
yaw_pin = machine.ADC(28)
throttle_pin = machine.ADC(26)

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


def send(nrf, msg):
    msg += ';'

    nrf.stop_listening()
    try:
        encoded_string = msg.encode()
        byte_array = bytearray(encoded_string)
        buf = struct.pack("s", byte_array)
        nrf.send_start(byte_array)
    except OSError:
        print("Sorry message not sent")
    nrf.start_listening()
nrf = setup()
nrf.start_listening()
msg_string = ""

i = 0
last = time.ticks_ms()


def gen_unique_id(bytes_num: int = 4):
    """ Generates a unique ID of the specified byte length using urandom.getrandbits() """
    if bytes_num <= 4:
        return urandom.getrandbits(bytes_num * 8)
    else:
        result = bytearray()
        while bytes_num > 4:
            result += int.to_bytes(urandom.getrandbits(32), 4, 'big')
            bytes_num -= 4
        result += int.to_bytes(urandom.getrandbits(bytes_num * 8), bytes_num, 'big')
        return result


def gen_frame_for_angles(pitch: int, yaw: int, throttle: int, *, frame_length: int = 32):
    frame = bytearray()
    frame += b'\x00'
    frame += b'\xf0'
    frame += gen_unique_id(10)
    payload = bytearray(14) + pitch.to_bytes(2, 'big') + yaw.to_bytes(2, 'big') + throttle.to_bytes(2, 'big')
    frame += payload
    return frame


last = time.ticks_ms()
times = 0
led.value(1)
while True:
    pitch_val = pitch_pin.read_u16()
    yaw_val = yaw_pin.read_u16()
    throttle_val = throttle_pin.read_u16()
    pitch_final = clamp(map_value(pitch_val, 400, 65535, 11, -10), -10, 10)
    yaw_final = clamp(map_value(yaw_val, 400, 65535, 11, -10), -10, 10)
    throttle_final = clamp(map_value(throttle_val, 2300, 57100, 400, 0), 0, 400)

    # print(f"pitch: {pitch_final} raw: {pitch_val} " +
    #       f"yaw: {yaw_final} raw: {yaw_val} " +
    #       f"throttle: {throttle_final} raw: {throttle_val}")
    package = gen_frame_for_angles(pitch_final+50, yaw_final+50, throttle_final)
    # print(package)

    times += 1
    now = time.ticks_ms()

    nrf.flush_rx()
    nrf.flush_tx()
    nrf.send_start(package)

    if time.ticks_diff(now, last) > 1000:
        print(f"times: {times}")
        times = 0
        last = now

    # if nrf.any():
    #     package = nrf.recv()
    #     print(f"package: {package}")
    # sleep(0.1)
